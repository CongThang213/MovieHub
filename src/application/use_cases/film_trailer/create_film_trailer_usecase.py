from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.film_trailer import FilmTrailer
from src.domain.repositories.film_trailer_repository import FilmTrailerRepository


class CreateFilmTrailerUseCase:
    """Use case for creating a new film trailer."""

    def __init__(
        self,
        film_trailer_repository: FilmTrailerRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_trailer_repository = film_trailer_repository
        self._sessionmaker = sessionmaker

    async def execute(self, film_trailer: FilmTrailer) -> FilmTrailer:
        """Create a new film trailer.

        Args:
            film_trailer: The film trailer domain model to create.

        Returns:
            The created film trailer with the ID assigned.
        """
        async with self._sessionmaker() as session:
            result = await self._film_trailer_repository.create(film_trailer, session)
            await session.commit()
            return result
