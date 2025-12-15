from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.cinema_exceptions import CinemaNotFoundException
from src.domain.models.cinema import Cinema
from src.domain.repositories.cinema_repository import CinemaRepository


class GetCinemaUseCase:
    """Use case for retrieving a cinema by ID."""

    def __init__(
        self,
        cinema_repository: CinemaRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._cinema_repository = cinema_repository
        self._sessionmaker = sessionmaker

    async def execute(self, cinema_id: str) -> Cinema:
        """Execute the use case to retrieve a cinema.

        Args:
            cinema_id: The ID of the cinema to retrieve

        Returns:
            The cinema domain model

        Raises:
            CinemaNotFoundException: If the cinema is not found
        """
        async with self._sessionmaker() as session:
            cinema = await self._cinema_repository.get_by_id(cinema_id, session)
            if not cinema:
                raise CinemaNotFoundException(cinema_id)
            return cinema
