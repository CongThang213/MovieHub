from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.repositories.payment_method_repository import PaymentMethodRepository


class DeletePaymentMethodUseCase:
    """Use case for deleting a payment method."""

    def __init__(
        self,
        payment_method_repository: PaymentMethodRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._payment_method_repository = payment_method_repository
        self._sessionmaker = sessionmaker

    async def execute(self, payment_method_id: str) -> None:
        """Execute the use case to delete a payment method."""
        async with self._sessionmaker() as session:
            await self._payment_method_repository.delete(payment_method_id, session)
            await session.commit()
