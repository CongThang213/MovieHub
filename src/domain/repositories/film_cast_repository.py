from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.film_cast import FilmCast


class FilmCastRepository(ABC):
    """Abstract base class for FilmCast repository."""

    @abstractmethod
    async def create(self, film_cast: FilmCast, session: AsyncSession) -> FilmCast:
        """
        Create a new FilmCast entry in the repository.

        Args:
            film_cast (FilmCast): The FilmCast object to be created.
            session (AsyncSession): The database session to use.

        Returns:
            FilmCast: The created FilmCast object with updated information (e.g., ID).
        """

    @abstractmethod
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
        """

    @abstractmethod
    async def delete(self, film_id: str, cast_id: str, session: AsyncSession) -> None:
        """
        Delete a FilmCast entry by its film_id and cast_id.

        Args:
            film_id (str): The ID of the Film.
            cast_id (str): The ID of the Cast.
            session (AsyncSession): The database session to use.
        """

    @abstractmethod
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
        """
