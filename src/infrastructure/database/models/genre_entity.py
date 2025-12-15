from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base


class GenreEntity(Base):
    """SQLAlchemy entity for Genre table."""

    __tablename__ = "genres"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    # Relationships
    film_genres: Mapped[List["FilmGenreEntity"]] = relationship(
        "FilmGenreEntity", back_populates="genre"
    )
