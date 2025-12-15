from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.seat_category import SeatCategory
from src.domain.repositories.seat_category_repository import SeatCategoryRepository


class UpdateSeatCategoryUseCase:
    """Use case for updating a seat category."""

    def __init__(
        self,
        seat_category_repository: SeatCategoryRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._seat_category_repository = seat_category_repository
        self._sessionmaker = sessionmaker

    async def execute(self, seat_category: SeatCategory) -> SeatCategory:
        """Execute the use case to update a seat category.

        Args:
            seat_category: The seat category domain model to update

        Returns:
            The updated seat category domain model

        Raises:
            SeatCategoryNotFoundException: If the seat category does not exist
        """
        async with self._sessionmaker() as session:
            result = await self._seat_category_repository.update(seat_category, session)
            await session.commit()
            return result


# Seat Category Use Cases
