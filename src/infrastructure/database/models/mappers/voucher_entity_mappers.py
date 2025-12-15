from src.domain.models.voucher import Voucher
from src.infrastructure.database.models.voucher_entity import VoucherEntity


class VoucherEntityMappers:
    @staticmethod
    def from_domain(voucher: Voucher) -> VoucherEntity:
        """Map a Voucher domain model to a VoucherEntity.

        Args:
            voucher: The Voucher domain model to map

        Returns:
            The corresponding VoucherEntity
        """
        return VoucherEntity(
            id=voucher.id,
            code=voucher.code,
            discount_rate=voucher.discount_rate,
            valid_from=voucher.valid_from,
            valid_until=voucher.valid_until,
            max_usage=voucher.max_usage,
            used_count=voucher.used_count,
        )

    @staticmethod
    def to_domain(voucher_entity: VoucherEntity) -> Voucher:
        """Map a VoucherEntity to a Voucher domain model.

        Args:
            voucher_entity: The VoucherEntity to map

        Returns:
            The corresponding Voucher domain model
        """
        return Voucher(
            id=voucher_entity.id,
            code=voucher_entity.code,
            discount_rate=voucher_entity.discount_rate,
            valid_from=voucher_entity.valid_from,
            valid_until=voucher_entity.valid_until,
            max_usage=voucher_entity.max_usage,
            used_count=voucher_entity.used_count,
        )

    @staticmethod
    def to_domains(voucher_entities: list[VoucherEntity]) -> list[Voucher]:
        """Map a list of VoucherEntity to a list of Voucher domain models.

        Args:
            voucher_entities: The list of VoucherEntity to map

        Returns:
            The corresponding list of Voucher domain models
        """
        return [VoucherEntityMappers.to_domain(entity) for entity in voucher_entities]
