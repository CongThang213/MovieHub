from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base


class FilmGenreEntity(Base):
    """SQLAlchemy entity for Film_Genres junction table."""

    __tablename__ = "film_genres"

    film_id: Mapped[str] = mapped_column(
        String, ForeignKey("films.id"), primary_key=True
    )
    genre_id: Mapped[str] = mapped_column(
        String, ForeignKey("genres.id"), primary_key=True
    )

    # Relationships
    film: Mapped["FilmEntity"] = relationship(
        "FilmEntity", back_populates="film_genres"
    )
    genre: Mapped["GenreEntity"] = relationship(
        "GenreEntity", back_populates="film_genres"
    )
