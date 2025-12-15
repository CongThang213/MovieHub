from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.payment_method import PaymentMethod
from src.domain.repositories.payment_method_repository import PaymentMethodRepository


class GetPaymentMethodsUseCase:
    """Use case for retrieving all payment methods with pagination."""

    def __init__(
        self,
        payment_method_repository: PaymentMethodRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._payment_method_repository = payment_method_repository
        self._sessionmaker = sessionmaker

    async def execute(
        self, page: int = PAGE_DEFAULT, page_size: int = PAGE_SIZE_DEFAULT
    ) -> list[PaymentMethod]:
        """Execute the use case to get all payment methods."""
        async with self._sessionmaker() as session:
            return await self._payment_method_repository.get_all(
                session, page, page_size
            )
