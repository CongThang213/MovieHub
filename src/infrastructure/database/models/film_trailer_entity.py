from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base


class FilmTrailerEntity(Base):
    """SQLAlchemy entity for Film_Trailer table."""

    __tablename__ = "film_trailers"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    film_id: Mapped[str] = mapped_column(String, ForeignKey("films.id"))
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    order_index: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Relationships
    film: Mapped["FilmEntity"] = relationship(back_populates="trailers")
