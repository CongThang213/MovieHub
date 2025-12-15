from src.domain.models.seat_category import SeatCategory
from src.interface.endpoints.schemas.seat_category_schemas import SeatCategorySchema


class SeatCategorySchemaMappers:
    @staticmethod
    def to_domain(schema, seat_category_id: str = None) -> SeatCategory:
        """Map schema objects to SeatCategory domain model.

        Args:
            schema: The schema object to map (e.g., SeatCategoryCreateRequest, SeatCategoryUpdateRequest).
            seat_category_id: Optional seat category ID for updates.

        Returns:
            The corresponding SeatCategory domain model instance.
        """
        if seat_category_id:
            # PATCH update - preserve None values to indicate "no change"
            seat_category_data = {
                "id": seat_category_id,
                "name": getattr(schema, "name", None) or "",
                "base_price": getattr(schema, "base_price", None),
                "attributes": getattr(schema, "attributes", None),
            }
        else:
            # POST create - use defaults for missing values
            seat_category_data = {
                "name": getattr(schema, "name", None) or "",
                "base_price": getattr(schema, "base_price", None) or 0.0,
                "attributes": getattr(schema, "attributes", None),
            }

        return SeatCategory(**seat_category_data)

    @staticmethod
    def from_domain(seat_category: SeatCategory) -> SeatCategorySchema:
        """Map SeatCategory domain model to SeatCategorySchema.

        Args:
            seat_category: The SeatCategory domain model to map

        Returns:
            The corresponding SeatCategorySchema
        """
        return SeatCategorySchema(
            id=seat_category.id,
            name=seat_category.name,
            base_price=seat_category.base_price,
            attributes=seat_category.attributes,
        )

    @staticmethod
    def from_domains(seat_categories: list[SeatCategory]) -> list[SeatCategorySchema]:
        """Map a list of SeatCategory domain models to a list of SeatCategorySchema.

        Args:
            seat_categories: The list of SeatCategory domain models to map

        Returns:
            The corresponding list of SeatCategorySchema
        """
        return [
            SeatCategorySchemaMappers.from_domain(seat_category)
            for seat_category in seat_categories
        ]
