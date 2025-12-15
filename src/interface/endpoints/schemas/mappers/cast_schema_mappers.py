from typing import List

from src.domain.models.cast import Cast
from src.interface.endpoints.schemas.cast_schemas import CastSchema


class CastSchemaMappers:
    """Mapper class for converting between Cast domain model and API schemas."""

    @staticmethod
    def from_domain(domain: Cast) -> CastSchema:
        """Convert a Cast domain model to a CastSchema.

        Args:
            domain: The domain model to convert

        Returns:
            The converted schema
        """
        return CastSchema(
            id=domain.id,
            name=domain.name,
            avatar_image_url=domain.avatar_image_url,
            date_of_birth=domain.date_of_birth,
            biography=domain.biography,
        )

    @staticmethod
    def from_domains(domains: List[Cast]) -> List[CastSchema]:
        """Convert a list of Cast domain models to CastSchema objects.

        Args:
            domains: The list of domain models to convert

        Returns:
            A list of converted schemas
        """
        return [CastSchemaMappers.from_domain(domain) for domain in domains]

    @staticmethod
    def to_domain(schema) -> Cast:
        """Convert a CastCreateRequest schema to a Cast domain model.

        Args:
            schema: The schema to convert (e.g., CastCreateRequest)

        Returns:
            The converted domain model
        """
        return (
            Cast(
                id=schema.id,
                name=schema.name,
                avatar_image_url=getattr(schema, "avatar_image_url", None),
                date_of_birth=schema.date_of_birth,
                biography=schema.biography,
            )
            if hasattr(schema, "id")
            else Cast(
                name=schema.name,
                avatar_image_url=getattr(schema, "avatar_image_url", None),
                date_of_birth=schema.date_of_birth,
                biography=schema.biography,
            )
        )
