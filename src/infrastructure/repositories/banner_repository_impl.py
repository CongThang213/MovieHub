from datetime import datetime
from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.exc import MultipleResultsFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.banner import Banner
from src.domain.repositories.banner_repository import BannerRepository
from src.infrastructure.database.models.banner_entity import BannerEntity
from src.infrastructure.database.models.mappers.banner_entity_mappers import (
    BannerEntityMappers,
)


class BannerRepositoryImpl(BannerRepository):
    """Implementation of the banner repository using SQLAlchemy."""

    async def create(self, banner: Banner, session: AsyncSession) -> Banner:
        """Create a new banner record.

        Args:
            banner: The banner domain model to create
            session: The database session to use

        Returns:
            The created banner domain model with ID populated
        """
        banner_entity = BannerEntityMappers.from_domain(banner)
        session.add(banner_entity)
        await session.flush()  # Flush to populate the ID

        return BannerEntityMappers.to_domain(banner_entity)

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
        result = await session.execute(
            select(BannerEntity).where(BannerEntity.id == banner_id)
        )
        try:
            banner_entity = result.scalar_one_or_none()
        except MultipleResultsFound:
            # In case of multiple results, just return the first one
            # This shouldn't happen with a proper primary key constraint
            banner_entity = result.scalars().first()

        return BannerEntityMappers.to_domain(banner_entity) if banner_entity else None

    async def update(self, banner: Banner, session: AsyncSession) -> Banner:
        """Update an existing banner record.

        Args:
            banner: The banner domain model with updated data
            session: The database session to use

        Returns:
            The updated banner domain model
        """
        result = await session.execute(
            select(BannerEntity).where(BannerEntity.id == banner.id)
        )
        banner_entity = result.scalar_one_or_none()

        if not banner_entity:
            raise ValueError(f"Banner with id {banner.id} not found")

        # Update all fields
        banner_entity.image_url = banner.image_url
        banner_entity.fallback_image = banner.fallback_image
        banner_entity.alt_text = banner.alt_text
        banner_entity.title = banner.title
        banner_entity.subtitle = banner.subtitle
        banner_entity.cta_label = banner.cta_label
        banner_entity.target_type = banner.target_type
        banner_entity.target_id = banner.target_id
        banner_entity.priority = banner.priority
        banner_entity.start_at = banner.start_at
        banner_entity.end_at = banner.end_at
        banner_entity.aspect_ratio = banner.aspect_ratio

        await session.flush()

        return BannerEntityMappers.to_domain(banner_entity)

    async def delete(self, banner_id: str, session: AsyncSession) -> bool:
        """Delete a banner by ID.

        Args:
            banner_id: The ID of the banner to delete
            session: The database session to use

        Returns:
            True if deleted successfully, False otherwise
        """
        result = await session.execute(
            delete(BannerEntity).where(BannerEntity.id == banner_id)
        )
        return result.rowcount > 0

    async def get_active_banners(self, session: AsyncSession) -> list[Banner]:
        """Get all currently active banners ordered by priority.

        A banner is active if:
        - Current time is after start_at (or start_at is None)
        - Current time is before end_at (or end_at is None)

        Args:
            session: The database session to use

        Returns:
            A list of active banner domain models ordered by priority (descending)
        """
        now = datetime.now()

        # Build query with filters for active banners
        query = (
            select(BannerEntity)
            .where(
                # start_at is None OR start_at <= now
                (BannerEntity.start_at.is_(None)) | (BannerEntity.start_at <= now),
                # end_at is None OR end_at >= now
                (BannerEntity.end_at.is_(None)) | (BannerEntity.end_at >= now),
            )
            .order_by(BannerEntity.priority.desc())
        )

        result = await session.execute(query)
        banner_entities = result.scalars().all()

        return BannerEntityMappers.to_domains(banner_entities)
