from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.exceptions.app_exception import DuplicateEntryException
from src.domain.exceptions.payment_method_exceptions import (
    PaymentMethodNotFoundException,
)
from src.domain.models.payment_method import PaymentMethod
from src.domain.repositories.payment_method_repository import PaymentMethodRepository
from src.infrastructure.database.models.mappers.payment_method_entity_mappers import (
    PaymentMethodEntityMappers,
)
from src.infrastructure.database.models.payment_method_entity import (
    PaymentMethodEntity,
)


class PaymentMethodRepositoryImpl(PaymentMethodRepository):
    """Implementation of the payment method repository using SQLAlchemy."""

    async def create(
        self, payment_method: PaymentMethod, session: AsyncSession
    ) -> PaymentMethod:
        """Create a new payment method record."""
        payment_method_entity = PaymentMethodEntityMappers.from_domain(payment_method)
        session.add(payment_method_entity)
        await session.flush()
        await session.refresh(payment_method_entity)

        return PaymentMethodEntityMappers.to_domain(payment_method_entity)

    async def get_by_id(
        self, payment_method_id: str, session: AsyncSession
    ) -> Optional[PaymentMethod]:
        """Get a payment method by its ID."""
        result = await session.execute(
            select(PaymentMethodEntity).where(
                PaymentMethodEntity.id == payment_method_id
            )
        )
        try:
            payment_method_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="PaymentMethod", identifier=payment_method_id
            ) from e

        return (
            PaymentMethodEntityMappers.to_domain(payment_method_entity)
            if payment_method_entity
            else None
        )

    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[PaymentMethod]:
        """Get all payment methods with pagination."""
        offset = (page - 1) * page_size
        result = await session.execute(
            select(PaymentMethodEntity).offset(offset).limit(page_size)
        )
        payment_method_entities = result.scalars().all()
        return PaymentMethodEntityMappers.to_domains(payment_method_entities)

    async def get_active_payment_methods(
        self, session: AsyncSession
    ) -> list[PaymentMethod]:
        """Get all active payment methods."""
        result = await session.execute(
            select(PaymentMethodEntity).where(PaymentMethodEntity.active == True)
        )
        payment_method_entities = result.scalars().all()
        return PaymentMethodEntityMappers.to_domains(payment_method_entities)

    async def update(
        self, payment_method: PaymentMethod, session: AsyncSession
    ) -> PaymentMethod:
        """Update an existing payment method record."""
        result = await session.execute(
            select(PaymentMethodEntity).where(
                PaymentMethodEntity.id == payment_method.id
            )
        )
        payment_method_entity = result.scalar_one_or_none()

        if not payment_method_entity:
            raise PaymentMethodNotFoundException(payment_method.id)

        # Update entity attributes
        payment_method_entity.name = payment_method.name
        payment_method_entity.active = payment_method.active
        payment_method_entity.surcharge = payment_method.surcharge

        await session.flush()
        await session.refresh(payment_method_entity)

        return PaymentMethodEntityMappers.to_domain(payment_method_entity)

    async def delete(self, payment_method_id: str, session: AsyncSession) -> None:
        """Delete a payment method record."""
        result = await session.execute(
            select(PaymentMethodEntity).where(
                PaymentMethodEntity.id == payment_method_id
            )
        )
        payment_method_entity = result.scalar_one_or_none()

        if not payment_method_entity:
            raise PaymentMethodNotFoundException(payment_method_id)

        await session.delete(payment_method_entity)
