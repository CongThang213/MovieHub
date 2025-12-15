from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.seat_category import SeatCategory
from src.domain.repositories.seat_category_repository import SeatCategoryRepository


class GetSeatCategoriesUseCase:
    """Use case for retrieving all seat categories with pagination."""

    def __init__(
        self,
        seat_category_repository: SeatCategoryRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._seat_category_repository = seat_category_repository
        self._sessionmaker = sessionmaker

    async def execute(
        self, page: int = PAGE_DEFAULT, page_size: int = PAGE_SIZE_DEFAULT
    ) -> list[SeatCategory]:
        """Execute the use case to get all seat categories.

        Args:
            page: The page number (1-based)
            page_size: The number of items per page

        Returns:
            A list of seat category domain models
        """
        async with self._sessionmaker() as session:
            return await self._seat_category_repository.get_all(
                session, page, page_size
            )
