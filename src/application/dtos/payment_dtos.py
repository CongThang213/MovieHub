from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.domain.enums.payment_status import PaymentStatus


class PaymentCreateDTO(BaseModel):
    """DTO for creating a payment"""

    booking_id: str
    payment_method_id: str
    amount: Optional[float] = None  # If None, use booking.total_price
    client_ip: str = "127.0.0.1"  # Client IP address for payment gateway


class PaymentResponseDTO(BaseModel):
    """DTO for payment response"""

    id: str
    booking_id: str
    payment_method_id: str
    external_txn_id: Optional[str]
    amount: float
    currency: str
    status: PaymentStatus
    created_at: datetime
    confirmed_at: Optional[datetime]
    payment_url: Optional[str] = None  # Generated dynamically, not persisted

    class Config:
        from_attributes = True

