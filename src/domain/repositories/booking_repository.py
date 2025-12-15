from abc import ABC, abstractmethod
from typing import List, Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.booking import Booking


class BookingRepository(ABC):
    """Interface for booking repository"""

    @abstractmethod
    async def get_by_id(
        self, booking_id: str, session: AsyncSession
    ) -> Optional[Booking]:
        """Get a booking by ID

        Args:
            booking_id: The booking ID to look up
            session: The database session to use

        Returns:
            The booking domain model or None if not found
        """
        pass

    @abstractmethod
    async def create(self, booking: Booking, session: AsyncSession) -> Booking:
        """Create a new booking

        Args:
            booking: The booking to create
            session: The database session to use

        Returns:
            The created booking
        """
        pass

    @abstractmethod
    async def update(
        self, booking_id: str, session: AsyncSession, **kwargs: Any
    ) -> Booking:
        """Update an existing booking

        Args:
            booking_id: The ID of the booking to update
            session: The database session to use
            **kwargs: Fields to update on the booking

        Returns:
            The updated booking
        """
        pass

    @abstractmethod
    async def delete(self, booking_id: str, session: AsyncSession) -> None:
        """Delete a booking by ID

        Args:
            booking_id: The ID of the booking to delete
            session: The database session to use
        """
        pass

    @abstractmethod
    async def get_bookings(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Booking]:
        """Get a list of bookings with pagination

        Args:
            session: The database session to use
            skip: Number of bookings to skip
            limit: Maximum number of bookings to return

        Returns:
            List of bookings
        """
        pass

    @abstractmethod
    async def get_bookings_by_user_id(
        self, user_id: str, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Booking]:
        """Get a list of bookings by user ID with pagination

        Args:
            user_id: The ID of the user
            session: The database session to use
            skip: Number of bookings to skip
            limit: Maximum number of bookings to return

        Returns:
            List of bookings
        """
        pass
