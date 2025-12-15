from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.enums.promotion_type import PromotionType
from src.infrastructure.database.init_database import Base
from src.infrastructure.database.models.film_entity import FilmEntity


class FilmPromotionEntity(Base):
    """SQLAlchemy entity for Film_Promotions table."""

    __tablename__ = "film_promotions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    film_id: Mapped[str] = mapped_column(String, ForeignKey("films.id"))
    type: Mapped[Optional[PromotionType]] = mapped_column(
        nullable=False,
        type_=Enum(PromotionType, native_enum=False),
        default=PromotionType.FEATURED,
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    valid_from: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    valid_until: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    film: Mapped["FilmEntity"] = relationship(back_populates="promotions")
