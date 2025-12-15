from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.repositories.cinema_repository import CinemaRepository


class DeleteCinemaUseCase:
    """Use case for deleting a cinema."""

    def __init__(
        self,
        cinema_repository: CinemaRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._cinema_repository = cinema_repository
        self._sessionmaker = sessionmaker

    async def execute(self, cinema_id: str) -> bool:
        """Execute the use case to delete a cinema.

        Args:
            cinema_id: The ID of the cinema to delete

        Returns:
            True if the cinema was deleted, False otherwise
        """
        async with self._sessionmaker() as session:
            result = await self._cinema_repository.delete(cinema_id, session)
            await session.commit()
            return result


# Cinema use cases
