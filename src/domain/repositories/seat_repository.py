from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.seat import Seat


class SeatRepository(ABC):
    """Interface for seat repository operations."""

    @abstractmethod
    async def create(self, seat: Seat, session: AsyncSession) -> Seat:
        """Create a new seat record.

        Args:
            seat: The seat domain model to create
            session: The database session to use

        Returns:
            The created seat domain model with ID populated
        """
        pass

    @abstractmethod
    async def get_by_id(self, seat_id: str, session: AsyncSession) -> Optional[Seat]:
        """Get seat by ID.

        Args:
            seat_id: The ID of the seat to retrieve
            session: The database session to use

        Returns:
            The seat domain model or None if not found
        """
        pass

    @abstractmethod
    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Seat]:
        """Get all seats with pagination.

        Args:
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.

        Returns:
            A list of seat domain models for the specified page
        """
        pass

    @abstractmethod
    async def get_by_row_id(
        self,
        row_id: str,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Seat]:
        """Get all seats in a specific row with pagination.

        Args:
            row_id: The ID of the row
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.

        Returns:
            A list of seat domain models for the specified row and page
        """
        pass

    @abstractmethod
    async def get_by_category_id(
        self,
        category_id: str,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Seat]:
        """Get all seats in a specific category with pagination.

        Args:
            category_id: The ID of the category
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.

        Returns:
            A list of seat domain models for the specified category and page
        """
        pass

    @abstractmethod
    async def update(self, seat: Seat, session: AsyncSession) -> Seat:
        """Update an existing seat record.

        Args:
            seat: The seat domain model to update
            session: The database session to use

        Returns:
            The updated seat domain model
        """
        pass

    @abstractmethod
    async def delete(self, seat_id: str, session: AsyncSession) -> None:
        """Delete a seat record.

        Args:
            seat_id: The ID of the seat to delete
            session: The database session to use
        """
        pass
