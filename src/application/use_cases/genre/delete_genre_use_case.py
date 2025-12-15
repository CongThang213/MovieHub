from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.repositories.genre_repository import GenreRepository


class DeleteGenreUseCase:
    """Use case for deleting a genre by its ID."""

    def __init__(
        self,
        genre_repository: GenreRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._genre_repository = genre_repository
        self._sessionmaker = sessionmaker

    async def execute(self, genre_id: str) -> None:
        """Delete a genre by its ID.

        Args:
            genre_id: The ID of the genre to delete
        """
        async with self._sessionmaker() as session:
            await self._genre_repository.delete(genre_id, session)
            await session.commit()
