from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.payment_method import PaymentMethod
from src.domain.repositories.payment_method_repository import PaymentMethodRepository


class CreatePaymentMethodUseCase:
    """Use case for creating a payment method."""

    def __init__(
        self,
        payment_method_repository: PaymentMethodRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._payment_method_repository = payment_method_repository
        self._sessionmaker = sessionmaker

    async def execute(self, payment_method: PaymentMethod) -> PaymentMethod:
        """Execute the use case to create a payment method."""
        async with self._sessionmaker() as session:
            result = await self._payment_method_repository.create(
                payment_method, session
            )
            await session.commit()
            return result
