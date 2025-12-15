from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.repositories.film_cast_repository import FilmCastRepository


class DeleteFilmCastUseCase:
    """Use case for deleting a film-cast relationship."""

    def __init__(
        self,
        film_cast_repository: FilmCastRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_cast_repository = film_cast_repository
        self._sessionmaker = sessionmaker

    async def execute(self, film_id: str, cast_id: str) -> None:
        """Execute the use case to delete a film-cast relationship.

        Args:
            film_id: The ID of the film
            cast_id: The ID of the cast member
        """
        async with self._sessionmaker() as session:
            await self._film_cast_repository.delete(film_id, cast_id, session)
            await session.commit()
