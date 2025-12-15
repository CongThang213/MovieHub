from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.hall_exceptions import HallNotFoundException
from src.domain.models.hall import Hall
from src.domain.repositories.hall_repository import HallRepository


class UpdateHallUseCase:
    """Use case for updating a hall."""

    def __init__(
        self,
        hall_repository: HallRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._hall_repository = hall_repository
        self._sessionmaker = sessionmaker

    async def execute(self, hall: Hall) -> Hall:
        """Execute the use case to update a hall.

        Args:
            hall: The hall domain model with updated fields

        Returns:
            The updated hall domain model

        Raises:
            HallNotFoundException: If the hall doesn't exist
        """
        async with self._sessionmaker() as session:
            result = await self._hall_repository.update(hall, session)
            await session.commit()
            return result
