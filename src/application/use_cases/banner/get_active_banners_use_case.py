from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.domain.models.banner import Banner
from src.domain.repositories.banner_repository import BannerRepository


class GetActiveBannersUseCase:
    """Use case for retrieving all active banners."""

    def __init__(
        self,
        banner_repository: BannerRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._banner_repository = banner_repository
        self._sessionmaker = sessionmaker

    async def execute(self) -> list[Banner]:
        """Execute the use case to retrieve all active banners.
        Returns:
            A list of active banner domain models ordered by priority
        """
        async with self._sessionmaker() as session:
            return await self._banner_repository.get_active_banners(session)
