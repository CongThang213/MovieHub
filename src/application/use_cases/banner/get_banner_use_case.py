from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.domain.models.banner import Banner
from src.domain.repositories.banner_repository import BannerRepository


class GetBannerUseCase:
    """Use case for retrieving a banner by ID."""

    def __init__(
        self,
        banner_repository: BannerRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._banner_repository = banner_repository
        self._sessionmaker = sessionmaker

    async def execute(self, banner_id: str) -> Optional[Banner]:
        """Execute the use case to retrieve a banner by ID.
        Args:
            banner_id: The ID of the banner to retrieve
        Returns:
            The banner domain model if found, None otherwise
        """
        async with self._sessionmaker() as session:
            return await self._banner_repository.get_by_id(banner_id, session)
