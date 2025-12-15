from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.flim_format import FilmFormat
from src.domain.repositories.film_format_repository import FilmFormatRepository


class GetFilmFormatUseCase:
    """Use case for retrieving a film format by its ID."""

    def __init__(
        self,
        film_format_repository: FilmFormatRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_format_repository = film_format_repository
        self._sessionmaker = sessionmaker

    async def execute(self, film_format_id: str) -> Optional[FilmFormat]:
        """Retrieve a film format by its ID.

        Args:
            film_format_id: The ID of the film format to retrieve.

        Returns:
            The film format domain model or None if not found.
        """
        async with self._sessionmaker() as session:
            return await self._film_format_repository.get_by_id(film_format_id, session)
