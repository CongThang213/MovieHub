from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4

from src.domain.enums.booking_status import BookingStatus


@dataclass
class Booking:
    """
    Represents a booking in the system, which can contain multiple seats reserved or purchased.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    user_id: Optional[str] = None
    status: BookingStatus = BookingStatus.CREATED
    created_at: datetime = field(default_factory=datetime.now)
    paid_at: Optional[datetime] = None
    total_price: float = 0.0
    payment_method_id: Optional[str] = None
    voucher_id: Optional[str] = None
    payment_reference: Optional[str] = None

    def update_status(self, new_status: BookingStatus) -> None:
        """
        Update the booking status and set paid_at timestamp if the booking is being paid.

        Args:
            new_status: The new status to set for this booking
        """
        self.status = new_status
        if new_status == BookingStatus.PAID and not self.paid_at:
            self.paid_at = datetime.now()

    def apply_voucher(self, voucher_id: str) -> None:
        """
        Apply a voucher to this booking.

        Args:
            voucher_id: The ID of the voucher to apply
        """
        self.voucher_id = voucher_id

    def is_paid(self) -> bool:
        """
        Check if the booking has been paid.

        Returns:
            bool: True if paid, False otherwise
        """
        return self.status == BookingStatus.PAID
