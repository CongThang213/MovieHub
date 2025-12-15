from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from src.domain.enums.booking_status import BookingStatus


class BookingSeatCreateDTO(BaseModel):
    seat_id: str


class BookingCreateDTO(BaseModel):
    user_id: str
    showtime_id: str
    booking_seats: List[BookingSeatCreateDTO]
    payment_method_id: Optional[str] = None
    voucher_id: Optional[str] = None


class BookingSeatResponseDTO(BaseModel):
    id: str
    booking_id: str
    showtime_id: str
    seat_id: str
    purchased_at: Optional[datetime]
    ticket_code: Optional[str]

    class Config:
        from_attributes = True


class BookingResponseDTO(BaseModel):
    id: str
    user_id: str
    status: BookingStatus
    created_at: datetime
    paid_at: Optional[datetime]
    total_price: float
    payment_method_id: Optional[str]
    voucher_id: Optional[str]
    payment_reference: Optional[str]
    booking_seats: List[BookingSeatResponseDTO] = []

    class Config:
        from_attributes = True


class BookingUpdateDTO(BaseModel):
    status: Optional[BookingStatus] = None
    paid_at: Optional[datetime] = None
    total_price: Optional[float] = None
    payment_method_id: Optional[str] = None
    voucher_id: Optional[str] = None
    payment_reference: Optional[str] = None
