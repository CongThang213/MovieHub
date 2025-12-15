import enum


class SeatStatus(str, enum.Enum):
    """Status of a seat booking"""

    AVAILABLE = "available"  # Seat is available for booking
    RESERVED = "reserved"  # Seat is temporarily reserved but not paid
    PURCHASED = "purchased"  # Seat has been purchased and confirmed
    CANCELLED = "cancelled"  # Reservation was cancelled
    CHECKED_IN = "checked_in"  # Customer has checked in for this seat
