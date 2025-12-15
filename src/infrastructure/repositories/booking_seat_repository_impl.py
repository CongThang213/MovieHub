from typing import List, Optional, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.booking_seat_exceptions import (
    BookingSeatNotFoundException,
    BookingSeatDeletionFailedException,
)  # Need to create this exception file
from src.domain.models.booking_seat import BookingSeat
from src.domain.repositories.booking_seat_repository import BookingSeatRepository
from src.infrastructure.database.models.booking_seat_entity import BookingSeatEntity
from src.infrastructure.database.models.mappers.booking_seat_entity_mappers import (
    BookingSeatEntityMapper,
)


class BookingSeatRepositoryImpl(BookingSeatRepository):
    """Implementation of the booking seat repository using SQLAlchemy."""

    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        """Initialize the booking seat repository with a session factory.

        Args:
            sessionmaker: Factory for creating database sessions
        """
        self._sessionmaker = sessionmaker

    async def get_by_id(
        self, booking_seat_id: str, session: AsyncSession
    ) -> Optional[BookingSeat]:
        """Get a booking seat by ID.

        Args:
            booking_seat_id: The booking seat ID to look up
            session: The database session to use

        Returns:
            The booking seat domain model

        Raises:
            BookingSeatNotFoundException: If booking seat with given ID is not found
        """
        result = await session.execute(
            select(BookingSeatEntity).where(BookingSeatEntity.id == booking_seat_id)
        )
        booking_seat_entity = result.scalars().first()

        if not booking_seat_entity:
            raise BookingSeatNotFoundException(identifier=booking_seat_id)

        return BookingSeatEntityMapper.to_domain(booking_seat_entity)

    async def create(
        self, booking_seat: BookingSeat, session: AsyncSession
    ) -> BookingSeat:
        """Create a new booking seat.

        Args:
            booking_seat: The booking seat domain model to persist
            session: The database session to use

        Returns:
            The booking seat domain model with updated info
        """
        booking_seat_entity = BookingSeatEntityMapper.from_domain(booking_seat)

        session.add(booking_seat_entity)
        await session.flush()

        return BookingSeatEntityMapper.to_domain(booking_seat_entity)

    async def update(
        self, booking_seat_id: str, session: AsyncSession, **kwargs: Any
    ) -> BookingSeat:
        """Update an existing booking seat.

        Args:
            booking_seat_id: The ID of the booking seat to update
            session: The database session to use
            **kwargs: Fields to update on the booking seat

        Returns:
            The updated booking seat domain model

        Raises:
            BookingSeatNotFoundException: If booking seat with given ID is not found
        """
        result = await session.execute(
            select(BookingSeatEntity).where(BookingSeatEntity.id == booking_seat_id)
        )
        booking_seat_entity = result.scalars().first()

        if not booking_seat_entity:
            raise BookingSeatNotFoundException(identifier=booking_seat_id)

        for attr, value in kwargs.items():
            if value is not None and hasattr(booking_seat_entity, attr):
                setattr(booking_seat_entity, attr, value)

        await session.flush()

        return BookingSeatEntityMapper.to_domain(booking_seat_entity)

    async def delete(self, booking_seat_id: str, session: AsyncSession) -> None:
        """Delete a booking seat by ID.

        Args:
            booking_seat_id: The booking seat ID to delete
            session: The database session to use

        Raises:
            BookingSeatDeletionFailedException: If booking seat deletion fails
        """
        result = await session.execute(
            select(BookingSeatEntity).where(BookingSeatEntity.id == booking_seat_id)
        )
        booking_seat_entity = result.scalars().first()

        if not booking_seat_entity:
            raise BookingSeatDeletionFailedException(id=booking_seat_id)

        await session.delete(booking_seat_entity)

    async def get_booking_seats(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[BookingSeat]:
        """Get a list of booking seats with pagination.

        Args:
            session: The database session to use
            skip: Number of booking seats to skip (for pagination)
            limit: Maximum number of booking seats to return

        Returns:
            List of booking seat domain models
        """
        result = await session.execute(
            select(BookingSeatEntity).offset(skip).limit(limit)
        )
        booking_seat_entities = result.scalars().all()
        return [
            BookingSeatEntityMapper.to_domain(entity)
            for entity in booking_seat_entities
        ]

    async def get_booking_seats_by_booking_id(
        self, booking_id: str, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[BookingSeat]:
        """Get a list of booking seats by booking ID with pagination

        Args:
            booking_id: The ID of the booking
            session: The database session to use
            skip: Number of booking seats to skip
            limit: Maximum number of booking seats to return

        Returns:
            List of booking seats
        """
        result = await session.execute(
            select(BookingSeatEntity)
            .where(BookingSeatEntity.booking_id == booking_id)
            .offset(skip)
            .limit(limit)
        )
        booking_seat_entities = result.scalars().all()
        return [
            BookingSeatEntityMapper.to_domain(entity)
            for entity in booking_seat_entities
        ]

    async def get_booking_seats_by_showtime_id(
        self, showtime_id: str, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[BookingSeat]:
        """Get a list of booking seats by showtime ID with pagination

        Args:
            showtime_id: The ID of the showtime
            session: The database session to use
            skip: Number of booking seats to skip
            limit: Maximum number of booking seats to return

        Returns:
            List of booking seats
        """
        result = await session.execute(
            select(BookingSeatEntity)
            .where(BookingSeatEntity.showtime_id == showtime_id)
            .offset(skip)
            .limit(limit)
        )
        booking_seat_entities = result.scalars().all()
        return [
            BookingSeatEntityMapper.to_domain(entity)
            for entity in booking_seat_entities
        ]
