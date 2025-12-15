from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.hall_exceptions import HallNotFoundException
from src.domain.models.hall import Hall
from src.domain.repositories.hall_repository import HallRepository


class GetHallUseCase:
    """Use case for retrieving a single hall by ID."""

    def __init__(
        self,
        hall_repository: HallRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._hall_repository = hall_repository
        self._sessionmaker = sessionmaker

    async def execute(self, hall_id: str) -> Hall:
        """Execute the use case to get a hall by ID.

        Args:
            hall_id: The ID of the hall to retrieve

        Returns:
            The hall domain model

        Raises:
            HallNotFoundException: If the hall is not found
        """
        async with self._sessionmaker() as session:
            hall = await self._hall_repository.get_by_id(hall_id, session)
            if not hall:
                raise HallNotFoundException(hall_id)
            return hall
