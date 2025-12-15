from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.cinema import Cinema
from src.domain.repositories.cinema_repository import CinemaRepository


class GetCinemasUseCase:
    """Use case for retrieving all cinemas with pagination."""

    def __init__(
        self,
        cinema_repository: CinemaRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._cinema_repository = cinema_repository
        self._sessionmaker = sessionmaker

    async def execute(
        self, page: int = PAGE_DEFAULT, page_size: int = PAGE_SIZE_DEFAULT
    ) -> list[Cinema]:
        """Execute the use case to retrieve all cinemas.

        Args:
            page: The page number (1-based)
            page_size: The number of records per page

        Returns:
            A list of cinema domain models
        """
        async with self._sessionmaker() as session:
            return await self._cinema_repository.get_all(session, page, page_size)
