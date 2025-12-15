from typing import Optional, List

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from config.logging_config import logger
from src.application.services.image_service import ImageService
from src.domain.exceptions.image_exceptions import ImageNotFoundException
from src.domain.models.image import Image
from src.domain.repositories.image_repository import ImageRepository


class FinalizeTempImagesUseCase:
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
        self, temp_image_ids: List[str], owner_id: Optional[str]
    ) -> list[Image]:
        """Finalize a temporary image by setting its owner and marking it as permanent.

        Args:
            temp_image_ids: List of temporary image IDs to finalize.
            owner_id: The ID of the owner to associate with the image.

        Returns:
            List of finalized Image domain models.
        """
        updated_images = await self._image_service.move_to_permanent(
            owner_id, temp_image_ids
        )

        async with self._sessionmaker() as session:
            for image in updated_images:
                try:
                    await self._image_repository.update(
                        image.id,
                        session,
                        owner_id=owner_id,
                        is_temp=False,
                        url=image.url,
                        public_id=image.public_id,
                    )
                except ImageNotFoundException as e:
                    # Log and continue if image not found in database
                    logger.error(f"Image not found during finalize: {e}")
                    continue

            await session.commit()  # Commit all updates at once

        return updated_images
