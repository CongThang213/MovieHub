from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.payment_method import PaymentMethod
from src.domain.repositories.payment_method_repository import PaymentMethodRepository


class GetActivePaymentMethodsUseCase:
    """Use case for retrieving all active payment methods."""

    def __init__(
        self,
        payment_method_repository: PaymentMethodRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._payment_method_repository = payment_method_repository
        self._sessionmaker = sessionmaker

    async def execute(self) -> list[PaymentMethod]:
        """Execute the use case to get all active payment methods."""
        async with self._sessionmaker() as session:
            return await self._payment_method_repository.get_active_payment_methods(
                session
            )
