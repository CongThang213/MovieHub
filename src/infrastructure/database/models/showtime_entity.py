from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base


class ShowTimeEntity(Base):
    """SQLAlchemy entity for ShowTime table."""

    __tablename__ = "showtimes"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    hall_id: Mapped[str] = mapped_column(String, ForeignKey("halls.id"))
    film_id: Mapped[str] = mapped_column(String, ForeignKey("films.id"))
    film_format_id: Mapped[str] = mapped_column(String, ForeignKey("film_formats.id"))
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    available_seats: Mapped[Optional[int]] = mapped_column(nullable=True)

    # Relationships
    hall: Mapped["HallEntity"] = relationship("HallEntity", back_populates="showtimes")
    film: Mapped["FilmEntity"] = relationship("FilmEntity", back_populates="showtimes")
    film_format: Mapped["FilmFormatEntity"] = relationship(
        "FilmFormatEntity", back_populates="showtimes"
    )
    booking_seats: Mapped[List["BookingSeatEntity"]] = relationship(
        "BookingSeatEntity", back_populates="showtime"
    )
