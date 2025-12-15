from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.seat_row import SeatRow


class SeatRowRepository(ABC):
    """Interface for seat row repository operations."""

    @abstractmethod
    async def create(self, seat_row: SeatRow, session: AsyncSession) -> SeatRow:
        """Create a new seat row record.

        Args:
            seat_row: The seat row domain model to create
            session: The database session to use

        Returns:
            The created seat row domain model with ID populated
        """
        pass

    @abstractmethod
    async def get_by_id(
        self, seat_row_id: str, session: AsyncSession
    ) -> Optional[SeatRow]:
        """Get seat row by ID.

        Args:
            seat_row_id: The ID of the seat row to retrieve
            session: The database session to use

        Returns:
            The seat row domain model or None if not found
        """
        pass

    @abstractmethod
    async def get_by_hall_id(
        self, hall_id: str, session: AsyncSession
    ) -> list[SeatRow]:
        """Get all seat rows for a specific hall.

        Args:
            hall_id: The ID of the hall
            session: The database session to use

        Returns:
            A list of seat row domain models for the specified hall
        """
        pass

    @abstractmethod
    async def delete_by_hall_id(self, hall_id: str, session: AsyncSession) -> None:
        """Delete all seat rows for a specific hall.

        Args:
            hall_id: The ID of the hall
            session: The database session to use
        """
        pass

    @abstractmethod
    async def delete(self, seat_row_id: str, session: AsyncSession) -> None:
        """Delete a seat row record.

        Args:
            seat_row_id: The ID of the seat row to delete
            session: The database session to use
        """
        pass
