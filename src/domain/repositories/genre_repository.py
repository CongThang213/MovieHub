from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.genre import Genre


class GenreRepository(ABC):
    """Interface for genre repository operations."""

    @abstractmethod
    async def create(self, genre: Genre, session: AsyncSession) -> Genre:
        """Create a new genre record.

        Args:
            genre: The genre domain model to create
            session: The database session to use

        Returns:
            The created genre domain model with ID populated
        """
        pass

    @abstractmethod
    async def get_by_id(self, genre_id: str, session: AsyncSession) -> Optional[Genre]:
        """Get genre by ID.

        Args:
            genre_id: The ID of the genre to retrieve
            session: The database session to use

        Returns:
            The genre domain model or None if not found
        """
        pass

    @abstractmethod
    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Genre]:
        """Get all genres with pagination.

        Args:
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.

        Returns:
            A list of genre domain models for the specified page
        """
        pass

    @abstractmethod
    async def get_all_genres(self, session) -> list["Genre"]:
        """Get all genres without pagination."""
        pass

    @abstractmethod
    async def update(self, genre_id: str, session: AsyncSession, **kwargs) -> Genre:
        """Update an existing genre record.

        Args:
            genre_id: The ID of the genre to update
            session: The database session to use
            **kwargs: Fields to update (e.g., name)

        Returns:
            The updated genre domain model
        """
        pass

    @abstractmethod
    async def delete(self, genre_id: str, session: AsyncSession) -> None:
        """Delete a genre record.

        Args:
            genre_id: The ID of the genre to delete
            session: The database session to use
        """
        pass
