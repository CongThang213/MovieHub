from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.domain.models.banner import Banner
from src.domain.repositories.banner_repository import BannerRepository


class CreateBannerUseCase:
    """Use case for creating a new banner."""

    def __init__(
        self,
        banner_repository: BannerRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._banner_repository = banner_repository
        self._sessionmaker = sessionmaker

    async def execute(self, banner: Banner) -> Banner:
        """Execute the use case to create a new banner.
        Args:
            banner: The banner domain model to create
        Returns:
            The created banner domain model
        """
        async with self._sessionmaker() as session:
            async with session.begin():
                created_banner = await self._banner_repository.create(banner, session)
                return created_banner
