from typing import Sequence, List

from src.domain.enums.payment_status import PaymentStatus
from src.domain.models.payment import Payment
from src.infrastructure.database.models.payment_entity import PaymentEntity


class PaymentEntityMapper:

    @staticmethod
    def from_domain(payment: Payment) -> PaymentEntity:
        return PaymentEntity(
            id=payment.id,
            booking_id=payment.booking_id,
            payment_method_id=payment.payment_method_id,
            external_txn_id=payment.external_txn_id,
            amount=payment.amount,
            status=payment.status.value if payment.status else None,
            created_at=payment.created_at,
            confirmed_at=payment.confirmed_at,
            payment_metadata=payment.metadata,
        )

    @staticmethod
    def to_domain(entity: PaymentEntity) -> Payment:
        return Payment(
            id=entity.id,
            booking_id=entity.booking_id,
            payment_method_id=entity.payment_method_id,
            external_txn_id=entity.external_txn_id,
            amount=entity.amount,
            currency="VND",  # Default currency
            status=(
                PaymentStatus(entity.status) if entity.status else PaymentStatus.PENDING
            ),
            created_at=entity.created_at,
            confirmed_at=entity.confirmed_at,
            metadata=entity.payment_metadata or {},
        )

    @staticmethod
    def to_domains(entities: Sequence[PaymentEntity]) -> List[Payment]:
        return [PaymentEntityMapper.to_domain(entity) for entity in entities]
