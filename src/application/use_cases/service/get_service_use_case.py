from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.service_exceptions import ServiceNotFoundException
from src.domain.models.service import Service
from src.domain.repositories.service_repository import ServiceRepository


class GetServiceUseCase:
    """Use case for retrieving a service by ID."""

    def __init__(
        self,
        service_repository: ServiceRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._service_repository = service_repository
        self._sessionmaker = sessionmaker

    async def execute(self, service_id: str) -> Service:
        """Execute the use case to get a service by ID."""
        async with self._sessionmaker() as session:
            result = await self._service_repository.get_by_id(service_id, session)
            if not result:
                raise ServiceNotFoundException(service_id)
            return result
