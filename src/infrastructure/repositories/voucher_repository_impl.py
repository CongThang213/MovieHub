from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.exc import MultipleResultsFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.exceptions.app_exception import DuplicateEntryException
from src.domain.exceptions.voucher_exceptions import VoucherNotFoundException
from src.domain.models.voucher import Voucher
from src.domain.repositories.voucher_repository import VoucherRepository
from src.infrastructure.database.models.voucher_entity import VoucherEntity
from src.infrastructure.database.models.mappers.voucher_entity_mappers import (
    VoucherEntityMappers,
)


class VoucherRepositoryImpl(VoucherRepository):
    """Implementation of the voucher repository using SQLAlchemy."""

    async def get_by_code(self, code: str, session: AsyncSession) -> Optional[Voucher]:
        """Get a voucher by its code.

        Args:
            code: The code of the voucher to retrieve
            session: The database session to use

        Returns:
            The voucher domain model or None if not found

        Raises:
            DuplicateEntryException: If multiple vouchers with the same code are found
        """
        result = await session.execute(
            select(VoucherEntity).where(VoucherEntity.code == code)
        )
        try:
            voucher_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(entry_type="Voucher", identifier=code) from e

        return (
            VoucherEntityMappers.to_domain(voucher_entity) if voucher_entity else None
        )

    async def create(self, voucher: Voucher, session: AsyncSession) -> Voucher:
        """Create a new voucher record.

        Args:
            voucher: The voucher domain model to create
            session: The database session to use

        Returns:
            The created voucher domain model with ID populated

        Raises:
            DuplicateEntryException: If a voucher with the same code already exists
        """
        try:
            # Check if a voucher with the same code already exists
            existing_voucher = await self.get_by_code(voucher.code, session)
            if existing_voucher:
                raise DuplicateEntryException(
                    entry_type="Voucher", identifier=voucher.code
                )

            voucher_entity = VoucherEntityMappers.from_domain(voucher)
            session.add(voucher_entity)  # Add the new voucher entity to the session
            await session.flush()  # Flush to populate the ID

            return VoucherEntityMappers.to_domain(voucher_entity)

        except IntegrityError as e:
            if "idx_vouchers_code" in str(e) or "unique constraint" in str(e).lower():
                raise DuplicateEntryException(
                    entry_type="Voucher", identifier=voucher.code
                ) from e
            raise

    async def get_by_id(
        self, voucher_id: str, session: AsyncSession
    ) -> Optional[Voucher]:
        """Get a voucher by its ID.

        Args:
            voucher_id: The ID of the voucher to retrieve
            session: The database session to use

        Returns:
            The voucher domain model or None if not found
        """
        result = await session.execute(
            select(VoucherEntity).where(VoucherEntity.id == voucher_id)
        )
        try:
            voucher_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="Voucher", identifier=voucher_id
            ) from e

        return (
            VoucherEntityMappers.to_domain(voucher_entity) if voucher_entity else None
        )

    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Voucher]:
        """Get all vouchers with pagination.

        Args:
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.

        Returns:
            A list of voucher domain models for the specified page
        """
        offset = (page - 1) * page_size
        result = await session.execute(
            select(VoucherEntity).offset(offset).limit(page_size)
        )
        voucher_entities = result.scalars().all()

        return VoucherEntityMappers.to_domains(voucher_entities)

    async def update(self, voucher: Voucher, session: AsyncSession) -> Voucher:
        """Update an existing voucher record.

        Args:
            voucher: The voucher domain model with updated fields
            session: The database session to use

        Returns:
            The updated voucher domain model

        Raises:
            VoucherNotFoundException: If the voucher to update is not found
        """
        existing_voucher_entity = await session.get(VoucherEntity, voucher.id)
        if not existing_voucher_entity:
            raise VoucherNotFoundException(voucher_id=voucher.id)

        # Update fields
        existing_voucher_entity.code = voucher.code
        existing_voucher_entity.discount_rate = voucher.discount_rate
        existing_voucher_entity.valid_from = voucher.valid_from
        existing_voucher_entity.valid_until = voucher.valid_until
        existing_voucher_entity.max_usage = voucher.max_usage
        existing_voucher_entity.used_count = voucher.used_count

        await session.flush()

        return VoucherEntityMappers.to_domain(existing_voucher_entity)

    async def delete(self, voucher_id: str, session: AsyncSession) -> bool:
        """Delete a voucher record.

        Args:
            voucher_id: The ID of the voucher to delete
            session: The database session to use

        Returns:
            True if the voucher was deleted, False otherwise
        """
        result = await session.execute(
            delete(VoucherEntity).where(VoucherEntity.id == voucher_id)
        )
        return result.rowcount > 0
