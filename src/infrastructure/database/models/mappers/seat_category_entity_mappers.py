from src.domain.models.seat_category import SeatCategory
from src.infrastructure.database.models.seat_category_entity import SeatCategoryEntity


class SeatCategoryEntityMappers:
    @staticmethod
    def from_domain(seat_category: SeatCategory) -> SeatCategoryEntity:
        """Map a SeatCategory domain model to a SeatCategoryEntity.

        Args:
            seat_category: The SeatCategory domain model to map

        Returns:
            The corresponding SeatCategoryEntity
        """
        return SeatCategoryEntity(
            id=seat_category.id,
            name=seat_category.name,
            base_price=seat_category.base_price,
            attributes=seat_category.attributes,
        )

    @staticmethod
    def to_domain(seat_category_entity: SeatCategoryEntity) -> SeatCategory:
        """Map a SeatCategoryEntity to a SeatCategory domain model.

        Args:
            seat_category_entity: The SeatCategoryEntity to map

        Returns:
            The corresponding SeatCategory domain model
        """
        return SeatCategory(
            id=seat_category_entity.id,
            name=seat_category_entity.name,
            base_price=seat_category_entity.base_price or 0.0,
            attributes=seat_category_entity.attributes,
        )

    @staticmethod
    def to_domains(
        seat_category_entities: list[SeatCategoryEntity],
    ) -> list[SeatCategory]:
        """Map a list of SeatCategoryEntity to a list of SeatCategory domain models.

        Args:
            seat_category_entities: The list of SeatCategoryEntity to map

        Returns:
            The corresponding list of SeatCategory domain models
        """
        return [
            SeatCategoryEntityMappers.to_domain(entity)
            for entity in seat_category_entities
        ]
