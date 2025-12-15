from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.repositories.film_format_repository import FilmFormatRepository


class DeleteFilmFormatUseCase:
    """Use case for deleting a film format."""

    def __init__(
        self,
        film_format_repository: FilmFormatRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_format_repository = film_format_repository
        self._sessionmaker = sessionmaker

    async def execute(self, film_format_id: str) -> None:
        """Delete a film format by its ID.
        Args:
            film_format_id: The ID of the film format to delete
        """
        async with self._sessionmaker() as session:
            await self._film_format_repository.delete(film_format_id, session)
            await session.commit()
