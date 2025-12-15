from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.genre import Genre
from src.domain.repositories.genre_repository import GenreRepository


class GetGenreUseCase:
    """Use case for retrieving a genre by its ID."""

    def __init__(
        self,
        genre_repository: GenreRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._genre_repository = genre_repository
        self._sessionmaker = sessionmaker

    async def execute(self, genre_id: str) -> Optional[Genre]:
        """Execute the use case to get a genre by ID.

        Args:
            genre_id: The ID of the genre to retrieve

        Returns:
            The genre domain model or None if not found
        """
        async with self._sessionmaker() as session:
            return await self._genre_repository.get_by_id(genre_id, session)
