from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.payment_method_exceptions import (
    PaymentMethodNotFoundException,
)
from src.domain.models.payment_method import PaymentMethod
from src.domain.repositories.payment_method_repository import PaymentMethodRepository


class GetPaymentMethodUseCase:
    """Use case for retrieving a payment method by ID."""

    def __init__(
        self,
        payment_method_repository: PaymentMethodRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._payment_method_repository = payment_method_repository
        self._sessionmaker = sessionmaker

    async def execute(self, payment_method_id: str) -> PaymentMethod:
        """Execute the use case to get a payment method by ID."""
        async with self._sessionmaker() as session:
            result = await self._payment_method_repository.get_by_id(
                payment_method_id, session
            )
            if not result:
                raise PaymentMethodNotFoundException(payment_method_id)
            return result
