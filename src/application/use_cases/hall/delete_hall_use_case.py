from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.hall_exceptions import HallNotFoundException
from src.domain.repositories.hall_repository import HallRepository


class DeleteHallUseCase:
    """Use case for deleting a hall."""

    def __init__(
        self,
        hall_repository: HallRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._hall_repository = hall_repository
        self._sessionmaker = sessionmaker

    async def execute(self, hall_id: str) -> bool:
        """Execute the use case to delete a hall.

        Args:
            hall_id: The ID of the hall to delete

        Returns:
            True if deletion was successful

        Raises:
            HallNotFoundException: If the hall doesn't exist
        """
        async with self._sessionmaker() as session:
            result = await self._hall_repository.delete(hall_id, session)
            await session.commit()
            return result
