from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.exc import MultipleResultsFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.exceptions.app_exception import DuplicateEntryException
from src.domain.exceptions.genre_exceptions import GenreNotFoundException
from src.domain.models.genre import Genre
from src.domain.repositories.genre_repository import GenreRepository
from src.infrastructure.database.models.genre_entity import GenreEntity
from src.infrastructure.database.models.mappers.genre_entity_mappers import (
    GenreEntityMappers,
)


class GenreRepositoryImpl(GenreRepository):
    """Implementation of the genre repository using SQLAlchemy."""

    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self._sessionmaker = sessionmaker

    async def get_by_name(self, name: str, session: AsyncSession) -> Optional[Genre]:
        """Get a genre by its name.

        Args:
            name: The name of the genre to retrieve
            session: The database session to use

        Returns:
            The genre domain model or None if not found

        Raises:
            DuplicateEntryException: If multiple genres with the same name are found
        """
        result = await session.execute(
            select(GenreEntity).where(GenreEntity.name == name)
        )
        try:
            genre_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(entry_type="Genre", identifier=name) from e

        return GenreEntityMappers.to_domain(genre_entity) if genre_entity else None

    async def create(self, genre: Genre, session: AsyncSession) -> Genre:
        """Create a new genre record.

        Args:
            genre: The genre domain model to create
            session: The database session to use

        Returns:
            The created genre domain model with ID populated

        Raises:
            DuplicateEntryException: If a genre with the same name already exists
        """
        try:
            # Check if a genre with the same name already exists
            existing_genre = await self.get_by_name(genre.name, session)
            if existing_genre:
                raise DuplicateEntryException(entry_type="Genre", identifier=genre.name)

            genre_entity = GenreEntityMappers.from_domain(genre)
            session.add(genre_entity)  # Add the new genre entity to the session
            await session.flush()  # Flush to populate the ID

            return GenreEntityMappers.to_domain(genre_entity)

        except IntegrityError as e:
            if "ix_genres_name" in str(e) or "unique constraint" in str(e).lower():
                raise DuplicateEntryException(
                    entry_type="Genre", identifier=genre.name
                ) from e
            raise

    async def get_by_id(self, genre_id: str, session: AsyncSession) -> Optional[Genre]:
        """Get a genre by its ID.

        Args:
            genre_id: The ID of the genre to retrieve
            session: The database session to use

        Returns:
            The genre domain model or None if not found
        """
        result = await session.execute(
            select(GenreEntity).where(GenreEntity.id == genre_id)
        )
        # If there is more than one result, it raises an error.
        # If there is no result, scalar_one_or_none() returns None.
        try:
            genre_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="Genre", identifier=genre_id
            ) from e

        # Return the domain model if found, else None
        return GenreEntityMappers.to_domain(genre_entity) if genre_entity else None

    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> tuple[list[Genre], int]:
        """Get all genres with pagination and total count.

        Args:
            session: The database session to use
            page: The page number (1-based)
            page_size: The number of records per page

        Returns:
            A tuple of two elements:
            - A list of genre domain models for the specified page
            - The total count of genre records
        """
        offset = (page - 1) * page_size
        # Get paginated genres
        result = await session.execute(
            select(GenreEntity).offset(offset).limit(page_size)
        )
        genre_entities = result.scalars().all()
        genres = GenreEntityMappers.to_domains(genre_entities)
        # Get total count
        count_result = await session.execute(
            select(func.count()).select_from(GenreEntity)
        )
        total_items = count_result.scalar()
        return genres, total_items

    async def update(self, genre_id: str, session: AsyncSession, **kwargs) -> Genre:
        """Update an existing genre record.

        Args:
            genre_id: The ID of the genre to update
            session: The database session to use
            kwargs: Fields to update with their new values

        Keyword Args:
            name: New name for the genre (optional)

        Returns:
            The updated genre domain model

        Raises:
            GenreNotFoundException: If the genre with the given ID does not exist
            DuplicateEntryException: If multiple genres with the same ID are found
                                    or if updating would violate a unique constraint
        """
        result = await session.execute(
            select(GenreEntity).where(GenreEntity.id == genre_id)
        )
        # If there is more than one result, it raises an error.
        # If there is no result, scalar_one_or_none() returns None.
        try:
            genre_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="Genre", identifier=genre_id
            ) from e

        if not genre_entity:
            # If the genre does not exist, raise an exception
            raise GenreNotFoundException(genre_id=genre_id)

        for attr, value in kwargs.items():
            if value is not None and hasattr(genre_entity, attr):
                setattr(genre_entity, attr, value)

        # If name is being updated, check if it would violate uniqueness
        if "name" in kwargs and kwargs["name"] is not None:
            new_name = kwargs["name"]
            # Skip the check if the name isn't actually changing
            if genre_entity.name != new_name:
                existing_genre = await self.get_by_name(new_name, session)
                if existing_genre:
                    raise DuplicateEntryException(
                        entry_type="Genre", identifier=new_name
                    )

        try:
            await session.flush()  # Flush changes to the database

        except IntegrityError as e:
            # Handle any unique constraint violations that might occur
            if "ix_genres_name" in str(e) or "unique constraint" in str(e).lower():
                raise DuplicateEntryException(
                    entry_type="Genre",
                    identifier=kwargs.get("name", "unknown"),
                ) from e
            raise

        return GenreEntityMappers.to_domain(genre_entity)

    async def delete(self, genre_id: str, session: AsyncSession) -> None:
        """Delete a genre record.

        Args:
            genre_id: The ID of the genre to delete
            session: The database session to use

        Raises:
            GenreNotFoundException: If genre with given ID is not found
            DuplicateEntryException: If multiple genres with the same ID are found
        """
        result = await session.execute(
            select(GenreEntity).where(GenreEntity.id == genre_id)
        )
        # If there is more than one result, it raises an error.
        # If there is no result, scalar_one_or_none() returns None.
        try:
            genre_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="Genre", identifier=genre_id
            ) from e

        if not genre_entity:
            raise GenreNotFoundException(genre_id=genre_id)

        await session.delete(genre_entity)

    async def get_all_genres(self, session: AsyncSession) -> list[Genre]:
        """Get all genres without pagination."""
        result = await session.execute(select(GenreEntity))
        genre_entities = result.scalars().all()
        return GenreEntityMappers.to_domains(genre_entities)
