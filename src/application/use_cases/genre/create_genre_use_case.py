from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.genre import Genre
from src.domain.repositories.genre_repository import GenreRepository


class CreateGenreUseCase:
    """Use case for creating a new genre."""

    def __init__(
        self,
        genre_repository: GenreRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._genre_repository = genre_repository
        self._sessionmaker = sessionmaker

    async def execute(self, genre: Genre) -> Genre:
        """Execute the use case to create a new genre.

        Args:
            genre: The genre domain model to create

        Returns:
            The created genre domain model with ID populated
        """
        async with self._sessionmaker() as session:
            result = await self._genre_repository.create(genre, session)
            await session.commit()
            return result
