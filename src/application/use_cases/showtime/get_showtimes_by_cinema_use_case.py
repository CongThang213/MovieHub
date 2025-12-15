from typing import List

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.show_time import ShowTime
from src.domain.repositories.showtime_repository import ShowTimeRepository


class GetShowTimesByCinemaUseCase:
    """Use case for getting showtimes by cinema ID."""

    def __init__(
        self,
        showtime_repository: ShowTimeRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._showtime_repository = showtime_repository
        self._sessionmaker = sessionmaker

    async def execute(self, cinema_id: str) -> List[ShowTime]:
        """Execute the use case to get showtimes by cinema ID.

        Args:
            cinema_id: The ID of the cinema

        Returns:
            List of showtime domain models
        """
        async with self._sessionmaker() as session:
            return await self._showtime_repository.get_by_cinema_id(cinema_id, session)
