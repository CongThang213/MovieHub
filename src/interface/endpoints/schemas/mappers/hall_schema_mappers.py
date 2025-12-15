from src.domain.models.hall import Hall
from src.interface.endpoints.schemas.hall_schemas import HallSchema


class HallSchemaMappers:
    @staticmethod
    def to_domain(schema, hall_id: str = None) -> Hall:
        """Map schema objects to Hall domain model.

        Args:
            schema: The schema object to map (e.g., HallCreateRequest, HallUpdateRequest).
            hall_id: Optional hall ID for updates.

        Returns:
            The corresponding Hall domain model instance.
        """
        # Only set id if hall_id is provided (for updates), otherwise let Hall generate it
        hall_data = {
            "cinema_id": getattr(schema, "cinema_id", None),
            "name": getattr(schema, "name", None) or "",
            "capacity": getattr(schema, "capacity", None) or 0,
            "description": getattr(schema, "description", None),
        }

        if hall_id:
            hall_data["id"] = hall_id

        return Hall(**hall_data)

    @staticmethod
    def from_domain(hall: Hall) -> HallSchema:
        """Map Hall domain model to HallSchema.

        Args:
            hall: The Hall domain model to map

        Returns:
            The corresponding HallSchema
        """
        return HallSchema(
            id=hall.id,
            cinema_id=hall.cinema_id or "",
            name=hall.name,
            capacity=hall.capacity,
            description=hall.description,
        )

    @staticmethod
    def from_domains(halls: list[Hall]) -> list[HallSchema]:
        """Map a list of Hall domain models to a list of HallSchema.

        Args:
            halls: The list of Hall domain models to map

        Returns:
            The corresponding list of HallSchema
        """
        return [HallSchemaMappers.from_domain(hall) for hall in halls]
