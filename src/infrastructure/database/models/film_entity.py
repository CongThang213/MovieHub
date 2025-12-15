from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, Text, Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base


class FilmEntity(Base):
    """SQLAlchemy entity for Film table."""

    __tablename__ = "films"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    votes: Mapped[int] = mapped_column(Integer, default=0)
    rating: Mapped[Optional[float]] = mapped_column(Float, default=0)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    movie_begin_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )
    movie_end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    trailers: Mapped[List["FilmTrailerEntity"]] = relationship(back_populates="film")
    showtimes: Mapped[List["ShowTimeEntity"]] = relationship(back_populates="film")
    film_genres: Mapped[List["FilmGenreEntity"]] = relationship(back_populates="film")
    film_casts: Mapped[List["FilmCastEntity"]] = relationship(back_populates="film")
    reviews: Mapped[List["FilmReviewEntity"]] = relationship(back_populates="film")
    promotions: Mapped[List["FilmPromotionEntity"]] = relationship(
        back_populates="film"
    )
    images: Mapped[List["ImageEntity"]] = relationship(
        "ImageEntity",
        primaryjoin="FilmEntity.id == foreign(ImageEntity.owner_id)",
        viewonly=True,
    )
