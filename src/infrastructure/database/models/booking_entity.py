from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base


class BookingEntity(Base):
    """SQLAlchemy entity for Booking table."""

    __tablename__ = "bookings"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    total_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    payment_method_id: Mapped[Optional[str]] = mapped_column(
        String, ForeignKey("payment_methods.id"), nullable=True
    )
    voucher_id: Mapped[Optional[str]] = mapped_column(
        String, ForeignKey("vouchers.id"), nullable=True
    )
    payment_reference: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationships
    user: Mapped["UserEntity"] = relationship("UserEntity", back_populates="bookings")
    payment_method: Mapped["PaymentMethodEntity"] = relationship(
        "PaymentMethodEntity", back_populates="bookings"
    )
    voucher: Mapped["VoucherEntity"] = relationship(
        "VoucherEntity", back_populates="bookings"
    )
    booking_seats: Mapped[List["BookingSeatEntity"]] = relationship(
        "BookingSeatEntity", back_populates="booking"
    )
    payments: Mapped[List["PaymentEntity"]] = relationship(
        "PaymentEntity", back_populates="booking"
    )
