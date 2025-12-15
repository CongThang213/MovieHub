from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.flim_format import FilmFormat
from src.domain.repositories.film_format_repository import FilmFormatRepository


class CreateFilmFormatUseCase:
    """Use case for creating a new film format."""

    def __init__(
        self,
        film_format_repository: FilmFormatRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_format_repository = film_format_repository
        self._sessionmaker = sessionmaker

    async def execute(self, film_format: FilmFormat) -> FilmFormat:
        """Create a new film format.

        Args:
            film_format: The film format domain model to create.

        Returns:
            The created film format with the ID assigned.
        """
        async with self._sessionmaker() as session:
            result = await self._film_format_repository.create(film_format, session)
            await session.commit()
            return result
