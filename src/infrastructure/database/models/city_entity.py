from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base
from src.infrastructure.database.models.cinema_entity import CinemaEntity


class CityEntity(Base):
    """SQLAlchemy entity for City table."""

    __tablename__ = "cities"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)

    # Relationships
    cinemas: Mapped[List["CinemaEntity"]] = relationship(back_populates="city")
