from typing import List, Optional, Dict

from config.logging_config import logger
from src.infrastructure.services.redis_service import RedisService
from src.infrastructure.services.websocket_manager import WebsocketManager


class SeatBookingService:
    """Service for handling seat booking operations with Redis and WebSocket."""

    def __init__(
        self,
        redis_service: RedisService,
        websocket_manager: WebsocketManager,
    ):
        """
        Initialize the seat booking service.

        Args:
            redis_service: Redis service for seat state management
            websocket_manager: WebSocket manager for real-time updates
        """
        self.redis_service = redis_service
        self.websocket_manager = websocket_manager

    async def reserve_seats(
        self, showtime_id: str, seat_ids: List[str], user_id: str, ttl: int = 900
    ) -> Dict[str, bool]:
        """
        Reserve multiple seats for a user.

        Args:
            showtime_id: The showtime ID
            seat_ids: List of seat IDs to reserve
            user_id: The user ID
            ttl: Time-to-live in seconds (default: 15 minutes)

        Returns:
            Dict[str, bool]: Mapping of seat_id to reservation success status
        """
        results = {}

        for seat_id in seat_ids:
            success = await self.redis_service.reserve_seat(
                showtime_id, seat_id, user_id, ttl
            )
            results[seat_id] = success

            if success:
                # Publish seat update
                await self.redis_service.publish_seat_update(
                    showtime_id, seat_id, "reserved", user_id
                )

                # Broadcast via WebSocket
                await self.websocket_manager.broadcast_to_showtime(
                    showtime_id,
                    {
                        "type": "seat_update",
                        "seat_id": seat_id,
                        "status": "reserved",
                        "user_id": user_id,
                        "showtime_id": showtime_id,
                    },
                )

        logger.info(
            f"Reserved {sum(results.values())}/{len(seat_ids)} seats for user {user_id}"
        )
        return results

    async def release_seats(
        self, showtime_id: str, seat_ids: List[str], user_id: Optional[str] = None
    ) -> Dict[str, bool]:
        """
        Release multiple seats.

        Args:
            showtime_id: The showtime ID
            seat_ids: List of seat IDs to release
            user_id: Optional user ID for permission check

        Returns:
            Dict[str, bool]: Mapping of seat_id to release success status
        """
        results = {}

        for seat_id in seat_ids:
            # Check permission if user_id is provided
            if user_id:
                reserved_by = await self.redis_service.get_seat_reservation(
                    showtime_id, seat_id
                )
                if reserved_by != user_id:
                    results[seat_id] = False
                    logger.warning(
                        f"User {user_id} attempted to release seat {seat_id} "
                        f"reserved by {reserved_by}"
                    )
                    continue

            success = await self.redis_service.release_seat(showtime_id, seat_id)
            results[seat_id] = success

            if success:
                # Publish seat update
                await self.redis_service.publish_seat_update(
                    showtime_id, seat_id, "available", None
                )

                # Broadcast via WebSocket
                await self.websocket_manager.broadcast_to_showtime(
                    showtime_id,
                    {
                        "type": "seat_update",
                        "seat_id": seat_id,
                        "status": "available",
                        "user_id": None,
                        "showtime_id": showtime_id,
                    },
                )

        logger.info(f"Released {sum(results.values())}/{len(seat_ids)} seats")
        return results

    async def confirm_purchase(
        self, showtime_id: str, seat_ids: List[str], user_id: str, booking_id: str
    ) -> bool:
        """
        Confirm seat purchase and update status.

        Args:
            showtime_id: The showtime ID
            seat_ids: List of purchased seat IDs
            user_id: The user ID
            booking_id: The booking ID

        Returns:
            bool: True if all seats confirmed successfully
        """
        try:
            # Lock seats for purchase
            locked = await self.redis_service.lock_seats_for_purchase(
                showtime_id, seat_ids, booking_id, ttl=300
            )

            if not locked:
                logger.error(f"Failed to lock seats for booking {booking_id}")
                return False

            # Release temporary reservations
            await self.release_seats(showtime_id, seat_ids)

            # Notify via WebSocket that seats are purchased
            await self.websocket_manager.notify_seat_purchased(
                showtime_id, seat_ids, user_id
            )

            # Publish purchase updates
            for seat_id in seat_ids:
                await self.redis_service.publish_seat_update(
                    showtime_id, seat_id, "purchased", user_id
                )

            # Unlock purchase locks after broadcasting
            await self.redis_service.unlock_seats_after_purchase(showtime_id, seat_ids)

            logger.info(
                f"Confirmed purchase of {len(seat_ids)} seats for booking {booking_id}"
            )
            return True

        except Exception as e:
            logger.error(f"Error confirming purchase: {e}")
            # Unlock seats on error
            await self.redis_service.unlock_seats_after_purchase(showtime_id, seat_ids)
            return False

    async def check_seat_availability(
        self, showtime_id: str, seat_ids: List[str]
    ) -> Dict[str, bool]:
        """
        Check if seats are available for reservation.

        Args:
            showtime_id: The showtime ID
            seat_ids: List of seat IDs to check

        Returns:
            Dict[str, bool]: Mapping of seat_id to availability (True if available)
        """
        results = {}

        for seat_id in seat_ids:
            reservation = await self.redis_service.get_seat_reservation(
                showtime_id, seat_id
            )
            results[seat_id] = reservation is None

        return results

    async def get_user_reserved_seats(
        self, showtime_id: str, user_id: str
    ) -> List[Dict[str, any]]:
        """
        Get all seats reserved by a specific user for a showtime.

        Args:
            showtime_id: The showtime ID
            user_id: The user ID

        Returns:
            List of seat information dictionaries
        """
        all_reserved = await self.redis_service.get_all_reserved_seats(showtime_id)

        user_seats = []
        for seat_id, reserved_user_id in all_reserved.items():
            if reserved_user_id == user_id:
                ttl = await self.redis_service.get_seat_ttl(showtime_id, seat_id)
                user_seats.append(
                    {
                        "seat_id": seat_id,
                        "user_id": user_id,
                        "ttl": ttl,
                    }
                )

        return user_seats

    async def extend_reservation_time(
        self, showtime_id: str, seat_ids: List[str], user_id: str, ttl: int = 900
    ) -> Dict[str, bool]:
        """
        Extend reservation time for multiple seats.

        Args:
            showtime_id: The showtime ID
            seat_ids: List of seat IDs
            user_id: The user ID (for permission check)
            ttl: New time-to-live in seconds

        Returns:
            Dict[str, bool]: Mapping of seat_id to extension success status
        """
        results = {}

        for seat_id in seat_ids:
            # Check permission
            reserved_by = await self.redis_service.get_seat_reservation(
                showtime_id, seat_id
            )

            if reserved_by != user_id:
                results[seat_id] = False
                continue

            success = await self.redis_service.extend_reservation(
                showtime_id, seat_id, ttl
            )
            results[seat_id] = success

        logger.info(
            f"Extended {sum(results.values())}/{len(seat_ids)} reservations for user {user_id}"
        )
        return results
