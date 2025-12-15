from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.genre import Genre
from src.domain.repositories.genre_repository import GenreRepository


class UpdateGenreUseCase:
    """Use case for updating a genre."""

    def __init__(
        self,
        genre_repository: GenreRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._genre_repository = genre_repository
        self._sessionmaker = sessionmaker

    async def execute(self, genre_id: str, **kwargs) -> Genre:
        """Execute the use case to update a genre.

        Args:
            genre_id: The ID of the genre to update
            **kwargs: Additional fields to update

        Keyword Args:
            name: The new name for the genre

        Returns:
            The updated genre domain model
        """
        async with self._sessionmaker() as session:
            result = await self._genre_repository.update(genre_id, session, **kwargs)
            await session.commit()
            return result
