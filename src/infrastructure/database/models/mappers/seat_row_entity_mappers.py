from src.domain.models.seat_row import SeatRow
from src.infrastructure.database.models.seat_row_entity import SeatRowEntity


class SeatRowEntityMappers:
    @staticmethod
    def from_domain(seat_row: SeatRow) -> SeatRowEntity:
        """Map a SeatRow domain model to a SeatRowEntity."""
        return SeatRowEntity(
            id=seat_row.id,
            hall_id=seat_row.hall_id,
            row_label=seat_row.row_label,
            row_order=seat_row.row_order,
        )

    @staticmethod
    def to_domain(seat_row_entity: SeatRowEntity) -> SeatRow:
        """Map a SeatRowEntity to a SeatRow domain model."""
        return SeatRow(
            id=seat_row_entity.id,
            hall_id=seat_row_entity.hall_id,
            row_label=seat_row_entity.row_label,
            row_order=seat_row_entity.row_order or 0,
        )

    @staticmethod
    def to_domains(seat_row_entities: list[SeatRowEntity]) -> list[SeatRow]:
        """Map a list of SeatRowEntity to a list of SeatRow domain models."""
        return [SeatRowEntityMappers.to_domain(entity) for entity in seat_row_entities]
