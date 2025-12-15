import json

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query

from config.logging_config import logger
from src.application.services.auth_service import AuthService
from src.containers import AppContainer
from src.infrastructure.services.redis_service import RedisService
from src.infrastructure.services.websocket_manager import WebsocketManager

router = APIRouter(prefix="/ws", tags=["WebSocket"])


@router.websocket("/seat-booking/{showtime_id}")
@inject
async def websocket_seat_booking(
    websocket: WebSocket,
    showtime_id: str,
    token: str = Query(...),
    manager: WebsocketManager = Depends(Provide[AppContainer.redis.websocket_manager]),
    auth_service: AuthService = Depends(
        Provide[AppContainer.firebase.firebase_auth_service]
    ),
):
    """
    WebSocket endpoint for real-time seat booking updates.

    Args:
        websocket: The WebSocket connection
        showtime_id: The showtime ID to subscribe to
        token: Authentication token passed as query parameter
        manager: The WebSocket connection manager
        auth_service: Authentication service for token validation

    Message Format:
        Client -> Server:
        {
            "action": "reserve" | "release" | "extend",
            "seat_id": "seat-uuid"
        }

        Server -> Client:
        {
            "type": "seat_update" | "action_result" | "error" | "initial_status",
            "seat_id": "seat-uuid",
            "status": "reserved" | "available" | "purchased",
            "user_id": "user-uuid" | null,
            "showtime_id": "showtime-uuid",
            "success": true | false,
            "message": "Status message"
        }
    """
    # Validate token and extract user_id
    try:
        decoded_token = await auth_service.validate_token(token)
        user_id = decoded_token.get("uid")

        if not user_id:
            await websocket.close(code=1008, reason="Invalid token: user ID not found")
            return

    except Exception as e:
        logger.error(f"WebSocket authentication failed: {e}")
        await websocket.close(code=1008, reason="Authentication failed")
        return

    await manager.connect(websocket, showtime_id, user_id)

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()

            try:
                message = json.loads(data)
                action = message.get("action")
                seat_id = message.get("seat_id")

                if not action or not seat_id:
                    await manager.send_personal_message(
                        websocket,
                        {
                            "type": "error",
                            "message": "Invalid message format. Required: action and seat_id",
                        },
                    )
                    continue

                # Handle the seat action
                await manager.handle_seat_action(
                    websocket, showtime_id, user_id, action, seat_id
                )

            except json.JSONDecodeError:
                await manager.send_personal_message(
                    websocket,
                    {
                        "type": "error",
                        "message": "Invalid JSON format",
                    },
                )

    except WebSocketDisconnect:
        await manager.disconnect(websocket, showtime_id)
        logger.info(f"User {user_id} disconnected from showtime {showtime_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await manager.disconnect(websocket, showtime_id)


@router.get("/seats/{showtime_id}/status")
@inject
async def get_showtime_seat_status(
    showtime_id: str,
    redis_service: RedisService = Depends(Provide[AppContainer.redis.redis_service]),
):
    """
    Get the current seat reservation status for a showtime.

    Args:
        showtime_id: The showtime ID
        redis_service: The Redis service

    Returns:
        Dictionary with reserved seats information
    """
    reserved_seats = await redis_service.get_all_reserved_seats(showtime_id)

    return {
        "showtime_id": showtime_id,
        "reserved_seats": [
            {
                "seat_id": seat_id,
                "user_id": user_id,
                "ttl": await redis_service.get_seat_ttl(showtime_id, seat_id),
            }
            for seat_id, user_id in reserved_seats.items()
        ],
    }


@router.get("/seats/{showtime_id}/connections")
@inject
async def get_active_connections(
    showtime_id: str,
    manager: WebsocketManager = Depends(Provide[AppContainer.redis.websocket_manager]),
):
    """
    Get the number of active WebSocket connections for a showtime.

    Args:
        showtime_id: The showtime ID
        manager: The WebSocket connection manager

    Returns:
        Dictionary with connection count
    """
    count = await manager.get_connection_count(showtime_id)
    return {
        "showtime_id": showtime_id,
        "active_connections": count,
    }
