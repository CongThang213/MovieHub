from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.exceptions.app_exception import DuplicateEntryException
from src.domain.exceptions.film_format_exceptions import FilmFormatNotFoundException
from src.domain.models.flim_format import FilmFormat
from src.domain.repositories.film_format_repository import FilmFormatRepository
from src.infrastructure.database.models.film_format_entity import FilmFormatEntity
from src.infrastructure.database.models.mappers.film_format_entity_mappers import (
    FilmFormatEntityMappers,
)


class FilmFormatRepositoryImpl(FilmFormatRepository):
    """Implementation of the film format repository using SQLAlchemy."""

    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self._sessionmaker = sessionmaker

    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[FilmFormat]:
        """Get all film formats with pagination.

        Args:
            session: The database session to use
            page: The page number (1-based)
            page_size: The number of records per page

        Returns:
            A list of film format domain models for the specified page
        """
        offset = (page - 1) * page_size

        result = await session.execute(
            select(FilmFormatEntity).offset(offset).limit(page_size)
        )
        format_entities = result.scalars().all()

        return FilmFormatEntityMappers.to_domains(format_entities)

    async def get_by_id(
        self, format_id: str, session: AsyncSession
    ) -> Optional[FilmFormat]:
        """Get a film format by its ID.

        Args:
            format_id: The ID of the film format to retrieve
            session: The database session to use

        Returns:
            The film format domain model or None if not found

        Raises:
            DuplicateEntryException: If multiple film formats with the same ID are found
        """
        result = await session.execute(
            select(FilmFormatEntity).where(FilmFormatEntity.id == format_id)
        )
        try:
            format_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="FilmFormat", identifier=format_id
            ) from e

        return (
            FilmFormatEntityMappers.to_domain(format_entity) if format_entity else None
        )

    async def create(
        self, film_format: FilmFormat, session: AsyncSession
    ) -> FilmFormat:
        """Create a new film format record.

        Args:
            film_format: The film format domain model to create
            session: The database session to use

        Returns:
            The created film format domain model with ID populated

        Raises:
            DuplicateEntryException: If a film format with the same ID already exists
        """
        try:
            format_entity = FilmFormatEntityMappers.from_domain(film_format)
            session.add(format_entity)
            await session.flush()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="FilmFormat", identifier=film_format.id
            ) from e

        return FilmFormatEntityMappers.to_domain(format_entity)

    async def update(
        self, format_id: str, session: AsyncSession, **kwargs
    ) -> FilmFormat:
        """Update an existing film format record.

        Args:
            format_id: The ID of the film format to update
            session: The database session to use
            kwargs: Fields to update with their new values

        Keyword Args:
            name: New name for the film format (optional)
            description: New description for the film format (optional)
            surcharge: New surcharge for the film format (optional)

        Returns:
            The updated film format domain model

        Raises:
            FilmFormatNotFoundException: If the film format with the given ID does not exist
            DuplicateEntryException: If multiple film formats with the same ID are found
        """
        result = await session.execute(
            select(FilmFormatEntity).where(FilmFormatEntity.id == format_id)
        )
        try:
            format_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="FilmFormat", identifier=format_id
            ) from e

        if not format_entity:
            raise FilmFormatNotFoundException(format_id=format_id)

        for attr, value in kwargs.items():
            if value is not None and hasattr(format_entity, attr):
                setattr(format_entity, attr, value)

        await session.flush()

        return FilmFormatEntityMappers.to_domain(format_entity)

    async def delete(self, format_id: str, session: AsyncSession) -> None:
        """Delete a film format record.

        Args:
            format_id: The ID of the film format to delete
            session: The database session to use

        Raises:
            FilmFormatNotFoundException: If film format with given ID is not found
            DuplicateEntryException: If multiple film formats with the same ID are found
        """
        result = await session.execute(
            select(FilmFormatEntity).where(FilmFormatEntity.id == format_id)
        )
        try:
            format_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="FilmFormat", identifier=format_id
            ) from e

        if not format_entity:
            raise FilmFormatNotFoundException(format_id=format_id)

        await session.delete(format_entity)
