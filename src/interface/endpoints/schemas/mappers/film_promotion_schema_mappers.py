from typing import List

from src.domain.models.film_promotion import FilmPromotion
from src.interface.endpoints.schemas.film_promotion_schemas import (
    FilmPromotionSchema,
)


class FilmPromotionSchemaMappers:
    """Mapper class for converting between FilmPromotion domain model and API schemas."""

    @staticmethod
    def from_domain(domain: FilmPromotion) -> FilmPromotionSchema:
        """Convert a FilmPromotion domain model to a FilmPromotionSchema.

        Args:
            domain: The domain model to convert

        Returns:
            The converted schema
        """
        return FilmPromotionSchema(
            id=domain.id,
            film_id=domain.film_id,
            type=domain.type,
            title=domain.title,
            content=domain.content,
            valid_from=domain.valid_from,
            valid_until=domain.valid_until,
        )

    @staticmethod
    def from_domains(domains: List[FilmPromotion]) -> List[FilmPromotionSchema]:
        """Convert a list of FilmPromotion domain models to FilmPromotionSchema objects.

        Args:
            domains: The list of domain models to convert

        Returns:
            A list of converted schemas
        """
        return [FilmPromotionSchemaMappers.from_domain(domain) for domain in domains]

    @staticmethod
    def to_domain(schema) -> FilmPromotion:
        """Convert a FilmPromotionCreateRequest schema to a FilmPromotion domain model.

        Args:
            schema: The schema to convert (e.g., FilmPromotionCreateRequest)

        Returns:
            The converted domain model
        """
        return (
            FilmPromotion(
                id=schema.id,
                film_id=schema.film_id,
                type=schema.type,
                title=schema.title,
                content=schema.content,
                valid_from=schema.valid_from,
                valid_until=schema.valid_until,
            )
            if hasattr(schema, "id")
            else FilmPromotion(
                film_id=schema.film_id,
                type=schema.type,
                title=schema.title,
                content=schema.content,
                valid_from=schema.valid_from,
                valid_until=schema.valid_until,
            )
        )
