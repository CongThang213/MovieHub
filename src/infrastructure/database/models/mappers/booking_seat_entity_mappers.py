from typing import Sequence, List

from src.domain.models.booking_seat import BookingSeat
from src.infrastructure.database.models.booking_seat_entity import BookingSeatEntity


class BookingSeatEntityMapper:

    @staticmethod
    def from_domain(booking_seat: BookingSeat) -> BookingSeatEntity:
        return BookingSeatEntity(
            id=booking_seat.id,
            booking_id=booking_seat.booking_id,
            showtime_id=booking_seat.showtime_id,
            seat_id=booking_seat.seat_id,
            purchased_at=booking_seat.purchased_at,
            ticket_code=booking_seat.ticket_code,
        )

    @staticmethod
    def to_domain(entity: BookingSeatEntity) -> BookingSeat:
        return BookingSeat(
            id=entity.id,
            booking_id=entity.booking_id,
            showtime_id=entity.showtime_id,
            seat_id=entity.seat_id,
            purchased_at=entity.purchased_at,
            ticket_code=entity.ticket_code,
        )

    @staticmethod
    def to_domains(entities: Sequence[BookingSeatEntity]) -> List[BookingSeat]:
        return [BookingSeatEntityMapper.to_domain(entity) for entity in entities]
