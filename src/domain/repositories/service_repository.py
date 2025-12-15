from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.service import Service


class ServiceRepository(ABC):
    """Interface for service repository operations."""

    @abstractmethod
    async def create(self, service: Service, session: AsyncSession) -> Service:
        """Create a new service record."""
        pass

    @abstractmethod
    async def get_by_id(
        self, service_id: str, session: AsyncSession
    ) -> Optional[Service]:
        """Get service by ID."""
        pass

    @abstractmethod
    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Service]:
        """Get all services with pagination."""
        pass

    @abstractmethod
    async def update(self, service: Service, session: AsyncSession) -> Service:
        """Update an existing service record."""
        pass

    @abstractmethod
    async def delete(self, service_id: str, session: AsyncSession) -> None:
        """Delete a service record."""
        pass


from src.domain.exceptions.app_exception import AppException


class ServiceNotFoundException(AppException):
    def __init__(self, service_id: str):
        """
        Exception raised when a service is not found by ID.
        :param service_id: The ID of the service that was not found.
        """
        super().__init__(
            status_code=404,
            error_code="SERVICE_NOT_FOUND",
            message=f"Service with id {service_id} not found",
            details={"service_id": service_id},
        )


class ServiceAlreadyExistsException(AppException):
    def __init__(self, name: str):
        """
        Exception raised when a service with the same name already exists.
        :param name: The name of the service that already exists.
        """
        super().__init__(
            status_code=409,
            error_code="SERVICE_ALREADY_EXISTS",
            message=f"Service with name '{name}' already exists",
            details={"name": name},
        )
