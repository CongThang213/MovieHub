from src.domain.models.hall import Hall
from src.infrastructure.database.models.hall_entity import HallEntity


class HallEntityMappers:
    @staticmethod
    def from_domain(hall: Hall) -> HallEntity:
        """Map a Hall domain model to a HallEntity.

        Args:
            hall: The Hall domain model to map

        Returns:
            The corresponding HallEntity
        """
        return HallEntity(
            id=hall.id,
            cinema_id=hall.cinema_id,
            name=hall.name,
            capacity=hall.capacity,
            description=hall.description,
        )

    @staticmethod
    def to_domain(hall_entity: HallEntity) -> Hall:
        """Map a HallEntity to a Hall domain model.

        Args:
            hall_entity: The HallEntity to map

        Returns:
            The corresponding Hall domain model
        """
        return Hall(
            id=hall_entity.id,
            cinema_id=hall_entity.cinema_id,
            name=hall_entity.name,
            capacity=hall_entity.capacity or 0,
            description=hall_entity.description,
        )

    @staticmethod
    def to_domains(hall_entities: list[HallEntity]) -> list[Hall]:
        """Map a list of HallEntity to a list of Hall domain models.

        Args:
            hall_entities: The list of HallEntity to map

        Returns:
            The corresponding list of Hall domain models
        """
        return [HallEntityMappers.to_domain(entity) for entity in hall_entities]
