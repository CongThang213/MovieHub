from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base


class FilmReviewEntity(Base):
    """SQLAlchemy entity for Film_Review table."""

    __tablename__ = "film_reviews"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    film_id: Mapped[str] = mapped_column(String, ForeignKey("films.id"))
    author_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    rating: Mapped[int] = mapped_column(Integer)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Relationships
    film: Mapped["FilmEntity"] = relationship("FilmEntity", back_populates="reviews")
    author: Mapped["UserEntity"] = relationship("UserEntity", back_populates="reviews")
