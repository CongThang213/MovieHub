from typing import List

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base


class SeatRowEntity(Base):
    """SQLAlchemy entity for Seat_Row table."""

    __tablename__ = "seat_rows"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    hall_id: Mapped[str] = mapped_column(
        String, ForeignKey("halls.id", ondelete="CASCADE")
    )
    row_label: Mapped[str] = mapped_column(String(10), nullable=False)
    row_order: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    hall: Mapped["HallEntity"] = relationship(back_populates="seat_rows")
    seats: Mapped[List["SeatEntity"]] = relationship(
        back_populates="row", cascade="all, delete-orphan"
    )
