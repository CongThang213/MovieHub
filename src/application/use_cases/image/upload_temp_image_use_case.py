from typing import List, Tuple, Dict, Any, NamedTuple

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from config.logging_config import logger
from src.application.exceptions.image_exceptions import (
    ImageUploadException,
    ImageSizeLimitExceededException,
)
from src.application.services.image_service import ImageService
from src.domain.models.image import ImageType, Image
from src.domain.repositories.image_repository import ImageRepository


class UploadResult(NamedTuple):
    """Container for upload operation results with both successful and failed uploads"""

    successful: List[Image]
    failed: List[Dict[str, Any]]


class UploadTempImagesUseCase:
    def __init__(
        self,
        image_service: ImageService,
        image_repository: ImageRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._image_service = image_service
        self._image_repository = image_repository
        self._sessionmaker = sessionmaker

    async def execute(
        self, paired_images: List[Tuple[bytes, ImageType, str]]
    ) -> UploadResult:
        """
        Upload multiple temporary images and save their metadata in the database.

        Args:
            paired_images: List of tuples containing image data (bytes), its type (ImageType), and filename.

        Returns:
            UploadResult containing both successful and failed image uploads.
        """
        uploaded_images = []
        saved_images = []
        failed_images = []

        # First upload all images to the storage provider
        for image_content, image_type, filename in paired_images:
            try:
                uploaded_image = await self._image_service.upload_temporary_image(
                    image_content, image_type
                )
                uploaded_images.append((filename, uploaded_image))
            except ImageSizeLimitExceededException as e:
                failed_images.append(
                    {
                        "type": image_type,
                        "error": "The image size exceeds the limit",
                        "filename": filename,
                    }
                )
                logger.error(f"Image size limit exceeded for {filename}: {str(e)}")
            except ImageUploadException as e:
                failed_images.append(
                    {
                        "type": image_type,
                        "error": "There was an error during uploading",
                        "filename": filename,
                    }
                )
                logger.error(f"Image upload failed for {filename}: {str(e)}")

        # Then save all images to the database in a single transaction
        if uploaded_images:
            try:
                async with self._sessionmaker() as session:
                    try:
                        for filename, uploaded_image in uploaded_images:
                            saved_image = await self._image_repository.create(
                                uploaded_image, session
                            )
                            saved_image.url = uploaded_image.url  # Ensure URL is set
                            saved_images.append(saved_image)

                        await session.commit()
                    except Exception as e:
                        await session.rollback()

                        # Clean up the uploaded images from storage
                        await self._cleanup_uploaded_images(uploaded_images)

                        # Add all as failed if database transaction fails
                        for filename, uploaded_image in uploaded_images:
                            failed_images.append(
                                {
                                    "type": uploaded_image.type,
                                    "error": "There was an error during uploading image",
                                    "filename": filename,
                                }
                            )
                            logger.error(f"Database error while saving image: {str(e)}")

                        saved_images = []  # Clear saved images since transaction failed
            except Exception as e:
                # If overall operation fails, clean up any uploaded images
                await self._cleanup_uploaded_images(uploaded_images)

                logger.error(f"Unexpected error during image upload process: {str(e)}")
                raise ImageUploadException(
                    message="There was an unexpected error during image upload, please try again",
                    details={"error": str(e)},
                ) from e

        return UploadResult(successful=saved_images, failed=failed_images)

    async def _cleanup_uploaded_images(self, images: List[Tuple[str, Image]]) -> None:
        """Helper method to delete uploaded images from storage in case of errors"""
        for filename, image in images:
            try:
                if hasattr(image, "public_id") and image.public_id:
                    await self._image_service.delete_image(image.public_id)
            except Exception as e:
                logger.error(
                    f"Failed to clean up image {image.public_id} after error: {str(e)}"
                )
                pass
