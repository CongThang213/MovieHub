from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, Float, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base
from src.infrastructure.database.models.booking_entity import BookingEntity


class VoucherEntity(Base):
    """SQLAlchemy entity for Voucher table."""

    __tablename__ = "vouchers"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    code: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    discount_rate: Mapped[float] = mapped_column(Float, nullable=False)
    valid_from: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    valid_until: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    max_usage: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    used_count: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    bookings: Mapped[List["BookingEntity"]] = relationship(back_populates="voucher")
