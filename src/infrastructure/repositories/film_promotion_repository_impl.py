from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.exceptions.app_exception import DuplicateEntryException
from src.domain.exceptions.film_promotion_exceptions import (
    FilmPromotionNotFoundException,
)
from src.domain.models.film_promotion import FilmPromotion
from src.domain.repositories.film_promotion_repository import FilmPromotionRepository
from src.infrastructure.database.models.film_promotion_entity import FilmPromotionEntity
from src.infrastructure.database.models.mappers.film_promotion_entity_mappers import (
    FilmPromotionEntityMappers,
)


class FilmPromotionRepositoryImpl(FilmPromotionRepository):
    async def create(
        self, promotion: FilmPromotion, session: AsyncSession
    ) -> FilmPromotion:
        """
        Create a new film promotion.

        Args:
            promotion: The film promotion to create
            session: The database session to use

        Returns:
            The created film promotion with ID
        """
        try:
            promotion_entity = FilmPromotionEntityMappers.from_domain(promotion)
            session.add(promotion_entity)
            await session.flush()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="FilmPromotion", identifier=promotion.id
            ) from e

        return FilmPromotionEntityMappers.to_domain(promotion_entity)

    async def get_by_id(
        self, promotion_id: str, session: AsyncSession
    ) -> Optional[FilmPromotion]:
        """
        Get a film promotion by its ID.

        Args:
            promotion_id: The ID of the promotion
            session: The database session to use

        Returns:
            The film promotion if found, None otherwise

        Raises:
            DuplicateEntryException: If multiple entries are found with the same ID
        """
        try:
            result = await session.execute(
                select(FilmPromotionEntity).where(
                    FilmPromotionEntity.id == promotion_id
                )
            )
            promotion_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="FilmPromotion", identifier=promotion_id
            ) from e

        return (
            FilmPromotionEntityMappers.to_domain(promotion_entity)
            if promotion_entity
            else None
        )

    async def get_by_film_id(
        self, film_id: str, session: AsyncSession
    ) -> List[FilmPromotion]:
        """
        Get all promotions for a specific film.

        Args:
            film_id: The ID of the film
            session: The database session to use

        Returns:
            List of film promotions associated with the film
        """
        result = await session.execute(
            select(FilmPromotionEntity).where(FilmPromotionEntity.film_id == film_id)
        )
        promotion_entities = result.scalars().all()
        return [
            FilmPromotionEntityMappers.to_domain(pe)
            for pe in promotion_entities
            if pe is not None
        ]

    async def delete(self, promotion_id: str, session: AsyncSession) -> None:
        """
        Delete a film promotion by its ID.

        Args:
            promotion_id: The ID of the promotion to delete
            session: The database session to use

        Raises:
            FilmPromotionNotFoundException: If the promotion with the given ID is not found
            DuplicateEntryException: If multiple entries are found with the same ID
        """
        try:
            result = await session.execute(
                select(FilmPromotionEntity).where(
                    FilmPromotionEntity.id == promotion_id
                )
            )
            promotion_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="FilmPromotion", identifier=promotion_id
            ) from e

        if not promotion_entity:
            raise FilmPromotionNotFoundException(promotion_id=promotion_id)

        await session.delete(promotion_entity)
        await session.flush()

    async def update(
        self, promotion_id: str, session: AsyncSession, **kwargs
    ) -> FilmPromotion:
        """
        Update a film promotion by its ID.

        Args:
            promotion_id: The ID of the promotion to update
            session: The database session to use
            **kwargs: Fields to update

        Keyword Args:
            title (str): New title for the promotion (Optional)
            content (str): New content for the promotion (Optional)
            valid_from (datetime): New valid_from date (Optional)
            valid_until (datetime): New valid_until date (Optional)
            type (str): New type for the promotion (Optional)

        Returns:
            The updated film promotion

        Raises:
            FilmPromotionNotFoundException: If the promotion with the given ID is not found
            DuplicateEntryException: If multiple entries are found with the same ID
        """
        try:
            result = await session.execute(
                select(FilmPromotionEntity).where(
                    FilmPromotionEntity.id == promotion_id
                )
            )
            promotion_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="FilmPromotion", identifier=promotion_id
            ) from e

        if not promotion_entity:
            raise FilmPromotionNotFoundException(promotion_id=promotion_id)

        for attr, value in kwargs.items():
            if value is not None and hasattr(promotion_entity, attr):
                setattr(promotion_entity, attr, value)

        await session.flush()

        return FilmPromotionEntityMappers.to_domain(promotion_entity)
