from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.repositories.voucher_repository import VoucherRepository


class DeleteVoucherUseCase:
    """Use case for deleting a voucher."""

    def __init__(
        self,
        voucher_repository: VoucherRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._voucher_repository = voucher_repository
        self._sessionmaker = sessionmaker

    async def execute(self, voucher_id: str) -> bool:
        """Execute the use case to delete a voucher.

        Args:
            voucher_id: The ID of the voucher to delete

        Returns:
            True if the voucher was deleted, False otherwise
        """
        async with self._sessionmaker() as session:
            result = await self._voucher_repository.delete(voucher_id, session)
            await session.commit()
            return result
