from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.seat_category_exceptions import SeatCategoryNotFoundException
from src.domain.models.seat_category import SeatCategory
from src.domain.repositories.seat_category_repository import SeatCategoryRepository


class GetSeatCategoryUseCase:
    """Use case for retrieving a seat category by ID."""

    def __init__(
        self,
        seat_category_repository: SeatCategoryRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._seat_category_repository = seat_category_repository
        self._sessionmaker = sessionmaker

    async def execute(self, seat_category_id: str) -> SeatCategory:
        """Execute the use case to get a seat category by ID.

        Args:
            seat_category_id: The ID of the seat category to retrieve

        Returns:
            The seat category domain model

        Raises:
            SeatCategoryNotFoundException: If the seat category does not exist
        """
        async with self._sessionmaker() as session:
            result = await self._seat_category_repository.get_by_id(
                seat_category_id, session
            )
            if not result:
                raise SeatCategoryNotFoundException(seat_category_id)
            return result
