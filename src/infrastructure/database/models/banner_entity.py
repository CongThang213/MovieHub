from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.database.init_database import Base


class BannerEntity(Base):
    """SQLAlchemy entity for Banner table."""

    __tablename__ = "banners"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    fallback_image: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    alt_text: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    subtitle: Mapped[str] = mapped_column(String, nullable=False)
    cta_label: Mapped[str] = mapped_column(String, nullable=False)
    target_type: Mapped[str] = mapped_column(String, nullable=False)
    target_id: Mapped[str] = mapped_column(String, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=0)
    start_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    aspect_ratio: Mapped[str] = mapped_column(String, default="9:14")
