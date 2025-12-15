from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.seat_category_exceptions import SeatCategoryNotFoundException
from src.domain.repositories.seat_category_repository import SeatCategoryRepository


class DeleteSeatCategoryUseCase:
    """Use case for deleting a seat category."""

    def __init__(
        self,
        seat_category_repository: SeatCategoryRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._seat_category_repository = seat_category_repository
        self._sessionmaker = sessionmaker

    async def execute(self, seat_category_id: str) -> None:
        """Execute the use case to delete a seat category.

        Args:
            seat_category_id: The ID of the seat category to delete

        Raises:
            SeatCategoryNotFoundException: If the seat category does not exist
        """
        async with self._sessionmaker() as session:
            await self._seat_category_repository.delete(seat_category_id, session)
            await session.commit()
