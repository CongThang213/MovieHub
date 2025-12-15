from src.domain.models.payment_method import PaymentMethod
from src.interface.endpoints.schemas.payment_method_schemas import PaymentMethodSchema


class PaymentMethodSchemaMappers:
    @staticmethod
    def to_domain(schema, payment_method_id: str = None) -> PaymentMethod:
        """Map schema objects to PaymentMethod domain model."""
        payment_method_data = {
            "name": getattr(schema, "name", ""),
            "active": getattr(schema, "active", True),
            "surcharge": getattr(schema, "surcharge", 0.0),
        }

        if payment_method_id:
            payment_method_data["id"] = payment_method_id

        return PaymentMethod(**payment_method_data)

    @staticmethod
    def from_domain(payment_method: PaymentMethod) -> PaymentMethodSchema:
        """Map PaymentMethod domain model to PaymentMethodSchema."""
        return PaymentMethodSchema(
            id=payment_method.id,
            name=payment_method.name,
            active=payment_method.active,
            surcharge=payment_method.surcharge,
        )

    @staticmethod
    def from_domains(
        payment_methods: list[PaymentMethod],
    ) -> list[PaymentMethodSchema]:
        """Map a list of PaymentMethod domain models to a list of PaymentMethodSchema."""
        return [
            PaymentMethodSchemaMappers.from_domain(payment_method)
            for payment_method in payment_methods
        ]
