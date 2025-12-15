from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.film_cast import FilmCast
from src.domain.repositories.film_cast_repository import FilmCastRepository


class GetFilmCastUseCase:
    """Use case for retrieving a film-cast relationship by film ID and cast ID."""

    def __init__(
        self,
        film_cast_repository: FilmCastRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_cast_repository = film_cast_repository
        self._sessionmaker = sessionmaker

    async def execute(self, film_id: str, cast_id: str) -> FilmCast:
        """Execute the use case to retrieve a film-cast relationship.

        Args:
            film_id: The ID of the film
            cast_id: The ID of the cast member

        Returns:
            The film_cast domain model if found
        """
        async with self._sessionmaker() as session:
            return await self._film_cast_repository.get_by_id(film_id, cast_id, session)
