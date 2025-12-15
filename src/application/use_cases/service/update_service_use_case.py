from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.service import Service
from src.domain.repositories.service_repository import ServiceRepository


class UpdateServiceUseCase:
    """Use case for updating a service."""

    def __init__(
        self,
        service_repository: ServiceRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._service_repository = service_repository
        self._sessionmaker = sessionmaker

    async def execute(self, service: Service) -> Service:
        """Execute the use case to update a service."""
        async with self._sessionmaker() as session:
            result = await self._service_repository.update(service, session)
            await session.commit()
            return result
