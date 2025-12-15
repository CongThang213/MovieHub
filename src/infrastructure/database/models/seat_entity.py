from typing import Optional, List

from sqlalchemy import String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base
from src.infrastructure.database.models.booking_seat_entity import BookingSeatEntity
from src.infrastructure.database.models.seat_category_entity import SeatCategoryEntity
from src.infrastructure.database.models.seat_row_entity import SeatRowEntity


class SeatEntity(Base):
    """SQLAlchemy entity for Seat table."""

    __tablename__ = "seats"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    row_id: Mapped[str] = mapped_column(
        String, ForeignKey("seat_rows.id", ondelete="CASCADE")
    )
    category_id: Mapped[str] = mapped_column(String, ForeignKey("seat_categories.id"))
    seat_number: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    pos_y: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_accessible: Mapped[bool] = mapped_column(Boolean, default=False)
    external_label: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Relationships
    row: Mapped["SeatRowEntity"] = relationship(back_populates="seats")
    category: Mapped["SeatCategoryEntity"] = relationship(back_populates="seats")
    booking_seats: Mapped[List["BookingSeatEntity"]] = relationship(
        back_populates="seat"
    )
