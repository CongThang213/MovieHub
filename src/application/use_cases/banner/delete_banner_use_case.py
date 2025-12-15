from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.domain.repositories.banner_repository import BannerRepository


class DeleteBannerUseCase:
    """Use case for deleting a banner."""

    def __init__(
        self,
        banner_repository: BannerRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._banner_repository = banner_repository
        self._sessionmaker = sessionmaker

    async def execute(self, banner_id: str) -> bool:
        """Execute the use case to delete a banner.
        Args:
            banner_id: The ID of the banner to delete
        Returns:
            True if deleted successfully
        Raises:
            ValueError: If banner is not found
        """
        async with self._sessionmaker() as session:
            async with session.begin():
                # Check if banner exists
                existing_banner = await self._banner_repository.get_by_id(
                    banner_id, session
                )
                if not existing_banner:
                    raise ValueError(f"Banner with id {banner_id} not found")
                # Delete banner
                success = await self._banner_repository.delete(banner_id, session)
                return success
