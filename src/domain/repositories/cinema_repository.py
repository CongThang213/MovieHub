from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.cinema import Cinema


class CinemaRepository(ABC):
    """Interface for cinema repository operations."""

    @abstractmethod
    async def create(self, cinema: Cinema, session: AsyncSession) -> Cinema:
        """Create a new cinema record.

        Args:
            cinema: The cinema domain model to create
            session: The database session to use

        Returns:
            The created cinema domain model with ID populated
        """
        pass

    @abstractmethod
    async def get_by_id(
        self, cinema_id: str, session: AsyncSession
    ) -> Optional[Cinema]:
        """Get cinema by ID.

        Args:
            cinema_id: The ID of the cinema to retrieve
            session: The database session to use

        Returns:
            The cinema domain model or None if not found
        """
        pass

    @abstractmethod
    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Cinema]:
        """Get all cinemas with pagination.

        Args:
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.

        Returns:
            A list of cinema domain models for the specified page
        """
        pass

    @abstractmethod
    async def get_by_city_id(
        self,
        city_id: str,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Cinema]:
        """Get all cinemas in a specific city with pagination.

        Args:
            city_id: The ID of the city
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.

        Returns:
            A list of cinema domain models for the specified city and page
        """
        pass

    @abstractmethod
    async def update(self, cinema: Cinema, session: AsyncSession) -> Cinema:
        """Update an existing cinema record.

        Args:
            cinema: The cinema domain model with updated fields
            session: The database session to use

        Returns:
            The updated cinema domain model
        """
        pass

    @abstractmethod
    async def delete(self, cinema_id: str, session: AsyncSession) -> bool:
        """Delete a cinema record.

        Args:
            cinema_id: The ID of the cinema to delete
            session: The database session to use

        Returns:
            True if the cinema was deleted, False otherwise
        """
        pass
