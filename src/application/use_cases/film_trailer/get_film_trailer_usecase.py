from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.film_trailer import FilmTrailer
from src.domain.repositories.film_trailer_repository import FilmTrailerRepository


class GetFilmTrailerUseCase:
    """Use case for retrieving a film trailer by its ID."""

    def __init__(
        self,
        film_trailer_repository: FilmTrailerRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_trailer_repository = film_trailer_repository
        self._sessionmaker = sessionmaker

    async def execute(self, trailer_id: str) -> Optional[FilmTrailer]:
        """Retrieve a film trailer by its ID.

        Args:
            trailer_id: The ID of the film trailer to retrieve.

        Returns:
            The film trailer domain model or None if not found.
        """
        async with self._sessionmaker() as session:
            return await self._film_trailer_repository.get_by_id(trailer_id, session)
