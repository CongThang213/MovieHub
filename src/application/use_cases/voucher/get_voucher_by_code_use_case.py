from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.voucher import Voucher
from src.domain.repositories.voucher_repository import VoucherRepository


class GetVoucherByCodeUseCase:
    """Use case for retrieving a voucher by code."""

    def __init__(
        self,
        voucher_repository: VoucherRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._voucher_repository = voucher_repository
        self._sessionmaker = sessionmaker

    async def execute(self, code: str) -> Optional[Voucher]:
        """Execute the use case to get a voucher by code.

        Args:
            code: The code of the voucher to retrieve

        Returns:
            The voucher domain model or None if not found
        """
        async with self._sessionmaker() as session:
            return await self._voucher_repository.get_by_code(code, session)
