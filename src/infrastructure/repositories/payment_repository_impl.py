from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.enums.payment_status import PaymentStatus
from src.domain.models.payment import Payment
from src.domain.repositories.payment_repository import PaymentRepository
from src.infrastructure.database.models.mappers.payment_entity_mappers import (
    PaymentEntityMapper,
)
from src.infrastructure.database.models.payment_entity import PaymentEntity


class PaymentRepositoryImpl(PaymentRepository):
    """Implementation of the payment repository using SQLAlchemy."""

    async def get_by_id(
        self, payment_id: str, session: AsyncSession
    ) -> Optional[Payment]:
        """Get a payment by ID.

        Args:
            payment_id: The payment ID to look up
            session: The database session to use

        Returns:
            The payment domain model or None if not found
        """
        result = await session.execute(
            select(PaymentEntity).where(PaymentEntity.id == payment_id)
        )
        payment_entity = result.scalars().first()

        if not payment_entity:
            return None

        return PaymentEntityMapper.to_domain(payment_entity)

    async def get_by_booking_id(
        self, booking_id: str, session: AsyncSession
    ) -> Optional[Payment]:
        """Get a payment by booking ID.

        Args:
            booking_id: The booking ID to look up
            session: The database session to use

        Returns:
            The payment domain model or None if not found
        """
        result = await session.execute(
            select(PaymentEntity).where(PaymentEntity.booking_id == booking_id)
        )
        payment_entity = result.scalars().first()

        if not payment_entity:
            return None

        return PaymentEntityMapper.to_domain(payment_entity)

    async def create(self, payment: Payment, session: AsyncSession) -> Payment:
        """Create a new payment.

        Args:
            payment: The payment domain model to persist
            session: The database session to use

        Returns:
            The payment domain model with updated info
        """
        payment_entity = PaymentEntityMapper.from_domain(payment)

        session.add(payment_entity)
        await session.flush()

        return PaymentEntityMapper.to_domain(payment_entity)

    async def update(self, payment_id: str, session: AsyncSession, **kwargs) -> Payment:
        """Update an existing payment.

        Args:
            payment_id: The ID of the payment to update
            session: The database session to use
            **kwargs: Fields to update on the payment

        Returns:
            The updated payment domain model
        """
        result = await session.execute(
            select(PaymentEntity).where(PaymentEntity.id == payment_id)
        )
        payment_entity = result.scalars().first()

        if not payment_entity:
            return None

        for attr, value in kwargs.items():
            if value is not None and hasattr(payment_entity, attr):
                if attr == "metadata":
                    setattr(payment_entity, "payment_metadata", value)
                else:
                    setattr(payment_entity, attr, value)

        await session.flush()

        return PaymentEntityMapper.to_domain(payment_entity)

    async def get_pending_by_booking_and_method(
        self, booking_id: str, payment_method_id: str, session: AsyncSession
    ) -> Optional[Payment]:
        """Get a pending payment by booking ID and payment method ID.

        Args:
            booking_id: The booking ID to look up
            payment_method_id: The payment method ID to look up
            session: The database session to use

        Returns:
            The pending payment domain model or None if not found
        """
        result = await session.execute(
            select(PaymentEntity).where(
                and_(
                    PaymentEntity.booking_id == booking_id,
                    PaymentEntity.payment_method_id == payment_method_id,
                    PaymentEntity.status == PaymentStatus.PENDING.value,
                )
            )
        )
        payment_entity = result.scalars().first()

        if not payment_entity:
            return None

        return PaymentEntityMapper.to_domain(payment_entity)
