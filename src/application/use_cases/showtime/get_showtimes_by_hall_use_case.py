from typing import List

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.show_time import ShowTime
from src.domain.repositories.showtime_repository import ShowTimeRepository


class GetShowTimesByHallUseCase:
    """Use case for getting showtimes by hall ID."""

    def __init__(
        self,
        showtime_repository: ShowTimeRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._showtime_repository = showtime_repository
        self._sessionmaker = sessionmaker

    async def execute(self, hall_id: str) -> List[ShowTime]:
        """Execute the use case to get showtimes by hall ID.

        Args:
            hall_id: The ID of the hall

        Returns:
            List of showtime domain models
        """
        async with self._sessionmaker() as session:
            return await self._showtime_repository.get_by_hall_id(hall_id, session)
