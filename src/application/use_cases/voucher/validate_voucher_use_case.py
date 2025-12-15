from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.voucher_exceptions import (
    VoucherCodeNotFoundException,
    VoucherInvalidException,
)
from src.domain.repositories.voucher_repository import VoucherRepository


class ValidateVoucherUseCase:
    """Use case for validating a voucher by code."""

    def __init__(
        self,
        voucher_repository: VoucherRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._voucher_repository = voucher_repository
        self._sessionmaker = sessionmaker

    async def execute(self, code: str) -> dict:
        """Execute the use case to validate a voucher by code.

        Args:
            code: The voucher code to validate

        Returns:
            A dictionary with validation result and voucher details

        Raises:
            VoucherCodeNotFoundException: If the voucher code does not exist
            VoucherInvalidException: If the voucher is invalid
        """
        async with self._sessionmaker() as session:
            voucher = await self._voucher_repository.get_by_code(code, session)

            if not voucher:
                raise VoucherCodeNotFoundException(code=code)

            # Check if voucher is valid
            if not voucher.is_valid():
                now = datetime.now()

                if now < voucher.valid_from:
                    reason = (
                        f"Voucher is not yet valid. Valid from {voucher.valid_from}"
                    )
                elif voucher.valid_until and now > voucher.valid_until:
                    reason = f"Voucher has expired. Valid until {voucher.valid_until}"
                elif voucher.used_count >= voucher.max_usage:
                    reason = "Voucher has reached maximum usage limit"
                else:
                    reason = "Voucher is invalid"

                raise VoucherInvalidException(code=code, reason=reason)

            return {
                "valid": True,
                "voucher_id": voucher.id,
                "code": voucher.code,
                "discount_rate": voucher.discount_rate,
                "remaining_uses": voucher.get_remaining_uses(),
            }
