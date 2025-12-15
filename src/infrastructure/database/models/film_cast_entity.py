from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base


class FilmCastEntity(Base):
    """SQLAlchemy entity for Film_Cast junction table."""

    __tablename__ = "film_casts"

    film_id: Mapped[str] = mapped_column(
        String, ForeignKey("films.id"), primary_key=True
    )
    cast_id: Mapped[str] = mapped_column(
        String, ForeignKey("casts.id"), primary_key=True
    )
    role: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    character_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationships
    film: Mapped["FilmEntity"] = relationship(back_populates="film_casts")
    cast: Mapped["CastEntity"] = relationship(back_populates="film_casts")
