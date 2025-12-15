from typing import Sequence, List

from src.domain.models.booking import Booking
from src.infrastructure.database.models.booking_entity import BookingEntity
from src.domain.enums.booking_status import BookingStatus


class BookingEntityMapper:

    @staticmethod
    def from_domain(booking: Booking) -> BookingEntity:
        return BookingEntity(
            id=booking.id,
            user_id=booking.user_id,
            status=booking.status.value,
            created_at=booking.created_at,
            paid_at=booking.paid_at,
            total_price=booking.total_price,
            payment_method_id=booking.payment_method_id,
            voucher_id=booking.voucher_id,
            payment_reference=booking.payment_reference,
        )

    @staticmethod
    def to_domain(entity: BookingEntity) -> Booking:
        return Booking(
            id=entity.id,
            user_id=entity.user_id,
            status=BookingStatus(entity.status),
            created_at=entity.created_at,
            paid_at=entity.paid_at,
            total_price=entity.total_price,
            payment_method_id=entity.payment_method_id,
            voucher_id=entity.voucher_id,
            payment_reference=entity.payment_reference,
        )

    @staticmethod
    def to_domains(entities: Sequence[BookingEntity]) -> List[Booking]:
        return [BookingEntityMapper.to_domain(entity) for entity in entities]
