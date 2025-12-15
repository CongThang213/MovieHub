from datetime import datetime, timedelta
from typing import List, Optional, Any

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.image_exceptions import ImageNotFoundException
from src.domain.models.image import Image, ImageType
from src.domain.repositories.image_repository import ImageRepository
from src.infrastructure.database.models.image_entity import ImageEntity
from src.infrastructure.database.models.mappers.image_entity_mappers import (
    ImageEntityMappers,
)


class ImageRepositoryImpl(ImageRepository):
    """Implementation of the image repository using SQLAlchemy."""

    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        """Initialize the image repository with a session factory.

        Args:
            sessionmaker: Factory for creating database sessions
        """
        self._sessionmaker = sessionmaker

    async def create(self, image: Image, session: AsyncSession) -> Image:
        """Create a new image record.

        Args:
            image: The image domain model to create
            session: The database session to use

        Returns:
            The created image domain model with ID populated
        """

        # Create entity from domain model
        image_entity = ImageEntityMappers.from_model(image)

        # Add to session and flush to get generated values
        session.add(image_entity)
        await session.flush()

        # Return domain model from updated entity
        return ImageEntityMappers.to_model(image_entity)

    async def get_by_public_id(
        self, public_id: str, session: AsyncSession
    ) -> Optional[Image]:
        """Get an image by public ID provided by storage service.

        Args:
            public_id: The public ID of an image from storage service
            session: The database session to use

        Returns:
            The image domain model or None if not found
        """
        result = await session.execute(
            select(ImageEntity).where(ImageEntity.public_id == public_id)
        )
        # Check if there are multiple results for the same ID
        # This should not happen if the database is consistent
        image_entity = result.scalar_one_or_none()

        # Return domain model or None if not found
        return ImageEntityMappers.to_model(image_entity) if image_entity else None

    async def get_by_owner_and_type(
        self, owner_id: str, image_type: ImageType, session: AsyncSession
    ) -> Optional[Image]:
        """Get image by owner ID and type, only return non-temporary images here.

        Args:
            owner_id: The owner ID to look up
            image_type: The type of image to look up
            session: The database session to use

        Returns:
            The image domain model or None if not found
        """
        result = await session.execute(
            select(ImageEntity).where(
                and_(
                    ImageEntity.owner_id == owner_id,
                    ImageEntity.type == image_type,
                    ImageEntity.is_temp == False,
                )
            )
        )
        image_entity = result.scalar_one_or_none()

        # Return domain model or None if not found
        return ImageEntityMappers.to_model(image_entity) if image_entity else None

    # async def get_temp_images_by_type(self, image_type: ImageType) -> List[Image]:
    #     """Get all temporary images of a specific type."""
    #     result = await self._sessionmaker.execute(
    #         select(ImageEntity).where(
    #             and_(ImageEntity.type == image_type, ImageEntity.is_temp == True)
    #         )
    #     )
    #     entities = result.scalars().all()
    #     return [self._entity_to_domain(entity) for entity in entities]

    async def get_expired_temp_images(
        self, session: AsyncSession, hours: int = 12
    ) -> List[Image]:
        """Get all expired temporary images.

        Args:
            session: The database session to use
            hours: Number of hours after which temp images are considered expired

        Returns:
            List of expired temporary image domain models
        """

        # Calculate the cutoff time for expiration by subtracting hours from current time.
        expiry_time = datetime.now() - timedelta(hours=hours)
        result = await session.execute(
            select(ImageEntity).where(
                and_(
                    ImageEntity.is_temp == True,  # Only temporary images
                    ImageEntity.created_at < expiry_time,  # Created before expiry time
                )
            )
        )
        image_entities = result.scalars().all()
        # Return the list of domain models
        return ImageEntityMappers.to_models(image_entities)

    async def update(
        self, image_id: str, session: AsyncSession, **kwargs: Any
    ) -> Image:
        """Update an existing image record.

        Args:
            image_id: The ID of the image to update
            session: The database session to use
            **kwargs: Fields to update on the image

        Keyword Args:
            owner_id: New owner ID
            type: New image type
            public_id: New public ID in storage service
            url: New URL of the image in storage service
            is_temp: Whether the image is temporary

        Returns:
            The updated image domain model

        Raises:
            ImageNotFoundException: If image with given ID is not found
        """
        result = await session.execute(
            select(ImageEntity).where(ImageEntity.id == image_id)
        )
        image_entity = result.scalar_one_or_none()

        # If the image_entity does not exist, raise an exception
        if not image_entity:
            raise ImageNotFoundException(image_id=image_id)

        # Update entity fields based on provided kwargs if they are not None
        for attr, value in kwargs.items():
            if value is not None and hasattr(image_entity, attr):
                setattr(image_entity, attr, value)

        await session.flush()  # Flush to ensure ORM updates

        # Return domain model from updated entity
        return ImageEntityMappers.to_model(image_entity)

    async def delete(self, image_id: str, session: AsyncSession) -> None:
        """Delete an image record.

        Args:
            image_id: The ID of the image to delete
            session: The database session to use

        Raises:
            ImageNotFoundException: If image with given ID is not found
        """
        result = await session.execute(
            select(ImageEntity).where(ImageEntity.id == image_id)
        )
        image_entity = result.scalar_one_or_none()

        if not image_entity:
            raise ImageNotFoundException(image_id=image_id)

        await session.delete(image_entity)

    async def get_all_by_owner(
        self, owner_id: str, session: AsyncSession
    ) -> List[Image]:
        """Get all images for a specific owner.

        Args:
            owner_id: The owner ID to look up
            session: The database session to use

        Returns:
            List of image domain models for the owner
        """
        result = await session.execute(
            select(ImageEntity).where(
                and_(ImageEntity.owner_id == owner_id, ImageEntity.is_temp == False)
            )
        )
        image_entities = result.scalars().all()
        return ImageEntityMappers.to_models(image_entities)
