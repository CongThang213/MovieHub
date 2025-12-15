from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.voucher import Voucher
from src.domain.repositories.voucher_repository import VoucherRepository


class CreateVoucherUseCase:
    """Use case for creating a new voucher."""

    def __init__(
        self,
        voucher_repository: VoucherRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._voucher_repository = voucher_repository
        self._sessionmaker = sessionmaker

    async def execute(self, voucher: Voucher) -> Voucher:
        """Execute the use case to create a new voucher.

        Args:
            voucher: The voucher domain model to create

        Returns:
            The created voucher domain model with ID populated
        """
        async with self._sessionmaker() as session:
            result = await self._voucher_repository.create(voucher, session)
            await session.commit()
            return result
