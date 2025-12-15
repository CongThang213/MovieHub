from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base


class TicketServiceEntity(Base):
    """SQLAlchemy entity for Ticket_Services junction table."""

    __tablename__ = "ticket_services"

    booking_seat_id: Mapped[str] = mapped_column(
        String, ForeignKey("booking_seats.id"), primary_key=True
    )
    service_id: Mapped[str] = mapped_column(
        String, ForeignKey("services.id"), primary_key=True
    )
    count: Mapped[int] = mapped_column(Integer, default=1)

    # Relationships
    booking_seat: Mapped["BookingSeatEntity"] = relationship(
        back_populates="ticket_services"
    )
    service: Mapped["ServiceEntity"] = relationship(back_populates="ticket_services")
