from typing import List

from sqlalchemy import String, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base


class SeatCategoryEntity(Base):
    """SQLAlchemy entity for Seat_Category table."""

    __tablename__ = "seat_categories"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    base_price: Mapped[float] = mapped_column(Float, nullable=False)
    attributes: Mapped[str] = mapped_column(Text, nullable=True)

    # Relationships
    seats: Mapped[List["SeatEntity"]] = relationship(back_populates="category")
