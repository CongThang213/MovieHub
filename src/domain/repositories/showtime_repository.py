from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.show_time import ShowTime


class ShowTimeRepository(ABC):
    """Abstract repository interface for ShowTime operations."""

    @abstractmethod
    async def create(self, showtime: ShowTime, session: AsyncSession) -> ShowTime:
        """Create a new showtime.

        Args:
            showtime: The showtime domain model to create
            session: The database session

        Returns:
            The created showtime domain model
        """
        pass

    @abstractmethod
    async def get_by_id(
        self, showtime_id: str, session: AsyncSession
    ) -> Optional[ShowTime]:
        """Get a showtime by ID.

        Args:
            showtime_id: The ID of the showtime
            session: The database session

        Returns:
            The showtime domain model if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_all(
        self,
        page: int,
        page_size: int,
        session: AsyncSession,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        film_id: Optional[str] = None,
        cinema_id: Optional[str] = None,
    ) -> dict:
        """Get all showtimes with pagination and optional filtering.

        Args:
            page: The page number (1-based)
            page_size: The number of items per page
            session: The database session
            start_date: Optional start date to filter showtimes
            end_date: Optional end date to filter showtimes
            film_id: Optional film ID filter
            cinema_id: Optional cinema ID filter

        Returns:
            Dict containing:
                - showtimes: List of showtime domain models
                - page: Current page number
                - page_size: Number of items per page
                - total: Total number of showtimes
        """
        pass

    @abstractmethod
    async def get_by_film_id(
        self, film_id: str, session: AsyncSession
    ) -> List[ShowTime]:
        """Get all showtimes for a specific film.

        Args:
            film_id: The ID of the film
            session: The database session

        Returns:
            List of showtime domain models
        """
        pass

    @abstractmethod
    async def get_by_hall_id(
        self, hall_id: str, session: AsyncSession
    ) -> List[ShowTime]:
        """Get all showtimes for a specific hall.

        Args:
            hall_id: The ID of the hall
            session: The database session

        Returns:
            List of showtime domain models
        """
        pass

    @abstractmethod
    async def get_by_cinema_id(
        self, cinema_id: str, session: AsyncSession
    ) -> List[ShowTime]:
        """Get all showtimes for a specific cinema.

        Args:
            cinema_id: The ID of the cinema
            session: The database session

        Returns:
            List of showtime domain models
        """
        pass

    @abstractmethod
    async def get_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        session: AsyncSession,
        film_id: Optional[str] = None,
        cinema_id: Optional[str] = None,
    ) -> List[ShowTime]:
        """Get showtimes within a date range with optional filters.

        Args:
            start_date: The start date
            end_date: The end date
            session: The database session
            film_id: Optional film ID filter
            cinema_id: Optional cinema ID filter

        Returns:
            List of showtime domain models
        """
        pass

    @abstractmethod
    async def update(self, showtime: ShowTime, session: AsyncSession) -> ShowTime:
        """Update an existing showtime.

        Args:
            showtime: The showtime domain model with updated data
            session: The database session

        Returns:
            The updated showtime domain model
        """
        pass

    @abstractmethod
    async def delete(self, showtime_id: str, session: AsyncSession) -> bool:
        """Delete a showtime.

        Args:
            showtime_id: The ID of the showtime to delete
            session: The database session

        Returns:
            True if deleted successfully, False otherwise
        """
        pass

    @abstractmethod
    async def check_time_conflict(
        self,
        hall_id: str,
        start_time: datetime,
        end_time: datetime,
        session: AsyncSession,
        exclude_showtime_id: Optional[str] = None,
    ) -> bool:
        """Check if there's a time conflict for a hall.

        Args:
            hall_id: The ID of the hall
            start_time: The start time
            end_time: The end time
            session: The database session
            exclude_showtime_id: Optional showtime ID to exclude from conflict check

        Returns:
            True if there's a conflict, False otherwise
        """
        pass
