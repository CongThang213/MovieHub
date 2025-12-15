from typing import List, Optional

from pydantic import BaseModel, Field


class SeatReservationRequest(BaseModel):
    """Request model for reserving seats."""

    seat_ids: List[str] = Field(..., description="List of seat IDs to reserve")
    ttl: Optional[int] = Field(
        900, description="Time-to-live in seconds (default: 15 minutes)"
    )


class SeatReleaseRequest(BaseModel):
    """Request model for releasing seats."""

    seat_ids: List[str] = Field(..., description="List of seat IDs to release")


class SeatExtendRequest(BaseModel):
    """Request model for extending seat reservations."""

    seat_ids: List[str] = Field(..., description="List of seat IDs to extend")
    ttl: Optional[int] = Field(900, description="New time-to-live in seconds")


class SeatPurchaseRequest(BaseModel):
    """Request model for confirming seat purchase."""

    seat_ids: List[str] = Field(..., description="List of seat IDs purchased")
    booking_id: str = Field(..., description="The booking ID")


class SeatReservationResponse(BaseModel):
    """Response model for seat reservation operations."""

    showtime_id: str
    results: dict[str, bool]
    success_count: int
    total_count: int
    message: str


class SeatStatusResponse(BaseModel):
    """Response model for seat status."""

    seat_id: str
    status: str  # available, reserved, purchased
    user_id: Optional[str] = None
    ttl: Optional[int] = None


class ShowtimeSeatStatusResponse(BaseModel):
    """Response model for showtime seat status."""

    showtime_id: str
    seats: List[SeatStatusResponse]
