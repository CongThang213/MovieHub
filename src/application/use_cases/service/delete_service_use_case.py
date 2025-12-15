from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.repositories.service_repository import ServiceRepository


class DeleteServiceUseCase:
    """Use case for deleting a service."""

    def __init__(
        self,
        service_repository: ServiceRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._service_repository = service_repository
        self._sessionmaker = sessionmaker

    async def execute(self, service_id: str) -> None:
        """Execute the use case to delete a service."""
        async with self._sessionmaker() as session:
            await self._service_repository.delete(service_id, session)
            await session.commit()


# Service Use Cases
