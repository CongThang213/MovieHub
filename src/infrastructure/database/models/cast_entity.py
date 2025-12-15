from datetime import date
from typing import Optional, List

from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.init_database import Base


class CastEntity(Base):
    """SQLAlchemy model for the Cast entity."""

    __tablename__ = "casts"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    biography: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationships
    film_casts: Mapped[List["FilmCastEntity"]] = relationship(back_populates="cast")
    image: Mapped["ImageEntity"] = relationship(
        "ImageEntity",
        primaryjoin="CastEntity.id == foreign(ImageEntity.owner_id)",
        viewonly=True,
    )
