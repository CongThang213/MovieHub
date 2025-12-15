from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.hall import Hall


class HallRepository(ABC):
    """Interface for hall repository operations."""

    @abstractmethod
    async def create(self, hall: Hall, session: AsyncSession) -> Hall:
        """Create a new hall record.

        Args:
            hall: The hall domain model to create
            session: The database session to use

        Returns:
            The created hall domain model with ID populated
        """
        pass

    @abstractmethod
    async def get_by_id(self, hall_id: str, session: AsyncSession) -> Optional[Hall]:
        """Get hall by ID.

        Args:
            hall_id: The ID of the hall to retrieve
            session: The database session to use

        Returns:
            The hall domain model or None if not found
        """
        pass

    @abstractmethod
    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Hall]:
        """Get all halls with pagination.

        Args:
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.

        Returns:
            A list of hall domain models for the specified page
        """
        pass

    @abstractmethod
    async def get_by_cinema_id(
        self,
        cinema_id: str,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Hall]:
        """Get all halls in a specific cinema with pagination.

        Args:
            cinema_id: The ID of the cinema
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.

        Returns:
            A list of hall domain models for the specified cinema and page
        """
        pass

    @abstractmethod
    async def update(self, hall: Hall, session: AsyncSession) -> Hall:
        """Update an existing hall record.

        Args:
            hall: The hall domain model with updated fields
            session: The database session to use

        Returns:
            The updated hall domain model
        """
        pass

    @abstractmethod
    async def delete(self, hall_id: str, session: AsyncSession) -> bool:
        """Delete a hall record.

        Args:
            hall_id: The ID of the hall to delete
            session: The database session to use

        Returns:
            True if deletion was successful, False otherwise
        """
        pass
