from typing import Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.voucher_exceptions import VoucherNotFoundException
from src.domain.models.voucher import Voucher
from src.domain.repositories.voucher_repository import VoucherRepository


class UpdateVoucherUseCase:
    """Use case for updating an existing voucher."""

    def __init__(
        self,
        voucher_repository: VoucherRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._voucher_repository = voucher_repository
        self._sessionmaker = sessionmaker

    async def execute(self, voucher_id: str, update_data: Dict[str, Any]) -> Voucher:
        """Execute the use case to update a voucher.

        Args:
            voucher_id: The ID of the voucher to update
            update_data: Dictionary containing the fields to update

        Returns:
            The updated voucher domain model

        Raises:
            VoucherNotFoundException: If the voucher is not found
        """
        async with self._sessionmaker() as session:
            # Fetch existing voucher
            existing_voucher = await self._voucher_repository.get_by_id(
                voucher_id, session
            )
            if not existing_voucher:
                raise VoucherNotFoundException(voucher_id=voucher_id)

            # Merge existing data with update data
            updated_voucher = Voucher(
                id=voucher_id,
                code=update_data.get("code", existing_voucher.code),
                discount_rate=update_data.get(
                    "discount_rate", existing_voucher.discount_rate
                ),
                valid_from=update_data.get("valid_from", existing_voucher.valid_from),
                valid_until=update_data.get(
                    "valid_until", existing_voucher.valid_until
                ),
                max_usage=update_data.get("max_usage", existing_voucher.max_usage),
                used_count=update_data.get("used_count", existing_voucher.used_count),
            )

            # Update in repository
            result = await self._voucher_repository.update(updated_voucher, session)
            await session.commit()
            return result
