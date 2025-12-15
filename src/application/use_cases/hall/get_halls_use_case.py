from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.hall import Hall
from src.domain.repositories.hall_repository import HallRepository


class GetHallsUseCase:
    """Use case for retrieving all halls with pagination."""

    def __init__(
        self,
        hall_repository: HallRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._hall_repository = hall_repository
        self._sessionmaker = sessionmaker

    async def execute(
        self,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Hall]:
        """Execute the use case to get all halls.

        Args:
            page: The page number (1-based)
            page_size: The number of items per page

        Returns:
            A list of hall domain models
        """
        async with self._sessionmaker() as session:
            return await self._hall_repository.get_all(
                session, page=page, page_size=page_size
            )
