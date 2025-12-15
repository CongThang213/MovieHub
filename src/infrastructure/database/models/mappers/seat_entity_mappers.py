from sqlalchemy import inspect as sa_inspect

from src.domain.models.seat import Seat
from src.infrastructure.database.models.mappers.seat_category_entity_mappers import (
    SeatCategoryEntityMappers,
)
from src.infrastructure.database.models.seat_entity import SeatEntity


class SeatEntityMappers:
    @staticmethod
    def from_domain(seat: Seat) -> SeatEntity:
        """Map a Seat domain model to a SeatEntity.

        Args:
            seat: The Seat domain model to map

        Returns:
            The corresponding SeatEntity
        """
        return SeatEntity(
            id=seat.id,
            row_id=seat.row_id,
            category_id=seat.category_id,
            seat_number=seat.seat_number,
            pos_x=seat.pos_x,
            pos_y=seat.pos_y,
            is_accessible=seat.is_accessible,
            external_label=seat.external_label,
        )

    @staticmethod
    def to_domain(seat_entity: SeatEntity) -> Seat:
        """Map a SeatEntity to a Seat domain model.

        Args:
            seat_entity: The SeatEntity to map

        Returns:
            The corresponding Seat domain model
        """
        # Map category if it's loaded (check without triggering lazy load)
        category = None
        insp = sa_inspect(seat_entity)
        if "category" in insp.unloaded:
            # Relationship is not loaded, leave category as None
            pass
        elif seat_entity.category is not None:
            # Relationship is loaded and has a value
            category = SeatCategoryEntityMappers.to_domain(seat_entity.category)

        return Seat(
            id=seat_entity.id,
            row_id=seat_entity.row_id,
            category_id=seat_entity.category_id,
            seat_number=seat_entity.seat_number or 0,
            pos_x=seat_entity.pos_x or 0.0,
            pos_y=seat_entity.pos_y or 0.0,
            is_accessible=seat_entity.is_accessible or False,
            external_label=seat_entity.external_label,
            category=category,
        )

    @staticmethod
    def to_domains(seat_entities: list[SeatEntity]) -> list[Seat]:
        """Map a list of SeatEntity to a list of Seat domain models.

        Args:
            seat_entities: The list of SeatEntity to map

        Returns:
            The corresponding list of Seat domain models
        """
        return [SeatEntityMappers.to_domain(entity) for entity in seat_entities]
