from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.cinema import Cinema
from src.domain.repositories.cinema_repository import CinemaRepository


class UpdateCinemaUseCase:
    """Use case for updating a cinema."""

    def __init__(
        self,
        cinema_repository: CinemaRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._cinema_repository = cinema_repository
        self._sessionmaker = sessionmaker

    async def execute(self, cinema: Cinema) -> Cinema:
        """Execute the use case to update a cinema.

        Args:
            cinema: The cinema domain model with updated fields

        Returns:
            The updated cinema domain model
        """
        async with self._sessionmaker() as session:
            result = await self._cinema_repository.update(cinema, session)
            await session.commit()
            return result
