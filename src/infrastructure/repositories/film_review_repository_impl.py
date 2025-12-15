from typing import Optional, List

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.enums.booking_status import BookingStatus
from src.domain.models.film_review import FilmReview
from src.domain.models.film_review_with_author import FilmReviewWithAuthor
from src.domain.repositories.film_review_repository import FilmReviewRepository
from src.infrastructure.database.models.booking_entity import BookingEntity
from src.infrastructure.database.models.booking_seat_entity import BookingSeatEntity
from src.infrastructure.database.models.film_review_entity import FilmReviewEntity
from src.infrastructure.database.models.user_entity import UserEntity
from src.infrastructure.database.models.mappers.film_review_entity_mappers import (
    FilmReviewEntityMappers,
)
from src.infrastructure.database.models.showtime_entity import ShowTimeEntity


class FilmReviewRepositoryImpl(FilmReviewRepository):
    """Implementation of FilmReviewRepository using SQLAlchemy."""

    async def get_by_id(
        self, review_id: str, session: AsyncSession
    ) -> Optional[FilmReview]:
        """Retrieve a film review by its ID."""
        result = await session.execute(
            select(FilmReviewEntity).where(FilmReviewEntity.id == review_id)
        )
        entity = result.scalar_one_or_none()
        return FilmReviewEntityMappers.to_domain(entity) if entity else None

    async def create(self, review: FilmReview, session: AsyncSession) -> FilmReview:
        """Create a new film review."""
        entity = FilmReviewEntityMappers.from_domain(review)
        session.add(entity)
        await session.flush()
        return FilmReviewEntityMappers.to_domain(entity)

    async def update(
        self, review_id: str, session: AsyncSession, **kwargs
    ) -> FilmReview:
        """Update an existing film review."""
        result = await session.execute(
            select(FilmReviewEntity).where(FilmReviewEntity.id == review_id)
        )
        entity = result.scalar_one_or_none()

        if entity:
            for key, value in kwargs.items():
                if hasattr(entity, key) and value is not None:
                    setattr(entity, key, value)
            await session.flush()

        return FilmReviewEntityMappers.to_domain(entity)

    async def delete(self, review_id: str, session: AsyncSession) -> None:
        """Delete a film review."""
        result = await session.execute(
            select(FilmReviewEntity).where(FilmReviewEntity.id == review_id)
        )
        entity = result.scalar_one_or_none()
        if entity:
            await session.delete(entity)
            await session.flush()

    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> List[FilmReview]:
        """Retrieve all film reviews with pagination."""
        offset = (page - 1) * page_size
        result = await session.execute(
            select(FilmReviewEntity)
            .options(
                selectinload(FilmReviewEntity.author).selectinload(UserEntity.image)
            )
            .order_by(FilmReviewEntity.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        entities = result.scalars().all()
        return FilmReviewEntityMappers.to_domains(entities)

    async def get_by_film_id(
        self,
        film_id: str,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> List[FilmReview]:
        """Retrieve all reviews for a specific film with pagination."""
        offset = (page - 1) * page_size
        result = await session.execute(
            select(FilmReviewEntity)
            .options(
                selectinload(FilmReviewEntity.author).selectinload(UserEntity.image)
            )
            .where(FilmReviewEntity.film_id == film_id)
            .order_by(FilmReviewEntity.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        entities = result.scalars().all()
        return FilmReviewEntityMappers.to_domains(entities)

    async def get_by_user_id(
        self,
        user_id: str,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> List[FilmReview]:
        """Retrieve all reviews by a specific user with pagination."""
        offset = (page - 1) * page_size
        result = await session.execute(
            select(FilmReviewEntity)
            .where(FilmReviewEntity.author_id == user_id)
            .order_by(FilmReviewEntity.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        entities = result.scalars().all()
        return FilmReviewEntityMappers.to_domains(entities)

    async def has_user_watched_film(
        self, user_id: str, film_id: str, session: AsyncSession
    ) -> bool:
        """
        Check if a user has watched a specific film by verifying if they have
        a paid booking for a showtime of that film.
        """
        result = await session.execute(
            select(BookingEntity)
            .join(BookingSeatEntity, BookingSeatEntity.booking_id == BookingEntity.id)
            .join(ShowTimeEntity, ShowTimeEntity.id == BookingSeatEntity.showtime_id)
            .where(
                and_(
                    BookingEntity.user_id == user_id,
                    ShowTimeEntity.film_id == film_id,
                    BookingEntity.status == BookingStatus.PAID,
                )
            )
            .limit(1)
        )
        entity = result.scalar_one_or_none()
        return entity is not None

    async def get_user_review_for_film(
        self, user_id: str, film_id: str, session: AsyncSession
    ) -> Optional[FilmReview]:
        """Get a user's review for a specific film if it exists."""
        result = await session.execute(
            select(FilmReviewEntity).where(
                and_(
                    FilmReviewEntity.author_id == user_id,
                    FilmReviewEntity.film_id == film_id,
                )
            )
        )
        entity = result.scalar_one_or_none()
        return FilmReviewEntityMappers.to_domain(entity) if entity else None

    async def get_by_film_id_with_author(
        self,
        film_id: str,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> List[FilmReviewWithAuthor]:
        """Retrieve all reviews for a specific film with author details and pagination."""
        offset = (page - 1) * page_size
        result = await session.execute(
            select(FilmReviewEntity)
            .options(
                selectinload(FilmReviewEntity.author).selectinload(UserEntity.image)
            )
            .where(FilmReviewEntity.film_id == film_id)
            .order_by(FilmReviewEntity.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        entities = result.scalars().all()
        return FilmReviewEntityMappers.to_domains_with_author(entities)

    async def get_all_with_author(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> List[FilmReviewWithAuthor]:
        """Retrieve all film reviews with author details and pagination."""
        offset = (page - 1) * page_size
        result = await session.execute(
            select(FilmReviewEntity)
            .options(
                selectinload(FilmReviewEntity.author).selectinload(UserEntity.image)
            )
            .order_by(FilmReviewEntity.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        entities = result.scalars().all()
        return FilmReviewEntityMappers.to_domains_with_author(entities)

    async def count_all(self, session: AsyncSession) -> int:
        """Count the total number of film reviews."""
        result = await session.execute(select(func.count(FilmReviewEntity.id)))
        return result.scalar() or 0

    async def count_by_film_id(self, film_id: str, session: AsyncSession) -> int:
        """Count the total number of reviews for a specific film."""
        result = await session.execute(
            select(func.count(FilmReviewEntity.id)).where(
                FilmReviewEntity.film_id == film_id
            )
        )
        return result.scalar() or 0
