from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.enums.image_type import ImageType
from src.infrastructure.database.init_database import Base


class ImageEntity(Base):
    """SQLAlchemy entity for Image table."""

    __tablename__ = "images"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    owner_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    type: Mapped[ImageType] = mapped_column(Enum(ImageType), nullable=False)
    public_id: Mapped[str] = mapped_column(String, nullable=False)
    is_temp: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
