from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.cinema import Cinema
from src.domain.repositories.cinema_repository import CinemaRepository


class GetCinemasByCityUseCase:
    """Use case for retrieving cinemas by city ID with pagination."""

    def __init__(
        self,
        cinema_repository: CinemaRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._cinema_repository = cinema_repository
        self._sessionmaker = sessionmaker

    async def execute(
        self,
        city_id: str,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Cinema]:
        """Execute the use case to retrieve cinemas by city.

        Args:
            city_id: The ID of the city
            page: The page number (1-based)
            page_size: The number of records per page

        Returns:
            A list of cinema domain models
        """
        async with self._sessionmaker() as session:
            return await self._cinema_repository.get_by_city_id(
                city_id, session, page, page_size
            )
