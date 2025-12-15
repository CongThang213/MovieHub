from dataclasses import dataclass
from typing import Optional


@dataclass
class TicketService:
    """
    Represents additional services attached to a specific booking seat/ticket.
    """

    booking_seat_id: Optional[str] = None
    service_id: Optional[str] = None
    count: int = 1

    def is_valid(self) -> bool:
        """
        Check if the ticket service has all required fields filled.

        Returns:
            bool: True if valid, False otherwise
        """
        return bool(self.booking_seat_id and self.service_id and self.count > 0)
