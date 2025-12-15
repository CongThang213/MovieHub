from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.payment_method import PaymentMethod
from src.domain.repositories.payment_method_repository import PaymentMethodRepository


class UpdatePaymentMethodUseCase:
    """Use case for updating a payment method."""

    def __init__(
        self,
        payment_method_repository: PaymentMethodRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._payment_method_repository = payment_method_repository
        self._sessionmaker = sessionmaker

    async def execute(self, payment_method: PaymentMethod) -> PaymentMethod:
        """Execute the use case to update a payment method."""
        async with self._sessionmaker() as session:
            result = await self._payment_method_repository.update(
                payment_method, session
            )
            await session.commit()
            return result
