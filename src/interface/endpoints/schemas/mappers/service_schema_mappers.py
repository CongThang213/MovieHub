from src.domain.models.service import Service
from src.interface.endpoints.schemas.service_schemas import ServiceSchema


class ServiceSchemaMappers:
    @staticmethod
    def to_domain(schema, service_id: str = None) -> Service:
        """Map schema objects to Service domain model."""
        service_data = {
            "name": getattr(schema, "name", ""),
            "detail": getattr(schema, "detail", ""),
            "price": getattr(schema, "price", 0.0),
            "is_available": True,
        }

        if service_id:
            service_data["id"] = service_id

        return Service(**service_data)

    @staticmethod
    def from_domain(service: Service) -> ServiceSchema:
        """Map Service domain model to ServiceSchema."""
        return ServiceSchema(
            id=service.id,
            name=service.name,
            detail=service.detail,
            image_url=service.image_url,
            price=service.price,
            is_available=service.is_available,
        )

    @staticmethod
    def from_domains(services: list[Service]) -> list[ServiceSchema]:
        """Map a list of Service domain models to a list of ServiceSchema."""
        return [ServiceSchemaMappers.from_domain(service) for service in services]
