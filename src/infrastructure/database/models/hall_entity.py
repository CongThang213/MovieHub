from typing import Optional, List

from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base
from src.infrastructure.database.models.cinema_entity import CinemaEntity
from src.infrastructure.database.models.seat_row_entity import SeatRowEntity
from src.infrastructure.database.models.showtime_entity import ShowTimeEntity


class HallEntity(Base):
    """SQLAlchemy entity for Hall table."""

    __tablename__ = "halls"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    cinema_id: Mapped[str] = mapped_column(String, ForeignKey("cinemas.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    cinema: Mapped["CinemaEntity"] = relationship(back_populates="halls")
    seat_rows: Mapped[List["SeatRowEntity"]] = relationship(
        back_populates="hall", cascade="all, delete-orphan"
    )
    showtimes: Mapped[List["ShowTimeEntity"]] = relationship(back_populates="hall")
