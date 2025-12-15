from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.domain.models.banner import Banner
from src.domain.repositories.banner_repository import BannerRepository


class UpdateBannerUseCase:
    """Use case for updating an existing banner."""

    def __init__(
        self,
        banner_repository: BannerRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._banner_repository = banner_repository
        self._sessionmaker = sessionmaker

    async def execute(self, banner_id: str, **updates) -> Banner:
        """Execute the use case to update a banner.
        Args:
            banner_id: The ID of the banner to update
            **updates: The fields to update
        Returns:
            The updated banner domain model
        Raises:
            ValueError: If banner is not found
        """
        async with self._sessionmaker() as session:
            async with session.begin():
                # Get existing banner
                existing_banner = await self._banner_repository.get_by_id(
                    banner_id, session
                )
                if not existing_banner:
                    raise ValueError(f"Banner with id {banner_id} not found")
                # Update fields
                for key, value in updates.items():
                    if hasattr(existing_banner, key):
                        setattr(existing_banner, key, value)
                # Save updated banner
                updated_banner = await self._banner_repository.update(
                    existing_banner, session
                )
                return updated_banner
