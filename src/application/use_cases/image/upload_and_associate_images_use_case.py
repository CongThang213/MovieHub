from typing import List, Tuple

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from config.logging_config import logger
from src.application.exceptions.image_exceptions import (
    ImageUploadException,
    ImageSizeLimitExceededException,
)
from src.application.services.image_service import ImageService
from src.application.use_cases.image.upload_temp_image_use_case import UploadResult
from src.domain.models.image import ImageType, Image
from src.domain.repositories.image_repository import ImageRepository


class UploadAndAssociateImagesUseCase:
    """Upload images directly to permanent storage and associate them with an owner entity."""

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
        self, paired_images: List[Tuple[bytes, ImageType, str]], owner_id: str
    ) -> UploadResult:
        """
        Upload images directly to permanent storage and associate with an owner.

        This uploads directly to permanent storage (p/{type}/{id}) without the temporary step.
        Use this when you already have an entity_id and want to upload images directly.

        Args:
            paired_images: List of tuples containing image data (bytes), its type (ImageType), and filename.
            owner_id: The ID of the owner entity to associate the images with.

        Returns:
            UploadResult containing both successful and failed image uploads.
        """
        uploaded_images = []
        saved_images = []
        failed_images = []

        # Upload all images directly to permanent storage
        for image_content, image_type, filename in paired_images:
            try:
                # Upload directly to permanent storage
                permanent_image = await self._image_service.upload_permanent_image(
                    image_content, image_type, owner_id
                )
                uploaded_images.append((filename, permanent_image))
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

        # Save all uploaded images to the database in a single transaction
        if uploaded_images:
            try:
                async with self._sessionmaker() as session:
                    try:
                        for filename, permanent_image in uploaded_images:
                            saved_image = await self._image_repository.create(
                                permanent_image, session
                            )
                            saved_image.url = permanent_image.url  # Ensure URL is set
                            saved_images.append(saved_image)

                        await session.commit()
                    except Exception as e:
                        await session.rollback()

                        # Clean up the uploaded images from storage
                        await self._cleanup_uploaded_images(uploaded_images)

                        # Mark all as failed if database transaction fails
                        for filename, permanent_image in uploaded_images:
                            failed_images.append(
                                {
                                    "type": permanent_image.type,
                                    "error": "Database error during save",
                                    "filename": filename,
                                }
                            )
                        logger.error(f"Database error while saving images: {str(e)}")
                        saved_images = []

            except Exception as e:
                # If overall operation fails, clean up any uploaded images
                await self._cleanup_uploaded_images(uploaded_images)

                logger.error(f"Error during permanent image upload: {str(e)}")
                # Mark all as failed
                for filename, img in uploaded_images:
                    failed_images.append(
                        {
                            "type": img.type,
                            "error": "Failed to upload to permanent storage",
                            "filename": filename,
                        }
                    )

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
