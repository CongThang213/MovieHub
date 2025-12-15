from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.exceptions.app_exception import DuplicateEntryException
from src.domain.exceptions.hall_exceptions import HallNotFoundException
from src.domain.models.hall import Hall
from src.domain.repositories.hall_repository import HallRepository
from src.infrastructure.database.models.hall_entity import HallEntity
from src.infrastructure.database.models.mappers.hall_entity_mappers import (
    HallEntityMappers,
)


class HallRepositoryImpl(HallRepository):
    """Implementation of the hall repository using SQLAlchemy."""

    async def create(self, hall: Hall, session: AsyncSession) -> Hall:
        """Create a new hall record.

        Args:
            hall: The hall domain model to create
            session: The database session to use

        Returns:
            The created hall domain model with ID populated
        """
        hall_entity = HallEntityMappers.from_domain(hall)
        session.add(hall_entity)
        await session.flush()

        return HallEntityMappers.to_domain(hall_entity)

    async def get_by_id(self, hall_id: str, session: AsyncSession) -> Optional[Hall]:
        """Get a hall by its ID.

        Args:
            hall_id: The ID of the hall to retrieve
            session: The database session to use

        Returns:
            The hall domain model or None if not found
        """
        result = await session.execute(
            select(HallEntity).where(HallEntity.id == hall_id)
        )
        try:
            hall_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(entry_type="Hall", identifier=hall_id) from e

        return HallEntityMappers.to_domain(hall_entity) if hall_entity else None

    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Hall]:
        """Get all halls with pagination.

        Args:
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.

        Returns:
            A list of hall domain models for the specified page
        """
        offset = (page - 1) * page_size
        result = await session.execute(
            select(HallEntity).offset(offset).limit(page_size)
        )
        hall_entities = result.scalars().all()

        return HallEntityMappers.to_domains(hall_entities)

    async def get_by_cinema_id(
        self,
        cinema_id: str,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Hall]:
        """Get all halls in a specific cinema with pagination.

        Args:
            cinema_id: The ID of the cinema
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.

        Returns:
            A list of hall domain models for the specified cinema and page
        """
        offset = (page - 1) * page_size
        result = await session.execute(
            select(HallEntity)
            .where(HallEntity.cinema_id == cinema_id)
            .offset(offset)
            .limit(page_size)
        )
        hall_entities = result.scalars().all()

        return HallEntityMappers.to_domains(hall_entities)

    async def update(self, hall: Hall, session: AsyncSession) -> Hall:
        """Update an existing hall record.

        Args:
            hall: The hall domain model with updated fields
            session: The database session to use

        Returns:
            The updated hall domain model

        Raises:
            HallNotFoundException: If the hall doesn't exist
        """
        result = await session.execute(
            select(HallEntity).where(HallEntity.id == hall.id)
        )
        hall_entity = result.scalar_one_or_none()

        if not hall_entity:
            raise HallNotFoundException(hall.id)

        # Update fields
        if hall.cinema_id:
            hall_entity.cinema_id = hall.cinema_id
        if hall.name:
            hall_entity.name = hall.name
        if hall.capacity is not None:
            hall_entity.capacity = hall.capacity
        if hall.description is not None:
            hall_entity.description = hall.description

        await session.flush()
        return HallEntityMappers.to_domain(hall_entity)

    async def delete(self, hall_id: str, session: AsyncSession) -> bool:
        """Delete a hall record.

        Args:
            hall_id: The ID of the hall to delete
            session: The database session to use

        Returns:
            True if deletion was successful

        Raises:
            HallNotFoundException: If the hall doesn't exist
        """
        result = await session.execute(
            select(HallEntity).where(HallEntity.id == hall_id)
        )
        hall_entity = result.scalar_one_or_none()

        if not hall_entity:
            raise HallNotFoundException(hall_id)

        await session.execute(delete(HallEntity).where(HallEntity.id == hall_id))
        await session.flush()
        return True
