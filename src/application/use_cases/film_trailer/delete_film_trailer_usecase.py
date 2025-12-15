from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.repositories.film_trailer_repository import FilmTrailerRepository


class DeleteFilmTrailerUseCase:
    """Use case for deleting a film trailer."""

    def __init__(
        self,
        film_trailer_repository: FilmTrailerRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_trailer_repository = film_trailer_repository
        self._sessionmaker = sessionmaker

    async def execute(self, trailer_id: str) -> None:
        """Delete a film trailer.

        Args:
            trailer_id: The ID of the film trailer to delete.
        """
        async with self._sessionmaker() as session:
            await self._film_trailer_repository.delete(trailer_id, session)
            await session.commit()
