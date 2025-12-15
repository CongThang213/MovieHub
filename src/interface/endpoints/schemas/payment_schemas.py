from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.domain.enums.payment_status import PaymentStatus


class CreatePaymentRequest(BaseModel):
    """Request schema for creating a payment"""

    payment_method_id: str = Field(..., description="ID of the payment method to use")


class PaymentResponse(BaseModel):
    """Response schema for payment"""

    id: str
    booking_id: str
    payment_method_id: str
    external_txn_id: Optional[str] = None
    amount: float
    currency: str
    status: PaymentStatus
    created_at: datetime
    confirmed_at: Optional[datetime] = None
    payment_url: Optional[str] = Field(
        None, description="URL to redirect user for payment (generated dynamically)"
    )

    class Config:
        from_attributes = True
