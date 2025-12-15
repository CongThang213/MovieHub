from sqlalchemy import select, and_
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.exceptions.app_exception import DuplicateEntryException
from src.domain.exceptions.film_cast_exceptions import FilmCastNotFoundException
from src.domain.models.film_cast import FilmCast
from src.domain.repositories.film_cast_repository import FilmCastRepository
from src.infrastructure.database.models import FilmCastEntity
from src.infrastructure.database.models.mappers.film_cast_entity_mappers import (
    FilmCastEntityMappers,
)


class FilmCastRepositoryImpl(FilmCastRepository):
    """Implementation of FilmCastRepository using SQLAlchemy."""

    async def create(self, film_cast: FilmCast, session: AsyncSession) -> FilmCast:
        """
        Create a new FilmCast entry in the repository.

        Args:
            film_cast (FilmCast): The FilmCast object to be created.
            session (AsyncSession): The database session to use.

        Returns:
            FilmCast: The created FilmCast object with updated information (e.g., ID).

        Raises:
            DuplicateEntryException: If a FilmCast with the same identifier already exists.
        """
        film_cast_entity = FilmCastEntityMappers.from_domain(film_cast)
        try:
            session.add(film_cast_entity)
            await session.flush()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="FilmCast",
                identifier={
                    "film_id": film_cast.film_id,
                    "cast_id": film_cast.cast_id,
                },
            ) from e

        return FilmCastEntityMappers.to_domain(film_cast_entity)

    async def get_by_id(
        self, film_id: str, cast_id: str, session: AsyncSession
    ) -> FilmCast:
        """
        Retrieve a FilmCast entry by its film_id and cast_id.

        Args:
            film_id (str): The ID of the Film.
            cast_id (str): The ID of the Cast.
            session (AsyncSession): The database session to use.

        Returns:
            FilmCast: The FilmCast object if found, otherwise exception is raised.

        Raises:
            DuplicateEntryException: If multiple FilmCast entries with the same film_id and cast_id are found.
            FilmCastNotFoundException: If no FilmCast with the given film_id and cast_id is found.
        """
        try:
            result = await session.execute(
                select(FilmCastEntity).where(
                    and_(
                        FilmCastEntity.film_id == film_id,
                        FilmCastEntity.cast_id == cast_id,
                    )
                )
            )
            film_cast_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="FilmCast",
                identifier={"film_id": film_id, "cast_id": cast_id},
            ) from e

        if film_cast_entity is None:
            raise FilmCastNotFoundException(film_id=film_id, cast_id=cast_id)

        return FilmCastEntityMappers.to_domain(film_cast_entity)

    async def delete(self, film_id: str, cast_id: str, session: AsyncSession) -> None:
        """
        Delete a FilmCast entry by its film_id and cast_id.

        Args:
            film_id (str): The ID of the Film.
            cast_id (str): The ID of the Cast.
            session (AsyncSession): The database session to use.

        Raises:
            DuplicateEntryException: If multiple FilmCast entries with the same film_id and cast_id are found.
            FilmCastNotFoundException: If no FilmCast with the given film_id and cast_id is found.
        """
        try:
            result = await session.execute(
                select(FilmCastEntity).where(
                    and_(
                        FilmCastEntity.film_id == film_id,
                        FilmCastEntity.cast_id == cast_id,
                    )
                )
            )
            film_cast_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="FilmCast",
                identifier={"film_id": film_id, "cast_id": cast_id},
            ) from e

        if not film_cast_entity:
            raise FilmCastNotFoundException(film_id=film_id, cast_id=cast_id)

        await session.delete(film_cast_entity)
        await session.flush()

    async def update(
        self, film_id: str, cast_id: str, session: AsyncSession, **kwargs
    ) -> FilmCast:
        """
        Update a FilmCast entry by its film_id and cast_id.

        Args:
            film_id (str): The ID of the Film.
            cast_id (str): The ID of the Cast.
            session (AsyncSession): The database session to use.
            **kwargs: The fields to update with their new values.

        Keyword Args:
            role (str): The new role of the cast member. (optional)
            character_name (str): The new character name. (optional)

        Returns:
            FilmCast: The updated FilmCast object.

        Raises:

        """
        try:
            result = await session.execute(
                select(FilmCastEntity).where(
                    and_(
                        FilmCastEntity.film_id == film_id,
                        FilmCastEntity.cast_id == cast_id,
                    )
                )
            )
            film_cast_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="FilmCast",
                identifier={"film_id": film_id, "cast_id": cast_id},
            ) from e

        if film_cast_entity is None:
            raise FilmCastNotFoundException(film_id=film_id, cast_id=cast_id)

        # Update the entity fields
        for attr, value in kwargs.items():
            if not value and hasattr(film_cast_entity, attr):
                setattr(film_cast_entity, attr, value)

        await session.flush()

        return FilmCastEntityMappers.to_domain(film_cast_entity)
