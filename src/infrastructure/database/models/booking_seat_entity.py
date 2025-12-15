from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base


class BookingSeatEntity(Base):
    """SQLAlchemy entity for Booking_Seat table."""

    __tablename__ = "booking_seats"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    booking_id: Mapped[str] = mapped_column(String, ForeignKey("bookings.id"))
    showtime_id: Mapped[str] = mapped_column(String, ForeignKey("showtimes.id"))
    seat_id: Mapped[str] = mapped_column(String, ForeignKey("seats.id"))
    purchased_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    ticket_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationships
    booking: Mapped["BookingEntity"] = relationship(
        "BookingEntity", back_populates="booking_seats"
    )
    showtime: Mapped["ShowTimeEntity"] = relationship(
        "ShowTimeEntity", back_populates="booking_seats"
    )
    seat: Mapped["SeatEntity"] = relationship(
        "SeatEntity", back_populates="booking_seats"
    )
    ticket_services: Mapped[List["TicketServiceEntity"]] = relationship(
        "TicketServiceEntity", back_populates="booking_seat"
    )
