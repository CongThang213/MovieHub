from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.service import Service
from src.domain.repositories.service_repository import ServiceRepository


class GetServicesUseCase:
    """Use case for retrieving all services with pagination."""

    def __init__(
        self,
        service_repository: ServiceRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._service_repository = service_repository
        self._sessionmaker = sessionmaker

    async def execute(
        self, page: int = PAGE_DEFAULT, page_size: int = PAGE_SIZE_DEFAULT
    ) -> list[Service]:
        """Execute the use case to get all services."""
        async with self._sessionmaker() as session:
            return await self._service_repository.get_all(session, page, page_size)
