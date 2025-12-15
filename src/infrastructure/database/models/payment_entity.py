from datetime import datetime
from typing import Optional

from sqlalchemy import String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base


class PaymentEntity(Base):
    """SQLAlchemy entity for Payment table."""

    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    booking_id: Mapped[str] = mapped_column(String, ForeignKey("bookings.id"))
    payment_method_id: Mapped[str] = mapped_column(
        String, ForeignKey("payment_methods.id")
    )
    external_txn_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    # currency: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    confirmed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    payment_metadata: Mapped[Optional[dict]] = mapped_column(
        "metadata", JSON, nullable=True
    )

    # Relationships
    booking: Mapped["BookingEntity"] = relationship(
        "BookingEntity", back_populates="payments"
    )
    payment_method: Mapped["PaymentMethodEntity"] = relationship(
        "PaymentMethodEntity", back_populates="payments"
    )
