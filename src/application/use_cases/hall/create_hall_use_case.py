from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.cinema_exceptions import CinemaNotFoundException
from src.domain.models.hall import Hall
from src.domain.repositories.cinema_repository import CinemaRepository
from src.domain.repositories.hall_repository import HallRepository


class CreateHallUseCase:
    """Use case for creating a hall."""

    def __init__(
        self,
        hall_repository: HallRepository,
        cinema_repository: CinemaRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._hall_repository = hall_repository
        self._cinema_repository = cinema_repository
        self._sessionmaker = sessionmaker

    async def execute(self, hall: Hall) -> Hall:
        """Execute the use case to create a hall.

        Args:
            hall: The hall domain model to create

        Returns:
            The created hall domain model

        Raises:
            CinemaNotFoundException: If the cinema_id does not exist
        """
        async with self._sessionmaker() as session:
            # Validate that the cinema exists
            if hall.cinema_id:
                cinema = await self._cinema_repository.get_by_id(
                    hall.cinema_id, session
                )
                if not cinema:
                    raise CinemaNotFoundException(hall.cinema_id)

            result = await self._hall_repository.create(hall, session)
            await session.commit()
            return result
