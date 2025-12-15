from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.showtime_exceptions import ShowTimeNotFoundException
from src.domain.repositories.showtime_repository import ShowTimeRepository


class DeleteShowTimeUseCase:
    """Use case for deleting a showtime."""

    def __init__(
        self,
        showtime_repository: ShowTimeRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._showtime_repository = showtime_repository
        self._sessionmaker = sessionmaker

    async def execute(self, showtime_id: str) -> None:
        """Execute the use case to delete a showtime.

        Args:
            showtime_id: The ID of the showtime to delete

        Raises:
            ShowTimeNotFoundException: If showtime is not found
        """
        async with self._sessionmaker() as session:
            # Check if showtime exists
            showtime = await self._showtime_repository.get_by_id(showtime_id, session)
            if not showtime:
                raise ShowTimeNotFoundException(showtime_id)

            await self._showtime_repository.delete(showtime_id, session)
            await session.commit()
