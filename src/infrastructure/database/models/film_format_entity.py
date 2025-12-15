from typing import Optional, List

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base


class FilmFormatEntity(Base):
    """Database entity model for film formats."""

    __tablename__ = "film_formats"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True, unique=True)
    surcharge: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationships
    showtimes: Mapped[List["ShowTimeEntity"]] = relationship(
        "ShowTimeEntity", back_populates="film_format"
    )
