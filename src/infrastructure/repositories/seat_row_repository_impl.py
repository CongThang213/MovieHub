from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.seat_row import SeatRow
from src.domain.repositories.seat_row_repository import SeatRowRepository
from src.infrastructure.database.models.mappers.seat_row_entity_mappers import (
    SeatRowEntityMappers,
)
from src.infrastructure.database.models.seat_row_entity import SeatRowEntity


class SeatRowRepositoryImpl(SeatRowRepository):
    """Implementation of the seat row repository using SQLAlchemy."""

    async def create(self, seat_row: SeatRow, session: AsyncSession) -> SeatRow:
        """Create a new seat row record."""
        seat_row_entity = SeatRowEntityMappers.from_domain(seat_row)
        session.add(seat_row_entity)
        await session.flush()
        return SeatRowEntityMappers.to_domain(seat_row_entity)

    async def get_by_id(
        self, seat_row_id: str, session: AsyncSession
    ) -> Optional[SeatRow]:
        """Get a seat row by its ID."""
        result = await session.execute(
            select(SeatRowEntity).where(SeatRowEntity.id == seat_row_id)
        )
        seat_row_entity = result.scalar_one_or_none()
        return (
            SeatRowEntityMappers.to_domain(seat_row_entity) if seat_row_entity else None
        )

    async def get_by_hall_id(
        self, hall_id: str, session: AsyncSession
    ) -> list[SeatRow]:
        """Get all seat rows for a specific hall."""
        result = await session.execute(
            select(SeatRowEntity)
            .where(SeatRowEntity.hall_id == hall_id)
            .order_by(SeatRowEntity.row_order)
        )
        seat_row_entities = result.scalars().all()
        return SeatRowEntityMappers.to_domains(seat_row_entities)

    async def delete_by_hall_id(self, hall_id: str, session: AsyncSession) -> None:
        """Delete all seat rows for a specific hall."""
        await session.execute(
            delete(SeatRowEntity).where(SeatRowEntity.hall_id == hall_id)
        )
        await session.flush()

    async def delete(self, seat_row_id: str, session: AsyncSession) -> None:
        """Delete a seat row record."""
        await session.execute(
            delete(SeatRowEntity).where(SeatRowEntity.id == seat_row_id)
        )
        await session.flush()
