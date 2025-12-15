from abc import ABC, abstractmethod
from typing import List, Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.booking_seat import BookingSeat


class BookingSeatRepository(ABC):
    """Interface for booking seat repository"""

    @abstractmethod
    async def get_by_id(
        self, booking_seat_id: str, session: AsyncSession
    ) -> Optional[BookingSeat]:
        """Get a booking seat by ID

        Args:
            booking_seat_id: The booking seat ID to look up
            session: The database session to use

        Returns:
            The booking seat domain model or None if not found
        """
        pass

    @abstractmethod
    async def create(
        self, booking_seat: BookingSeat, session: AsyncSession
    ) -> BookingSeat:
        """Create a new booking seat

        Args:
            booking_seat: The booking seat to create
            session: The database session to use

        Returns:
            The created booking seat
        """
        pass

    @abstractmethod
    async def update(
        self, booking_seat_id: str, session: AsyncSession, **kwargs: Any
    ) -> BookingSeat:
        """Update an existing booking seat

        Args:
            booking_seat_id: The ID of the booking seat to update
            session: The database session to use
            **kwargs: Fields to update on the booking seat

        Returns:
            The updated booking seat
        """
        pass

    @abstractmethod
    async def delete(self, booking_seat_id: str, session: AsyncSession) -> None:
        """Delete a booking seat by ID

        Args:
            booking_seat_id: The ID of the booking seat to delete
            session: The database session to use
        """
        pass

    @abstractmethod
    async def get_booking_seats(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[BookingSeat]:
        """Get a list of booking seats with pagination

        Args:
            session: The database session to use
            skip: Number of booking seats to skip
            limit: Maximum number of booking seats to return

        Returns:
            List of booking seats
        """
        pass

    @abstractmethod
    async def get_booking_seats_by_booking_id(
        self, booking_id: str, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[BookingSeat]:
        """Get a list of booking seats by booking ID with pagination

        Args:
            booking_id: The ID of the booking
            session: The database session to use
            skip: Number of booking seats to skip
            limit: Maximum number of booking seats to return

        Returns:
            List of booking seats
        """
        pass

    @abstractmethod
    async def get_booking_seats_by_showtime_id(
        self, showtime_id: str, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[BookingSeat]:
        """Get a list of booking seats by showtime ID with pagination

        Args:
            showtime_id: The ID of the showtime
            session: The database session to use
            skip: Number of booking seats to skip
            limit: Maximum number of booking seats to return

        Returns:
            List of booking seats
        """
        pass
