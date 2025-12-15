from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.exceptions.app_exception import DuplicateEntryException
from src.domain.exceptions.service_exceptions import ServiceNotFoundException
from src.domain.models.service import Service
from src.domain.repositories.service_repository import ServiceRepository
from src.infrastructure.database.models.service_entity import ServiceEntity
from src.infrastructure.database.models.mappers.service_entity_mappers import (
    ServiceEntityMappers,
)


class ServiceRepositoryImpl(ServiceRepository):
    """Implementation of the service repository using SQLAlchemy."""

    async def create(self, service: Service, session: AsyncSession) -> Service:
        """Create a new service record."""
        service_entity = ServiceEntityMappers.from_domain(service)
        session.add(service_entity)
        await session.flush()

        # Reload the entity with eager loading to avoid lazy loading issues
        await session.refresh(service_entity, ["image"])

        return ServiceEntityMappers.to_domain(service_entity)

    async def get_by_id(
        self, service_id: str, session: AsyncSession
    ) -> Optional[Service]:
        """Get a service by its ID."""
        result = await session.execute(
            select(ServiceEntity)
            .options(selectinload(ServiceEntity.image))
            .where(ServiceEntity.id == service_id)
        )
        try:
            service_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="Service", identifier=service_id
            ) from e

        return (
            ServiceEntityMappers.to_domain(service_entity) if service_entity else None
        )

    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Service]:
        """Get all services with pagination."""
        offset = (page - 1) * page_size
        result = await session.execute(
            select(ServiceEntity)
            .options(selectinload(ServiceEntity.image))
            .offset(offset)
            .limit(page_size)
        )
        service_entities = result.scalars().all()
        return ServiceEntityMappers.to_domains(service_entities)

    async def update(self, service: Service, session: AsyncSession) -> Service:
        """Update an existing service record."""
        result = await session.execute(
            select(ServiceEntity)
            .options(selectinload(ServiceEntity.image))
            .where(ServiceEntity.id == service.id)
        )
        service_entity = result.scalar_one_or_none()

        if not service_entity:
            raise ServiceNotFoundException(service.id)

        # Update entity attributes
        service_entity.name = service.name
        service_entity.detail = service.detail
        service_entity.price = service.price

        await session.flush()
        await session.refresh(service_entity, ["image"])

        return ServiceEntityMappers.to_domain(service_entity)

    async def delete(self, service_id: str, session: AsyncSession) -> None:
        """Delete a service record."""
        result = await session.execute(
            select(ServiceEntity).where(ServiceEntity.id == service_id)
        )
        service_entity = result.scalar_one_or_none()

        if not service_entity:
            raise ServiceNotFoundException(service_id)

        await session.execute(
            delete(ServiceEntity).where(ServiceEntity.id == service_id)
        )
        await session.flush()
