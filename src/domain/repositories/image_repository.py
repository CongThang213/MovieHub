from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.image import Image, ImageType


class ImageRepository(ABC):
    """Interface for image repository operations."""

    @abstractmethod
    async def create(self, image: Image, session: AsyncSession) -> Image:
        """Create a new image record."""
        pass

    @abstractmethod
    async def get_by_public_id(
        self, image_id: str, session: AsyncSession
    ) -> Optional[Image]:
        """Get image by ID."""
        pass

    @abstractmethod
    async def get_by_owner_and_type(
        self, owner_id: str, image_type: ImageType, session: AsyncSession
    ) -> Optional[Image]:
        """Get image by owner ID and type."""
        pass

    # @abstractmethod
    # async def get_temp_images_by_type(self, image_type: ImageType) -> List[Image]:
    #     """Get all temporary images of a specific type."""
    #     pass

    @abstractmethod
    async def get_expired_temp_images(
        self, session: AsyncSession, hours: int = 12
    ) -> List[Image]:
        """Get all expired temporary images."""
        pass

    @abstractmethod
    async def update(self, image: Image, session: AsyncSession, **kwargs) -> Image:
        """Update an existing image record."""
        pass

    @abstractmethod
    async def delete(self, image_id: str, session: AsyncSession) -> None:
        """Delete an image record."""
        pass

    @abstractmethod
    async def get_all_by_owner(
        self, owner_id: str, session: AsyncSession
    ) -> List[Image]:
        """Get all images for a specific owner."""
        pass
