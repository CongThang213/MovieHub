from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.voucher import Voucher
from src.domain.repositories.voucher_repository import VoucherRepository


class GetVouchersUseCase:
    """Use case for retrieving all vouchers with pagination."""

    def __init__(
        self,
        voucher_repository: VoucherRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._voucher_repository = voucher_repository
        self._sessionmaker = sessionmaker

    async def execute(
        self,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Voucher]:
        """Execute the use case to get all vouchers.

        Args:
            page: The page number for pagination
            page_size: The number of items per page

        Returns:
            A list of voucher domain models
        """
        async with self._sessionmaker() as session:
            return await self._voucher_repository.get_all(session, page, page_size)
