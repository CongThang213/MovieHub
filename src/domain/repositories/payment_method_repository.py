from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.payment_method import PaymentMethod


class PaymentMethodRepository(ABC):
    """Interface for payment method repository operations."""

    @abstractmethod
    async def create(
        self, payment_method: PaymentMethod, session: AsyncSession
    ) -> PaymentMethod:
        """Create a new payment method record."""
        pass

    @abstractmethod
    async def get_by_id(
        self, payment_method_id: str, session: AsyncSession
    ) -> Optional[PaymentMethod]:
        """Get payment method by ID."""
        pass

    @abstractmethod
    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[PaymentMethod]:
        """Get all payment methods with pagination."""
        pass

    @abstractmethod
    async def get_active_payment_methods(
        self, session: AsyncSession
    ) -> list[PaymentMethod]:
        """Get all active payment methods."""
        pass

    @abstractmethod
    async def update(
        self, payment_method: PaymentMethod, session: AsyncSession
    ) -> PaymentMethod:
        """Update an existing payment method record."""
        pass

    @abstractmethod
    async def delete(self, payment_method_id: str, session: AsyncSession) -> None:
        """Delete a payment method record."""
        pass
