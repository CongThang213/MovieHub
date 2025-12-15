from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.banner import Banner


class BannerRepository(ABC):
    """Interface for banner repository operations."""

    @abstractmethod
    async def create(self, banner: Banner, session: AsyncSession) -> Banner:
        """Create a new banner record.

        Args:
            banner: The banner domain model to create
            session: The database session to use

        Returns:
            The created banner domain model with ID populated
        """
        pass

    @abstractmethod
    async def get_by_id(
        self, banner_id: str, session: AsyncSession
    ) -> Optional[Banner]:
        """Get banner by ID.

        Args:
            banner_id: The ID of the banner to retrieve
            session: The database session to use

        Returns:
            The banner domain model or None if not found
        """
        pass

    @abstractmethod
    async def update(self, banner: Banner, session: AsyncSession) -> Banner:
        """Update an existing banner record.

        Args:
            banner: The banner domain model with updated data
            session: The database session to use

        Returns:
            The updated banner domain model
        """
        pass

    @abstractmethod
    async def delete(self, banner_id: str, session: AsyncSession) -> bool:
        """Delete a banner by ID.

        Args:
            banner_id: The ID of the banner to delete
            session: The database session to use

        Returns:
            True if deleted successfully, False otherwise
        """
        pass

    @abstractmethod
    async def get_active_banners(self, session: AsyncSession) -> list[Banner]:
        """Get all currently active banners ordered by priority.

        Args:
            session: The database session to use

        Returns:
            A list of active banner domain models ordered by priority (descending)
        """
        pass
