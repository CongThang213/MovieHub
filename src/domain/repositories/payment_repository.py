from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.payment import Payment


class PaymentRepository(ABC):
    """Interface for payment repository"""

    @abstractmethod
    async def get_by_id(
        self, payment_id: str, session: AsyncSession
    ) -> Optional[Payment]:
        """Get a payment by ID

        Args:
            payment_id: The payment ID to look up
            session: The database session to use

        Returns:
            The payment domain model or None if not found
        """
        pass

    @abstractmethod
    async def get_by_booking_id(
        self, booking_id: str, session: AsyncSession
    ) -> Optional[Payment]:
        """Get a payment by booking ID

        Args:
            booking_id: The booking ID to look up
            session: The database session to use

        Returns:
            The payment domain model or None if not found
        """
        pass

    @abstractmethod
    async def create(self, payment: Payment, session: AsyncSession) -> Payment:
        """Create a new payment

        Args:
            payment: The payment to create
            session: The database session to use

        Returns:
            The created payment
        """
        pass

    @abstractmethod
    async def update(self, payment_id: str, session: AsyncSession, **kwargs) -> Payment:
        """Update an existing payment

        Args:
            payment_id: The ID of the payment to update
            session: The database session to use
            **kwargs: Fields to update on the payment

        Returns:
            The updated payment
        """
        pass

    @abstractmethod
    async def get_pending_by_booking_and_method(
        self, booking_id: str, payment_method_id: str, session: AsyncSession
    ) -> Optional[Payment]:
        """Get a pending payment by booking ID and payment method ID

        Args:
            booking_id: The booking ID to look up
            payment_method_id: The payment method ID to look up
            session: The database session to use

        Returns:
            The pending payment domain model or None if not found
        """
        pass
