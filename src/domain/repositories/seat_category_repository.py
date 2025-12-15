from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.seat_category import SeatCategory


class SeatCategoryRepository(ABC):
    """Interface for seat category repository operations."""

    @abstractmethod
    async def create(
        self, seat_category: SeatCategory, session: AsyncSession
    ) -> SeatCategory:
        """Create a new seat category record.

        Args:
            seat_category: The seat category domain model to create
            session: The database session to use

        Returns:
            The created seat category domain model with ID populated
        """
        pass

    @abstractmethod
    async def get_by_id(
        self, seat_category_id: str, session: AsyncSession
    ) -> Optional[SeatCategory]:
        """Get seat category by ID.

        Args:
            seat_category_id: The ID of the seat category to retrieve
            session: The database session to use

        Returns:
            The seat category domain model or None if not found
        """
        pass

    @abstractmethod
    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[SeatCategory]:
        """Get all seat categories with pagination.

        Args:
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.

        Returns:
            A list of seat category domain models for the specified page
        """
        pass

    @abstractmethod
    async def update(
        self, seat_category: SeatCategory, session: AsyncSession
    ) -> SeatCategory:
        """Update an existing seat category record.

        Args:
            seat_category: The seat category domain model to update
            session: The database session to use

        Returns:
            The updated seat category domain model
        """
        pass

    @abstractmethod
    async def delete(self, seat_category_id: str, session: AsyncSession) -> None:
        """Delete a seat category record.

        Args:
            seat_category_id: The ID of the seat category to delete
            session: The database session to use
        """
        pass
