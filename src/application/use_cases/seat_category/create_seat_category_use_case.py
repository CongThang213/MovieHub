from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.seat_category import SeatCategory
from src.domain.repositories.seat_category_repository import SeatCategoryRepository


class CreateSeatCategoryUseCase:
    """Use case for creating a seat category."""

    def __init__(
        self,
        seat_category_repository: SeatCategoryRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._seat_category_repository = seat_category_repository
        self._sessionmaker = sessionmaker

    async def execute(self, seat_category: SeatCategory) -> SeatCategory:
        """Execute the use case to create a seat category.

        Args:
            seat_category: The seat category domain model to create

        Returns:
            The created seat category domain model
        """
        async with self._sessionmaker() as session:
            result = await self._seat_category_repository.create(seat_category, session)
            await session.commit()
            return result
