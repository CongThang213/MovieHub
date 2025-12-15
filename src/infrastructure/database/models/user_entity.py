from datetime import datetime, date
from typing import Optional, List

from sqlalchemy import DateTime, Date, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.enums.account_type import AccountType
from src.infrastructure.database.init_database import Base


class UserEntity(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    account_type: Mapped[AccountType] = mapped_column(
        nullable=False,
        type_=Enum(AccountType, native_enum=False),
        default=AccountType.CUSTOMER,
    )
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )

    # Relationships
    bookings: Mapped[List["BookingEntity"]] = relationship(
        "BookingEntity", back_populates="user"
    )
    reviews: Mapped[List["FilmReviewEntity"]] = relationship(
        "FilmReviewEntity", back_populates="author"
    )
    image: Mapped["ImageEntity"] = relationship(
        "ImageEntity",
        primaryjoin="UserEntity.id == foreign(ImageEntity.owner_id)",
        viewonly=True,
    )
