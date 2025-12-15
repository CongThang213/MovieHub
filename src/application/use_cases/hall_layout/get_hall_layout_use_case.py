from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.hall_exceptions import HallNotFoundException
from src.domain.repositories.hall_repository import HallRepository
from src.domain.repositories.seat_repository import SeatRepository
from src.domain.repositories.seat_row_repository import SeatRowRepository


class GetHallLayoutUseCase:
    """Use case for retrieving a complete hall layout with rows and seats."""

    def __init__(
        self,
        hall_repository: HallRepository,
        seat_row_repository: SeatRowRepository,
        seat_repository: SeatRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._hall_repository = hall_repository
        self._seat_row_repository = seat_row_repository
        self._seat_repository = seat_repository
        self._sessionmaker = sessionmaker

    async def execute(self, hall_id: str) -> Dict:
        """Execute the use case to get a hall layout.

        Args:
            hall_id: The ID of the hall

        Returns:
            Dictionary with complete layout information

        Raises:
            HallNotFoundException: If the hall does not exist
        """
        async with self._sessionmaker() as session:
            # Verify hall exists
            hall = await self._hall_repository.get_by_id(hall_id, session)
            if not hall:
                raise HallNotFoundException(hall_id)

            # Get all rows for the hall
            rows = await self._seat_row_repository.get_by_hall_id(hall_id, session)

            # Get seats for each row
            layout_rows = []
            total_seats = 0

            for row in rows:
                # Get seats for this row (fetch all seats without pagination limit)
                seats = await self._seat_repository.get_by_row_id(
                    row.id, session, page=1, page_size=1000
                )
                total_seats += len(seats)

                layout_rows.append({"row": row, "seats": seats})

            return {
                "hall_id": hall_id,
                "rows": layout_rows,
                "total_seats": total_seats,
                "total_rows": len(layout_rows),
            }
