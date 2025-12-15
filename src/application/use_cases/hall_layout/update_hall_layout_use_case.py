from typing import List, Dict

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.hall_exceptions import HallNotFoundException
from src.domain.exceptions.seat_category_exceptions import SeatCategoryNotFoundException
from src.domain.models.seat import Seat
from src.domain.models.seat_row import SeatRow
from src.domain.repositories.hall_repository import HallRepository
from src.domain.repositories.seat_category_repository import SeatCategoryRepository
from src.domain.repositories.seat_repository import SeatRepository
from src.domain.repositories.seat_row_repository import SeatRowRepository


class UpdateHallLayoutUseCase:
    """Use case for updating a complete hall layout with rows and seats."""

    def __init__(
        self,
        hall_repository: HallRepository,
        seat_row_repository: SeatRowRepository,
        seat_repository: SeatRepository,
        seat_category_repository: SeatCategoryRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._hall_repository = hall_repository
        self._seat_row_repository = seat_row_repository
        self._seat_repository = seat_repository
        self._seat_category_repository = seat_category_repository
        self._sessionmaker = sessionmaker

    async def execute(self, hall_id: str, rows_data: List[Dict]) -> Dict:
        """Execute the use case to update a hall layout.

        This replaces the entire existing layout with the new one.

        Args:
            hall_id: The ID of the hall
            rows_data: List of row configurations with seats

        Returns:
            Dictionary with updated layout information

        Raises:
            HallNotFoundException: If the hall does not exist
        """
        async with self._sessionmaker() as session:
            # Verify hall exists
            hall = await self._hall_repository.get_by_id(hall_id, session)
            if not hall:
                raise HallNotFoundException(hall_id)

            # Delete existing layout (rows and seats will be cascade deleted)
            await self._seat_row_repository.delete_by_hall_id(hall_id, session)

            # Create new layout
            created_rows = []
            total_seats = 0

            for row_data in rows_data:
                # Create seat row
                seat_row = SeatRow(
                    hall_id=hall_id,
                    row_label=row_data["row_label"],
                    row_order=row_data["row_order"],
                )
                created_row = await self._seat_row_repository.create(seat_row, session)

                # Create seats for this row
                row_seats = []
                for seat_data in row_data["seats"]:
                    # Validate that the seat category exists
                    category_id = seat_data["category_id"]
                    category = await self._seat_category_repository.get_by_id(
                        category_id, session
                    )
                    if not category:
                        raise SeatCategoryNotFoundException(category_id)

                    seat = Seat(
                        row_id=created_row.id,
                        category_id=category_id,
                        seat_number=seat_data["seat_number"],
                        pos_x=seat_data.get("pos_x", 0.0),
                        pos_y=seat_data.get("pos_y", 0.0),
                        is_accessible=seat_data.get("is_accessible", False),
                        external_label=seat_data.get("external_label"),
                    )
                    created_seat = await self._seat_repository.create(seat, session)
                    row_seats.append(created_seat)
                    total_seats += 1

                created_rows.append({"row": created_row, "seats": row_seats})

            await session.commit()

            return {
                "hall_id": hall_id,
                "rows": created_rows,
                "total_seats": total_seats,
                "total_rows": len(created_rows),
            }
