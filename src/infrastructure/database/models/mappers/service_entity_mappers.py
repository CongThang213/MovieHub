from sqlalchemy import inspect

from src.domain.models.service import Service
from src.infrastructure.database.models.service_entity import ServiceEntity


class ServiceEntityMappers:
    @staticmethod
    def from_domain(service: Service) -> ServiceEntity:
        """Map a Service domain model to a ServiceEntity."""
        return ServiceEntity(
            id=service.id,
            name=service.name,
            detail=service.detail,
            price=service.price,
        )

    @staticmethod
    def to_domain(service_entity: ServiceEntity) -> Service:
        """Map a ServiceEntity to a Service domain model."""
        # Get image_url from related image if it exists
        image_url = None

        # Check if the image relationship is loaded to avoid lazy loading
        insp = inspect(service_entity)
        if "image" not in insp.unloaded:
            # The relationship is loaded, safe to access
            if service_entity.image is not None:
                image_url = service_entity.image.url

        return Service(
            id=service_entity.id,
            name=service_entity.name,
            detail=service_entity.detail or "",
            image_url=image_url,
            price=service_entity.price or 0.0,
            is_available=True,  # Default to available
        )

    @staticmethod
    def to_domains(service_entities: list[ServiceEntity]) -> list[Service]:
        """Map a list of ServiceEntity to a list of Service domain models."""
        return [ServiceEntityMappers.to_domain(entity) for entity in service_entities]
