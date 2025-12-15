from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.film_cast import FilmCast
from src.domain.repositories.film_cast_repository import FilmCastRepository


class CreateFilmCastUseCase:
    """Use case for creating a new film-cast relationship."""

    def __init__(
        self,
        film_cast_repository: FilmCastRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_cast_repository = film_cast_repository
        self._sessionmaker = sessionmaker

    async def execute(self, film_cast: FilmCast) -> FilmCast:
        """Execute the use case to create a new film-cast relationship.

        Args:
            film_cast: The film_cast domain model to create

        Returns:
            The created film_cast domain model
        """
        async with self._sessionmaker() as session:
            result = await self._film_cast_repository.create(film_cast, session)
            await session.commit()
            return result
