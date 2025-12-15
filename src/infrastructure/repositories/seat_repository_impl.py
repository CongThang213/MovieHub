from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.exceptions.app_exception import DuplicateEntryException
from src.domain.exceptions.seat_exceptions import SeatNotFoundException
from src.domain.models.seat import Seat
from src.domain.repositories.seat_repository import SeatRepository
from src.infrastructure.database.models.mappers.seat_entity_mappers import (
    SeatEntityMappers,
)
from src.infrastructure.database.models.seat_entity import SeatEntity


class SeatRepositoryImpl(SeatRepository):
    """Implementation of the seat repository using SQLAlchemy."""

    async def create(self, seat: Seat, session: AsyncSession) -> Seat:
        """Create a new seat record.

        Args:
            seat: The seat domain model to create
            session: The database session to use

        Returns:
            The created seat domain model with ID populated
        """
        seat_entity = SeatEntityMappers.from_domain(seat)
        session.add(seat_entity)
        await session.flush()

        return SeatEntityMappers.to_domain(seat_entity)

    async def get_by_id(self, seat_id: str, session: AsyncSession) -> Optional[Seat]:
        """Get a seat by its ID.

        Args:
            seat_id: The ID of the seat to retrieve
            session: The database session to use

        Returns:
            The seat domain model or None if not found
        """
        result = await session.execute(
            select(SeatEntity)
            .options(joinedload(SeatEntity.category))
            .where(SeatEntity.id == seat_id)
        )
        try:
            seat_entity = result.unique().scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(entry_type="Seat", identifier=seat_id) from e

        return SeatEntityMappers.to_domain(seat_entity) if seat_entity else None

    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Seat]:
        """Get all seats with pagination.

        Args:
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.

        Returns:
            A list of seat domain models for the specified page
        """
        offset = (page - 1) * page_size
        result = await session.execute(
            select(SeatEntity).offset(offset).limit(page_size)
        )
        seat_entities = result.scalars().all()

        return SeatEntityMappers.to_domains(seat_entities)

    async def get_by_row_id(
        self,
        row_id: str,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Seat]:
        """Get all seats in a specific row with pagination.

        Args:
            row_id: The ID of the row
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.

        Returns:
            A list of seat domain models for the specified row and page
        """
        offset = (page - 1) * page_size
        result = await session.execute(
            select(SeatEntity)
            .options(joinedload(SeatEntity.category))
            .where(SeatEntity.row_id == row_id)
            .offset(offset)
            .limit(page_size)
        )
        seat_entities = result.unique().scalars().all()

        return SeatEntityMappers.to_domains(seat_entities)

    async def get_by_category_id(
        self,
        category_id: str,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Seat]:
        """Get all seats in a specific category with pagination.

        Args:
            category_id: The ID of the category
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.

        Returns:
            A list of seat domain models for the specified category and page
        """
        offset = (page - 1) * page_size
        result = await session.execute(
            select(SeatEntity)
            .where(SeatEntity.category_id == category_id)
            .offset(offset)
            .limit(page_size)
        )
        seat_entities = result.scalars().all()

        return SeatEntityMappers.to_domains(seat_entities)

    async def update(self, seat: Seat, session: AsyncSession) -> Seat:
        """Update an existing seat record.

        Args:
            seat: The seat domain model to update
            session: The database session to use

        Returns:
            The updated seat domain model

        Raises:
            SeatNotFoundException: If the seat does not exist
        """
        result = await session.execute(
            select(SeatEntity).where(SeatEntity.id == seat.id)
        )
        seat_entity = result.scalar_one_or_none()

        if not seat_entity:
            raise SeatNotFoundException(seat.id)

        # Update entity attributes with the complete domain model
        seat_entity.row_id = seat.row_id
        seat_entity.category_id = seat.category_id
        seat_entity.seat_number = seat.seat_number
        seat_entity.pos_x = seat.pos_x
        seat_entity.pos_y = seat.pos_y
        seat_entity.is_accessible = seat.is_accessible
        seat_entity.external_label = seat.external_label

        await session.flush()

        return SeatEntityMappers.to_domain(seat_entity)

    async def delete(self, seat_id: str, session: AsyncSession) -> None:
        """Delete a seat record.

        Args:
            seat_id: The ID of the seat to delete
            session: The database session to use

        Raises:
            SeatNotFoundException: If the seat does not exist
        """
        result = await session.execute(
            select(SeatEntity).where(SeatEntity.id == seat_id)
        )
        seat_entity = result.scalar_one_or_none()

        if not seat_entity:
            raise SeatNotFoundException(seat_id)

        await session.execute(delete(SeatEntity).where(SeatEntity.id == seat_id))
        await session.flush()
