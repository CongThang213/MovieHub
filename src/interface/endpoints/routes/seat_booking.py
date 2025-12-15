from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from src.application.services.seat_booking_service import SeatBookingService
from src.containers import AppContainer
from src.infrastructure.services.redis_service import RedisService
from src.interface.endpoints.dependencies.auth_dependencies import get_current_user, TokenData
from src.interface.endpoints.schemas.seat_booking_schema import (
    SeatReservationRequest,
    SeatReleaseRequest,
    SeatExtendRequest,
    SeatPurchaseRequest,
    SeatReservationResponse,
    ShowtimeSeatStatusResponse,
    SeatStatusResponse,
)

router = APIRouter(prefix="/seat-booking", tags=["Seat Booking"])


def get_seat_booking_service(
    redis_service: RedisService = Depends(Provide[AppContainer.redis.redis_service]),
    websocket_manager=Depends(Provide[AppContainer.redis.websocket_manager]),
) -> SeatBookingService:
    """Dependency to get seat booking service."""
    return SeatBookingService(redis_service, websocket_manager)


@router.post(
    "/showtimes/{showtime_id}/reserve",
    response_model=SeatReservationResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def reserve_seats(
    showtime_id: str,
    request: SeatReservationRequest,
    current_user: TokenData = Depends(get_current_user),
    service: SeatBookingService = Depends(get_seat_booking_service),
):
    """
    Reserve seats for a showtime.

    Args:
        showtime_id: The showtime ID
        request: Seat reservation request
        current_user: The authenticated user
        service: Seat booking service

    Returns:
        Reservation results
    """
    results = await service.reserve_seats(
        showtime_id, request.seat_ids, current_user.user_id, request.ttl
    )

    success_count = sum(results.values())
    total_count = len(results)

    return SeatReservationResponse(
        showtime_id=showtime_id,
        results=results,
        success_count=success_count,
        total_count=total_count,
        message=f"Reserved {success_count}/{total_count} seats successfully",
    )


@router.post(
    "/showtimes/{showtime_id}/release",
    response_model=SeatReservationResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def release_seats(
    showtime_id: str,
    request: SeatReleaseRequest,
    current_user: TokenData = Depends(get_current_user),
    service: SeatBookingService = Depends(get_seat_booking_service),
):
    """
    Release reserved seats.

    Args:
        showtime_id: The showtime ID
        request: Seat release request
        current_user: The authenticated user
        service: Seat booking service

    Returns:
        Release results
    """
    results = await service.release_seats(
        showtime_id, request.seat_ids, current_user.user_id
    )

    success_count = sum(results.values())
    total_count = len(results)

    return SeatReservationResponse(
        showtime_id=showtime_id,
        results=results,
        success_count=success_count,
        total_count=total_count,
        message=f"Released {success_count}/{total_count} seats successfully",
    )


@router.post(
    "/showtimes/{showtime_id}/extend",
    response_model=SeatReservationResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def extend_reservations(
    showtime_id: str,
    request: SeatExtendRequest,
    current_user: TokenData = Depends(get_current_user),
    service: SeatBookingService = Depends(get_seat_booking_service),
):
    """
    Extend seat reservation time.

    Args:
        showtime_id: The showtime ID
        request: Seat extension request
        current_user: The authenticated user
        service: Seat booking service

    Returns:
        Extension results
    """
    results = await service.extend_reservation_time(
        showtime_id, request.seat_ids, current_user.user_id, request.ttl
    )

    success_count = sum(results.values())
    total_count = len(results)

    return SeatReservationResponse(
        showtime_id=showtime_id,
        results=results,
        success_count=success_count,
        total_count=total_count,
        message=f"Extended {success_count}/{total_count} reservations successfully",
    )


@router.post(
    "/showtimes/{showtime_id}/confirm-purchase",
    status_code=status.HTTP_200_OK,
)
@inject
async def confirm_seat_purchase(
    showtime_id: str,
    request: SeatPurchaseRequest,
    current_user: TokenData = Depends(get_current_user),
    service: SeatBookingService = Depends(get_seat_booking_service),
):
    """
    Confirm seat purchase after payment.

    Args:
        showtime_id: The showtime ID
        request: Seat purchase request
        current_user: The authenticated user
        service: Seat booking service

    Returns:
        Purchase confirmation
    """
    success = await service.confirm_purchase(
        showtime_id, request.seat_ids, current_user.user_id, request.booking_id
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to confirm purchase. Some seats may already be taken.",
        )

    return {
        "message": "Purchase confirmed successfully",
        "showtime_id": showtime_id,
        "seat_count": len(request.seat_ids),
        "booking_id": request.booking_id,
    }


@router.get(
    "/showtimes/{showtime_id}/seats/status",
    response_model=ShowtimeSeatStatusResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_showtime_seats_status(
    showtime_id: str,
    redis_service: RedisService = Depends(Provide[AppContainer.redis.redis_service]),
):
    """
    Get the status of all seats for a showtime.

    Args:
        showtime_id: The showtime ID
        redis_service: Redis service

    Returns:
        Seat status information
    """
    reserved_seats = await redis_service.get_all_reserved_seats(showtime_id)

    seats = []
    for seat_id, user_id in reserved_seats.items():
        ttl = await redis_service.get_seat_ttl(showtime_id, seat_id)
        seats.append(
            SeatStatusResponse(
                seat_id=seat_id,
                status="reserved",
                user_id=user_id,
                ttl=ttl,
            )
        )

    return ShowtimeSeatStatusResponse(showtime_id=showtime_id, seats=seats)


@router.get(
    "/showtimes/{showtime_id}/my-seats",
    status_code=status.HTTP_200_OK,
)
@inject
async def get_my_reserved_seats(
    showtime_id: str,
    current_user: TokenData = Depends(get_current_user),
    service: SeatBookingService = Depends(get_seat_booking_service),
):
    """
    Get seats reserved by the current user for a showtime.

    Args:
        showtime_id: The showtime ID
        current_user: The authenticated user
        service: Seat booking service

    Returns:
        User's reserved seats
    """
    seats = await service.get_user_reserved_seats(showtime_id, current_user.user_id)

    return {
        "showtime_id": showtime_id,
        "user_id": current_user.user_id,
        "reserved_seats": seats,
        "count": len(seats),
    }


@router.post(
    "/showtimes/{showtime_id}/check-availability",
    status_code=status.HTTP_200_OK,
)
@inject
async def check_seats_availability(
    showtime_id: str,
    seat_ids: list[str],
    service: SeatBookingService = Depends(get_seat_booking_service),
):
    """
    Check if specific seats are available.

    Args:
        showtime_id: The showtime ID
        seat_ids: List of seat IDs to check
        service: Seat booking service

    Returns:
        Availability status for each seat
    """
    availability = await service.check_seat_availability(showtime_id, seat_ids)

    return {
        "showtime_id": showtime_id,
        "availability": availability,
        "available_count": sum(availability.values()),
        "total_count": len(availability),
    }
