from typing import Optional, List

from sqlalchemy import String, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base
from src.infrastructure.database.models.ticket_service_entity import TicketServiceEntity


class ServiceEntity(Base):
    """SQLAlchemy entity for Service table."""

    __tablename__ = "services"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    detail: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # image_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    ticket_services: Mapped[List["TicketServiceEntity"]] = relationship(
        back_populates="service"
    )
    image: Mapped["ImageEntity"] = relationship(
        "ImageEntity",
        primaryjoin="ServiceEntity.id == foreign(ImageEntity.owner_id)",
        viewonly=True,
    )
