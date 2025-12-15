from typing import List

from sqlalchemy import String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base
from src.infrastructure.database.models.booking_entity import BookingEntity
from src.infrastructure.database.models.payment_entity import PaymentEntity


class PaymentMethodEntity(Base):
    """SQLAlchemy entity for Payment_Method table."""

    __tablename__ = "payment_methods"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    surcharge: Mapped[float] = mapped_column(Float, default=0)

    # Relationships
    bookings: Mapped[List["BookingEntity"]] = relationship(
        back_populates="payment_method"
    )
    payments: Mapped[List["PaymentEntity"]] = relationship(
        back_populates="payment_method"
    )
