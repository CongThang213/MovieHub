from typing import Dict

from fastapi import WebSocket

from config.logging_config import logger
from src.infrastructure.services.redis_service import RedisService


class WebsocketManager:
    """Manages WebSocket connections for real-time seat booking updates."""

    def __init__(self, redis_service: RedisService):
        """
        Initialize the connection manager.

        Args:
            redis_service: Redis service for pub/sub
        """
        self._redis_service = redis_service

        # Structure: {showtime_id: {websocket: user_id}}
        self._active_connections: Dict[str, Dict[WebSocket, str]] = {}

        # Structure: {showtime_id: pubsub_listener_task}
        self.pubsub_listeners: Dict[str, any] = {}

    async def connect(self, websocket: WebSocket, showtime_id: str, user_id: str):
        """
        Accepts a new WebSocket connection, registers it under the specified showtime,
        and associates it with the given user. If this is the first connection for the
        showtime, initializes the connection mapping. Also sends the current seat status
        to the newly connected client to ensure they have up-to-date reservation data.

        Args:
            websocket: The WebSocket connection instance to accept and register.
            showtime_id: The unique identifier for the showtime session.
            user_id: The unique identifier for the connecting user.
        """
        await websocket.accept()

        if showtime_id not in self._active_connections:
            self._active_connections[showtime_id] = {}

        self._active_connections[showtime_id][websocket] = user_id
        logger.info(
            f"User {user_id} connected to showtime {showtime_id}. "
            f"Total connections: {len(self._active_connections[showtime_id])}"
        )

        # Send current seat status to the newly connected client
        await self.send_current_seat_status(websocket, showtime_id)

    async def disconnect(self, websocket: WebSocket, showtime_id: str):
        """
        Remove a WebSocket connection from the active connections mapping for a given showtime.

        This method ensures that when a client disconnects, their WebSocket is properly removed from the
        tracking structure. If the disconnected client was the last one for the showtime, the showtime entry
        is also cleaned up to free resources and prevent memory leaks.

        Args:
            websocket: The WebSocket connection to remove.
            showtime_id: The unique identifier for the showtime session.
        """
        if showtime_id in self._active_connections:
            if websocket in self._active_connections[showtime_id]:
                user_id = self._active_connections[showtime_id][websocket]
                del self._active_connections[showtime_id][websocket]
                logger.info(
                    f"User {user_id} disconnected from showtime {showtime_id}. "
                    f"Remaining connections: {len(self._active_connections[showtime_id])}"
                )

                # Clean up if no connections left
                if not self._active_connections[showtime_id]:
                    del self._active_connections[showtime_id]

    async def send_current_seat_status(self, websocket: WebSocket, showtime_id: str):
        """
        Send the current seat reservation status to a newly connected client.

        This ensures the client receives an up-to-date snapshot of all currently reserved seats for the specified showtime,
        allowing the UI to accurately reflect real-time seat availability immediately upon connection.

        Args:
            websocket: The WebSocket connection to send the status to.
            showtime_id: The unique identifier for the showtime session whose seat status is requested.
        """
        try:
            reserved_seats = await self._redis_service.get_all_reserved_seats(
                showtime_id
            )
            message = {
                "type": "initial_status",
                "showtime_id": showtime_id,
                "reserved_seats": [
                    {"seat_id": seat_id, "user_id": user_id, "status": "reserved"}
                    for seat_id, user_id in reserved_seats.items()
                ],
            }
            await websocket.send_json(message)
            logger.debug(f"Sent initial seat status for showtime {showtime_id}")
        except Exception as e:
            logger.error(f"Error sending current seat status: {e}")

    async def broadcast_to_showtime(self, showtime_id: str, message: dict):
        """
        Broadcast a message to all clients connected to a specific showtime.

        This method iterates through all active WebSocket connections for the given showtime
        and sends the provided message to each client. If any connections are found to be
        closed or raise exceptions during sending, they are cleaned up to maintain an
        accurate list of active connections.

        Args:
            showtime_id: The unique identifier for the showtime session whose clients should receive the broadcast.
            message: The message dictionary to broadcast to all connected clients for the specified showtime.
        """
        if showtime_id not in self._active_connections:
            return

        disconnected_websockets = []

        for websocket in self._active_connections[showtime_id].keys():
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Error sending message to websocket: {e}")
                disconnected_websockets.append(websocket)

        # Clean up disconnected websockets
        for websocket in disconnected_websockets:
            await self.disconnect(websocket, showtime_id)

    async def send_personal_message(self, websocket: WebSocket, message: dict):
        """
        Send a message to a specific client via their WebSocket connection.

        This method is used for sending direct, private messages to a single client,
        such as confirmations, error notifications, or personalized updates that should
        not be broadcast to all connected clients.

        Args:
            websocket: The WebSocket connection instance representing the target client.
            message: The message dictionary to send to the client.
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")

    async def handle_seat_action(
        self,
        websocket: WebSocket,
        showtime_id: str,
        user_id: str,
        action: str,
        seat_id: str,
    ):
        """
        Handle seat reservation, release, and extension actions for a specific seat.

        Args:
            websocket: The WebSocket connection of the requesting user.
            showtime_id: The showtime identifier.
            user_id: The user performing the action.
            action: The action to perform ("reserve", "release", "extend").
            seat_id: The seat to act upon.
        """
        try:
            if action == "reserve":
                await self._handle_reserve(websocket, showtime_id, user_id, seat_id)
            elif action == "release":
                await self._handle_release(websocket, showtime_id, user_id, seat_id)
            elif action == "extend":
                await self._handle_extend(websocket, showtime_id, user_id, seat_id)
            else:
                await self.send_personal_message(
                    websocket,
                    {
                        "type": "error",
                        "message": f"Unknown action: {action}",
                    },
                )
        except Exception as e:
            logger.error(f"Error handling seat action: {e}")
            await self.send_personal_message(
                websocket,
                {
                    "type": "error",
                    "message": "An error occurred processing your request",
                },
            )

    async def _handle_reserve(
        self, websocket: WebSocket, showtime_id: str, user_id: str, seat_id: str
    ):
        """
        Attempt to reserve a seat for the user. If successful, broadcast the update to all clients
        and send a success message to the requester. If the seat is already reserved, notify the user.

        Args:
            websocket: The WebSocket connection of the requesting user.
            showtime_id: The showtime identifier.
            user_id: The user attempting to reserve the seat.
            seat_id: The seat to reserve.
        """
        success = await self._redis_service.reserve_seat(showtime_id, seat_id, user_id)
        if success:
            # Broadcast the reservation to all clients
            await self._redis_service.publish_seat_update(
                showtime_id, seat_id, "reserved", user_id
            )
            await self.broadcast_to_showtime(
                showtime_id,
                {
                    "type": "seat_update",
                    "seat_id": seat_id,
                    "status": "reserved",
                    "user_id": user_id,
                    "showtime_id": showtime_id,
                },
            )
            # Notify the requester of success
            await self.send_personal_message(
                websocket,
                {
                    "type": "action_result",
                    "action": "reserve",
                    "seat_id": seat_id,
                    "success": True,
                    "message": "Seat reserved successfully",
                },
            )
        else:
            # Notify the requester that the seat is already reserved
            await self.send_personal_message(
                websocket,
                {
                    "type": "action_result",
                    "action": "reserve",
                    "seat_id": seat_id,
                    "success": False,
                    "message": "Seat already reserved",
                },
            )

    async def _handle_release(
        self, websocket: WebSocket, showtime_id: str, user_id: str, seat_id: str
    ):
        """
        Attempt to release a seat reservation. Only the user who reserved the seat can release it.
        If successful, broadcast the update to all clients and notify the requester. If not permitted,
        send an error message to the requester.

        Args:
            websocket: The WebSocket connection of the requesting user.
            showtime_id: The showtime identifier.
            user_id: The user attempting to release the seat.
            seat_id: The seat to release.
        """
        reserved_by = await self._redis_service.get_seat_reservation(
            showtime_id, seat_id
        )
        if reserved_by == user_id:
            # User is allowed to release the seat
            success = await self._redis_service.release_seat(showtime_id, seat_id)
            if success:
                # Broadcast the release to all clients
                await self._redis_service.publish_seat_update(
                    showtime_id, seat_id, "available", None
                )
                await self.broadcast_to_showtime(
                    showtime_id,
                    {
                        "type": "seat_update",
                        "seat_id": seat_id,
                        "status": "available",
                        "user_id": None,
                        "showtime_id": showtime_id,
                    },
                )
                # Notify the requester of success
                await self.send_personal_message(
                    websocket,
                    {
                        "type": "action_result",
                        "action": "release",
                        "seat_id": seat_id,
                        "success": True,
                        "message": "Seat released successfully",
                    },
                )
        else:
            # User does not have permission to release this seat
            await self.send_personal_message(
                websocket,
                {
                    "type": "action_result",
                    "action": "release",
                    "seat_id": seat_id,
                    "success": False,
                    "message": "You don't have permission to release this seat",
                },
            )

    async def _handle_extend(
        self, websocket: WebSocket, showtime_id: str, user_id: str, seat_id: str
    ):
        """
        Attempt to extend the reservation time for a seat. Only the user who reserved the seat can extend it.
        Notify the requester of the result (success or failure).

        Args:
            websocket: The WebSocket connection of the requesting user.
            showtime_id: The showtime identifier.
            user_id: The user attempting to extend the reservation.
            seat_id: The seat to extend.
        """
        reserved_by = await self._redis_service.get_seat_reservation(
            showtime_id, seat_id
        )
        if reserved_by == user_id:
            # User is allowed to extend the reservation
            success = await self._redis_service.extend_reservation(
                showtime_id, seat_id, ttl=900
            )
            await self.send_personal_message(
                websocket,
                {
                    "type": "action_result",
                    "action": "extend",
                    "seat_id": seat_id,
                    "success": success,
                    "message": (
                        "Reservation extended" if success else "Failed to extend"
                    ),
                },
            )
        else:
            # User does not have permission to extend this reservation
            await self.send_personal_message(
                websocket,
                {
                    "type": "action_result",
                    "action": "extend",
                    "seat_id": seat_id,
                    "success": False,
                    "message": "You don't have permission to extend this reservation",
                },
            )

    async def get_connection_count(self, showtime_id: str) -> int:
        """
        Get the number of active connections for a showtime.

        Args:
            showtime_id: The showtime ID

        Returns:
            int: Number of active connections
        """
        if showtime_id in self._active_connections:
            return len(self._active_connections[showtime_id])
        return 0

    async def notify_seat_purchased(
        self, showtime_id: str, seat_ids: list, user_id: str
    ):
        """
        Notify all clients that seats have been purchased.

        Args:
            showtime_id: The showtime ID
            seat_ids: List of purchased seat IDs
            user_id: The user who purchased
        """
        for seat_id in seat_ids:
            await self.broadcast_to_showtime(
                showtime_id,
                {
                    "type": "seat_update",
                    "seat_id": seat_id,
                    "status": "purchased",
                    "user_id": user_id,
                    "showtime_id": showtime_id,
                },
            )
