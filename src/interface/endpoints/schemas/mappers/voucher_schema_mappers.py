from datetime import datetime

from src.domain.models.voucher import Voucher
from src.interface.endpoints.schemas.voucher_schemas import (
    VoucherSchema,
)


class VoucherSchemaMappers:
    @staticmethod
    def to_domain(schema, voucher_id: str = None) -> Voucher:
        """Map schema objects to Voucher domain model.

        Args:
            schema: The schema object to map (e.g., VoucherCreateRequest, VoucherUpdateRequest).
            voucher_id: Optional voucher ID for updates.

        Returns:
            The corresponding Voucher domain model instance.
        """
        # Default values for optional fields
        valid_from = getattr(schema, "valid_from", None) or datetime.now()
        valid_until = getattr(schema, "valid_until", None)
        max_usage = getattr(schema, "max_usage", 1)
        used_count = getattr(schema, "used_count", 0)

        if voucher_id:
            # For update requests
            return Voucher(
                id=voucher_id,
                code=schema.code if hasattr(schema, "code") and schema.code else "",
                discount_rate=(
                    schema.discount_rate
                    if hasattr(schema, "discount_rate")
                    and schema.discount_rate is not None
                    else 0.0
                ),
                valid_from=(
                    schema.valid_from
                    if hasattr(schema, "valid_from") and schema.valid_from
                    else valid_from
                ),
                valid_until=(
                    schema.valid_until
                    if hasattr(schema, "valid_until")
                    else valid_until
                ),
                max_usage=(
                    schema.max_usage
                    if hasattr(schema, "max_usage") and schema.max_usage is not None
                    else max_usage
                ),
                used_count=(
                    schema.used_count
                    if hasattr(schema, "used_count") and schema.used_count is not None
                    else used_count
                ),
            )
        elif hasattr(schema, "id"):
            # For schemas with ID
            return Voucher(
                id=schema.id,
                code=schema.code,
                discount_rate=schema.discount_rate,
                valid_from=schema.valid_from if schema.valid_from else valid_from,
                valid_until=schema.valid_until,
                max_usage=(
                    schema.max_usage if hasattr(schema, "max_usage") else max_usage
                ),
                used_count=(
                    schema.used_count if hasattr(schema, "used_count") else used_count
                ),
            )
        else:
            # For create requests
            return Voucher(
                code=schema.code,
                discount_rate=schema.discount_rate,
                valid_from=schema.valid_from if schema.valid_from else valid_from,
                valid_until=schema.valid_until,
                max_usage=(
                    schema.max_usage if hasattr(schema, "max_usage") else max_usage
                ),
                used_count=used_count,
            )

    @staticmethod
    def from_domain(voucher: Voucher) -> VoucherSchema:
        """Map Voucher domain model to VoucherSchema.

        Args:
            voucher: The Voucher domain model instance to map.

        Returns:
            The corresponding VoucherSchema instance.
        """
        return VoucherSchema(
            id=voucher.id,
            code=voucher.code,
            discount_rate=voucher.discount_rate,
            valid_from=voucher.valid_from,
            valid_until=voucher.valid_until,
            max_usage=voucher.max_usage,
            used_count=voucher.used_count,
        )

    @staticmethod
    def from_domains(vouchers: list[Voucher]) -> list[VoucherSchema]:
        """Map a list of Voucher domain models to a list of VoucherSchemas.

        Args:
            vouchers: The list of Voucher domain model instances to map.

        Returns:
            A list of corresponding VoucherSchema instances.
        """
        return [VoucherSchemaMappers.from_domain(voucher) for voucher in vouchers]
