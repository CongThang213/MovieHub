from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class BookingSeat:
    """
    Represents a seat reserved or purchased as part of a booking.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    booking_id: Optional[str] = None
    showtime_id: Optional[str] = None
    seat_id: Optional[str] = None
    purchased_at: Optional[datetime] = None
    ticket_code: Optional[str] = None

    @staticmethod
    def generate_ticket_code() -> str:
        """
        Generate a secure, unique ticket code.

        Returns:
            str: A unique ticket code
        """
        import secrets
        import string

        alphabet = string.ascii_uppercase + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(10))
