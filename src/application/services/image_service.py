from abc import ABC
from typing import Optional

from src.domain.models.image import Image, ImageType


class ImageService(ABC):
    async def upload_temporary_image(
        self, image_data: bytes, image_type: ImageType
    ) -> Image:
        """Upload a temporary image to storage service provider

        The image goes to temp/{type}/... folder in storage service.

        Args:
            image_data: Binary image data
            image_type: Type of image (avatar, film_thumbnail, etc.)

        Returns:
            Image domain model with metadata about the uploaded image.
        """
        pass

    async def upload_permanent_image(
        self, image_data: bytes, image_type: ImageType, owner_id: str
    ) -> Image:
        """Upload an image directly to permanent storage.

        The image goes directly to p/{type}/... folder in storage service.
        Use this when you already have an entity_id and want to skip the temporary step.

        Args:
            image_data: Binary image data
            image_type: Type of image (avatar, film_thumbnail, etc.)
            owner_id: ID of the entity (user, film, etc.) that owns this image

        Returns:
            Image domain model with metadata about the uploaded image.
        """
        pass

    async def move_to_permanent(
        self, owner_id: Optional[str], temp_public_ids: list[str]
    ) -> list[Image]:
        """Promote temporary images to permanent storage for an entity.

        This moves images from t/{type}/... to p/{type}/... in storage service

        Args:
            owner_id: ID of the entity (user, film, etc.) or None
            temp_public_ids: List of temporary image public IDs to promote

        Returns:
            List of promoted images with updated metadata.
        """
        pass

    async def delete_image(self, public_id: str) -> None:
        """Delete an image from storage service by its public ID.

        Args:
            public_id: The public ID of the image to delete.
        """
        pass
