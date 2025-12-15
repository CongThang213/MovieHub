import uuid
from io import BytesIO
from typing import Optional

import cloudinary
import cloudinary.api
import cloudinary.uploader

from config.app_config import AppSettings
from config.logging_config import logger
from src.application.exceptions.image_exceptions import (
    ImageDeletionException,
    ImageUploadException,
    ImageSizeLimitExceededException,
)
from src.application.services.image_service import ImageService
from src.domain.models.image import ImageType, Image


class CloudinaryImageService(ImageService):
    """Cloudinary service that works with database-driven image metadata."""

    def __init__(self, config: AppSettings):
        self._config = config

        # Define transformations for different image types based on config.
        self._transformations = {
            ImageType.AVATAR: {
                "width": self._config.cloudinary.AVATAR_SIZE[0],
                "height": self._config.cloudinary.AVATAR_SIZE[1],
                "crop": "fill",
                "gravity": "face",
                "quality": "auto:good",
                "fetch_format": "auto",
            },
            ImageType.FILM_THUMBNAIL: {
                "width": self._config.cloudinary.THUMBNAIL_SIZE[0],
                "height": self._config.cloudinary.THUMBNAIL_SIZE[1],
                "crop": "fill",
                "gravity": "center",
                "quality": "auto:good",
                "fetch_format": "auto",
            },
            ImageType.FILM_BACKGROUND: {
                "width": self._config.cloudinary.BACKGROUND_SIZE[0],
                "height": self._config.cloudinary.BACKGROUND_SIZE[1],
                "crop": "fill",
                "gravity": "center",
                "quality": "auto:best",
                "fetch_format": "auto",
            },
            ImageType.FILM_POSTER: {
                "width": self._config.cloudinary.POSTER_SIZE[0],
                "height": self._config.cloudinary.POSTER_SIZE[1],
                "crop": "fill",
                "gravity": "center",
                "quality": "auto:good",
                "fetch_format": "auto",
            },
        }

    async def upload_temporary_image(
        self, image_data: bytes, image_type: ImageType
    ) -> Image:
        """
        Upload image to temporary folder in Cloudinary.

        Args:
            image_data: Binary image data
            image_type: Type of image (avatar, film_thumbnail, etc.)

        Returns:
            Image domain model with metadata about the uploaded image.
        """
        try:
            # Generate unique ID for the image
            image_id = str(uuid.uuid4())

            # Create public_id for temp folder
            public_id = f"t/{image_type.value}/{image_id}"

            # Get transformation for this image type
            transformation = self._transformations.get(image_type, {})

            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                file=BytesIO(image_data),
                public_id=public_id,
                transformation=transformation,
                resource_type="image",
                overwrite=True,
            )

            # Create and return Image domain model
            return Image(
                id=image_id,
                owner_id=None,
                type=image_type,
                public_id=result["public_id"],
                url=result["secure_url"],
                is_temp=True,
            )
        except Exception as e:
            if "File size exceeds" in str(e) or "too large" in str(e):
                raise ImageSizeLimitExceededException(
                    message="The image size exceeds provider limit",
                    detail={
                        "provider": "Cloudinary",
                        "method": "upload_temporary_image",
                        "image_type": image_type.value,
                    },
                ) from e

            raise ImageUploadException(
                message=f"There was an error uploading the image: {str(e)}",
                details={
                    "provider": "Cloudinary",
                    "method": "upload_temporary_image",
                    "image_type": image_type.value,
                },
            ) from e

    async def upload_permanent_image(
        self, image_data: bytes, image_type: ImageType, owner_id: str
    ) -> Image:
        """
        Upload image directly to permanent storage in Cloudinary.

        This skips the temporary step and uploads directly to p/{type}/{image_id}.

        Args:
            image_data: Binary image data
            image_type: Type of image (avatar, film_thumbnail, etc.)
            owner_id: ID of the entity that owns this image

        Returns:
            Image domain model with metadata about the uploaded image.
        """
        try:
            # Generate unique ID for the image
            image_id = str(uuid.uuid4())

            # Create public_id for permanent folder
            public_id = f"p/{image_type.value}/{image_id}"

            # Get transformation for this image type
            transformation = self._transformations.get(image_type, {})

            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                file=BytesIO(image_data),
                public_id=public_id,
                transformation=transformation,
                resource_type="image",
                overwrite=True,
            )

            # Create and return Image domain model
            return Image(
                id=image_id,
                owner_id=owner_id,
                type=image_type,
                public_id=result["public_id"],
                url=result["secure_url"],
                is_temp=False,
            )
        except Exception as e:
            if "File size exceeds" in str(e) or "too large" in str(e):
                raise ImageSizeLimitExceededException(
                    message="The image size exceeds provider limit",
                    detail={
                        "provider": "Cloudinary",
                        "method": "upload_permanent_image",
                        "image_type": image_type.value,
                    },
                ) from e

            raise ImageUploadException(
                message=f"There was an error uploading the image: {str(e)}",
                details={
                    "provider": "Cloudinary",
                    "method": "upload_permanent_image",
                    "image_type": image_type.value,
                },
            ) from e

    async def move_to_permanent(
        self, entity_id: Optional[str], temp_image_ids: list[str]
    ) -> list[Image]:
        """Promote temporary images to permanent storage for an entity.

        This moves images from t/{type}/... to p/{type}/... in Cloudinary.

        Args:
            entity_id: ID of the entity (user, film, etc.)
            temp_image_ids: List of temporary image public IDs to promote

        Returns:
            List of successfully promoted images with updated metadata.
            May be shorter than input list if some promotions failed.
        """
        promoted_images = []

        for temp_public_id in temp_image_ids:
            # Split to get data parts from temp_public_id
            # Example: ["t", "avatar", "{image_id}"]
            data_parts = temp_public_id.split("/", 2)
            if len(data_parts) != 3 or data_parts[0] != "t":
                logger.error(f"Invalid temporary public_id format: {temp_public_id}")
                continue

            # Example for permanent_public_id: p/avatar/{owner_id}
            permanent_public_id = f"p/{data_parts[1]}/{data_parts[2]}"

            try:
                # Get transformation for this image type
                transformation = self._transformations.get(data_parts[1], {})

                # Get temporary image resource through Cloudinary API
                temp_image_resource = cloudinary.api.resource(temp_public_id)

                result = cloudinary.uploader.upload(
                    file=temp_image_resource["secure_url"],
                    public_id=permanent_public_id,
                    transformation=transformation,
                    resource_type="image",
                    overwrite=True,
                )

                # Delete the temporary image after successful upload
                try:
                    cloudinary.uploader.destroy(temp_public_id)
                except Exception as delete_error:
                    logger.error(
                        f"Failed to delete temporary image {temp_public_id}, but promotion was successful",
                        exc_info=delete_error,
                    )

                # Create Image domain model for the promoted image
                image = Image(
                    id=data_parts[2],
                    owner_id=entity_id,
                    type=ImageType(data_parts[1]),
                    public_id=result["public_id"],
                    url=result["secure_url"],
                    is_temp=False,
                )
                promoted_images.append(image)  # Add to results

            except Exception as e:
                logger.error(
                    f"Failed to promote image {temp_public_id} to permanent storage",
                    exc_info=e,
                )

        return promoted_images

    async def delete_image(self, public_id: str) -> None:
        """Delete an image from Cloudinary.

        Args:
            public_id: The public ID of the image to delete.

        Raises:
            ImageStorageException: If there was an error during deletion.
        """
        try:
            cloudinary.uploader.destroy(public_id)
        except Exception as e:
            logger.error("Failed to delete image from Cloudinary", exc_info=e)
            raise ImageDeletionException(
                "There was an error deleting the image in Cloudinary"
            ) from e
