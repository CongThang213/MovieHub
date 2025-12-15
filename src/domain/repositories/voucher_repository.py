from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.voucher import Voucher


class VoucherRepository(ABC):
    """Interface for voucher repository operations."""

    @abstractmethod
    async def create(self, voucher: Voucher, session: AsyncSession) -> Voucher:
        """Create a new voucher record.

        Args:
            voucher: The voucher domain model to create
            session: The database session to use

        Returns:
            The created voucher domain model with ID populated
        """
        pass

    @abstractmethod
    async def get_by_id(
        self, voucher_id: str, session: AsyncSession
    ) -> Optional[Voucher]:
        """Get voucher by ID.

        Args:
            voucher_id: The ID of the voucher to retrieve
            session: The database session to use

        Returns:
            The voucher domain model or None if not found
        """
        pass

    @abstractmethod
    async def get_by_code(self, code: str, session: AsyncSession) -> Optional[Voucher]:
        """Get voucher by code.

        Args:
            code: The code of the voucher to retrieve
            session: The database session to use

        Returns:
            The voucher domain model or None if not found
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    async def update(self, voucher: Voucher, session: AsyncSession) -> Voucher:
        """Update an existing voucher record.

        Args:
            voucher: The voucher domain model with updated fields
            session: The database session to use

        Returns:
            The updated voucher domain model
        """
        pass

    @abstractmethod
    async def delete(self, voucher_id: str, session: AsyncSession) -> bool:
        """Delete a voucher record.

        Args:
            voucher_id: The ID of the voucher to delete
            session: The database session to use

        Returns:
            True if the voucher was deleted, False otherwise
        """
        pass
