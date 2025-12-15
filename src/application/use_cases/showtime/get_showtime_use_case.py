from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.showtime_exceptions import ShowTimeNotFoundException
from src.domain.models.show_time import ShowTime
from src.domain.repositories.showtime_repository import ShowTimeRepository


class GetShowTimeUseCase:
    """Use case for getting a showtime by ID."""

    def __init__(
        self,
        showtime_repository: ShowTimeRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._showtime_repository = showtime_repository
        self._sessionmaker = sessionmaker

    async def execute(self, showtime_id: str) -> ShowTime:
        """Execute the use case to get a showtime.

        Args:
            showtime_id: The ID of the showtime

        Returns:
            The showtime domain model

        Raises:
            ShowTimeNotFoundException: If showtime is not found
        """
        async with self._sessionmaker() as session:
            showtime = await self._showtime_repository.get_by_id(showtime_id, session)

            if not showtime:
                raise ShowTimeNotFoundException(showtime_id)

            return showtime
