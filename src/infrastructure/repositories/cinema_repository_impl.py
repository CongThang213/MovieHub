from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.exceptions.app_exception import DuplicateEntryException
from src.domain.exceptions.cinema_exceptions import CinemaNotFoundException
from src.domain.models.cinema import Cinema
from src.domain.repositories.cinema_repository import CinemaRepository
from src.infrastructure.database.models.cinema_entity import CinemaEntity
from src.infrastructure.database.models.mappers.cinema_entity_mappers import (
    CinemaEntityMappers,
)


class CinemaRepositoryImpl(CinemaRepository):
    """Implementation of the cinema repository using SQLAlchemy."""

    async def create(self, cinema: Cinema, session: AsyncSession) -> Cinema:
        """Create a new cinema record.

        Args:
            cinema: The cinema domain model to create
            session: The database session to use

        Returns:
            The created cinema domain model with ID populated
        """
        cinema_entity = CinemaEntityMappers.from_domain(cinema)
        session.add(cinema_entity)
        await session.flush()

        return CinemaEntityMappers.to_domain(cinema_entity)

    async def get_by_id(
        self, cinema_id: str, session: AsyncSession
    ) -> Optional[Cinema]:
        """Get a cinema by its ID.

        Args:
            cinema_id: The ID of the cinema to retrieve
            session: The database session to use

        Returns:
            The cinema domain model or None if not found
        """
        result = await session.execute(
            select(CinemaEntity).where(CinemaEntity.id == cinema_id)
        )
        try:
            cinema_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="Cinema", identifier=cinema_id
            ) from e

        return CinemaEntityMappers.to_domain(cinema_entity) if cinema_entity else None

    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Cinema]:
        """Get all cinemas with pagination.

        Args:
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.

        Returns:
            A list of cinema domain models for the specified page
        """
        offset = (page - 1) * page_size
        result = await session.execute(
            select(CinemaEntity).offset(offset).limit(page_size)
        )
        cinema_entities = result.scalars().all()

        return CinemaEntityMappers.to_domains(cinema_entities)

    async def get_by_city_id(
        self,
        city_id: str,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Cinema]:
        """Get all cinemas in a specific city with pagination.

        Args:
            city_id: The ID of the city
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.

        Returns:
            A list of cinema domain models for the specified city and page
        """
        offset = (page - 1) * page_size
        result = await session.execute(
            select(CinemaEntity)
            .where(CinemaEntity.city_id == city_id)
            .offset(offset)
            .limit(page_size)
        )
        cinema_entities = result.scalars().all()

        return CinemaEntityMappers.to_domains(cinema_entities)

    async def update(self, cinema: Cinema, session: AsyncSession) -> Cinema:
        """Update an existing cinema record.

        Args:
            cinema: The cinema domain model with updated fields
            session: The database session to use

        Returns:
            The updated cinema domain model

        Raises:
            CinemaNotFoundException: If the cinema is not found
        """
        result = await session.execute(
            select(CinemaEntity).where(CinemaEntity.id == cinema.id)
        )
        cinema_entity = result.scalar_one_or_none()

        if not cinema_entity:
            raise CinemaNotFoundException(cinema.id)

        # Update fields
        cinema_entity.city_id = cinema.city_id
        cinema_entity.name = cinema.name
        cinema_entity.address = cinema.address
        cinema_entity.lat = cinema.lat
        cinema_entity.long = cinema.long
        cinema_entity.rating = cinema.rating

        await session.flush()

        return CinemaEntityMappers.to_domain(cinema_entity)

    async def delete(self, cinema_id: str, session: AsyncSession) -> bool:
        """Delete a cinema record.

        Args:
            cinema_id: The ID of the cinema to delete
            session: The database session to use

        Returns:
            True if the cinema was deleted, False otherwise
        """
        result = await session.execute(
            delete(CinemaEntity).where(CinemaEntity.id == cinema_id)
        )
        return result.rowcount > 0
