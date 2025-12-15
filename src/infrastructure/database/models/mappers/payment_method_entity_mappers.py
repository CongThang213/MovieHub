from src.domain.models.payment_method import PaymentMethod
from src.infrastructure.database.models.payment_method_entity import (
    PaymentMethodEntity,
)


class PaymentMethodEntityMappers:
    @staticmethod
    def from_domain(payment_method: PaymentMethod) -> PaymentMethodEntity:
        """Map a PaymentMethod domain model to a PaymentMethodEntity."""
        return PaymentMethodEntity(
            id=payment_method.id,
            name=payment_method.name,
            active=payment_method.active,
            surcharge=payment_method.surcharge,
        )

    @staticmethod
    def to_domain(payment_method_entity: PaymentMethodEntity) -> PaymentMethod:
        """Map a PaymentMethodEntity to a PaymentMethod domain model."""
        return PaymentMethod(
            id=payment_method_entity.id,
            name=payment_method_entity.name or "",
            active=payment_method_entity.active,
            surcharge=payment_method_entity.surcharge or 0.0,
        )

    @staticmethod
    def to_domains(
        payment_method_entities: list[PaymentMethodEntity],
    ) -> list[PaymentMethod]:
        """Map a list of PaymentMethodEntity to a list of PaymentMethod domain models."""
        return [
            PaymentMethodEntityMappers.to_domain(entity)
            for entity in payment_method_entities
        ]
