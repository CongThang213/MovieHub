from typing import List

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.show_time import ShowTime
from src.domain.repositories.showtime_repository import ShowTimeRepository


class GetShowTimesByFilmUseCase:
    """Use case for getting showtimes by film ID."""

    def __init__(
        self,
        showtime_repository: ShowTimeRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._showtime_repository = showtime_repository
        self._sessionmaker = sessionmaker

    async def execute(self, film_id: str) -> List[ShowTime]:
        """Execute the use case to get showtimes by film ID.

        Args:
            film_id: The ID of the film

        Returns:
            List of showtime domain models
        """
        async with self._sessionmaker() as session:
            return await self._showtime_repository.get_by_film_id(film_id, session)
