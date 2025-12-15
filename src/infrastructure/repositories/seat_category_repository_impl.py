from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.exceptions.app_exception import DuplicateEntryException
from src.domain.exceptions.seat_category_exceptions import SeatCategoryNotFoundException
from src.domain.models.seat_category import SeatCategory
from src.domain.repositories.seat_category_repository import SeatCategoryRepository
from src.infrastructure.database.models.seat_category_entity import SeatCategoryEntity
from src.infrastructure.database.models.mappers.seat_category_entity_mappers import (
    SeatCategoryEntityMappers,
)


class SeatCategoryRepositoryImpl(SeatCategoryRepository):
    """Implementation of the seat category repository using SQLAlchemy."""

    async def create(
        self, seat_category: SeatCategory, session: AsyncSession
    ) -> SeatCategory:
        """Create a new seat category record.

        Args:
            seat_category: The seat category domain model to create
            session: The database session to use

        Returns:
            The created seat category domain model with ID populated
        """
        seat_category_entity = SeatCategoryEntityMappers.from_domain(seat_category)
        session.add(seat_category_entity)
        await session.flush()

        return SeatCategoryEntityMappers.to_domain(seat_category_entity)

    async def get_by_id(
        self, seat_category_id: str, session: AsyncSession
    ) -> Optional[SeatCategory]:
        """Get a seat category by its ID.

        Args:
            seat_category_id: The ID of the seat category to retrieve
            session: The database session to use

        Returns:
            The seat category domain model or None if not found
        """
        result = await session.execute(
            select(SeatCategoryEntity).where(SeatCategoryEntity.id == seat_category_id)
        )
        try:
            seat_category_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="SeatCategory", identifier=seat_category_id
            ) from e

        return (
            SeatCategoryEntityMappers.to_domain(seat_category_entity)
            if seat_category_entity
            else None
        )

    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[SeatCategory]:
        """Get all seat categories with pagination.

        Args:
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.

        Returns:
            A list of seat category domain models for the specified page
        """
        offset = (page - 1) * page_size
        result = await session.execute(
            select(SeatCategoryEntity).offset(offset).limit(page_size)
        )
        seat_category_entities = result.scalars().all()

        return SeatCategoryEntityMappers.to_domains(seat_category_entities)

    async def update(
        self, seat_category: SeatCategory, session: AsyncSession
    ) -> SeatCategory:
        """Update an existing seat category record.

        Args:
            seat_category: The seat category domain model to update
            session: The database session to use

        Returns:
            The updated seat category domain model

        Raises:
            SeatCategoryNotFoundException: If the seat category does not exist
        """
        result = await session.execute(
            select(SeatCategoryEntity).where(SeatCategoryEntity.id == seat_category.id)
        )
        seat_category_entity = result.scalar_one_or_none()

        if not seat_category_entity:
            raise SeatCategoryNotFoundException(seat_category.id)

        # Update entity attributes with the complete domain model
        seat_category_entity.name = seat_category.name
        seat_category_entity.base_price = seat_category.base_price
        seat_category_entity.attributes = seat_category.attributes

        await session.flush()

        return SeatCategoryEntityMappers.to_domain(seat_category_entity)

    async def delete(self, seat_category_id: str, session: AsyncSession) -> None:
        """Delete a seat category record.

        Args:
            seat_category_id: The ID of the seat category to delete
            session: The database session to use

        Raises:
            SeatCategoryNotFoundException: If the seat category does not exist
        """
        result = await session.execute(
            select(SeatCategoryEntity).where(SeatCategoryEntity.id == seat_category_id)
        )
        seat_category_entity = result.scalar_one_or_none()

        if not seat_category_entity:
            raise SeatCategoryNotFoundException(seat_category_id)

        await session.execute(
            delete(SeatCategoryEntity).where(SeatCategoryEntity.id == seat_category_id)
        )
        await session.flush()
