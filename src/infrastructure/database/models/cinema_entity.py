from typing import Optional, List

from sqlalchemy import String, Text, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base


class CinemaEntity(Base):
    """SQLAlchemy entity for Cinema table."""

    __tablename__ = "cinemas"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    city_id: Mapped[str] = mapped_column(String, ForeignKey("cities.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    lat: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    long: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Relationships
    city: Mapped["CityEntity"] = relationship(back_populates="cinemas")
    halls: Mapped[List["HallEntity"]] = relationship(back_populates="cinema")
