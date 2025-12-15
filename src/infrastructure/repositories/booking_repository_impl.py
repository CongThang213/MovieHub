from typing import List, Optional, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.booking_exceptions import (
    BookingNotFoundException,
    BookingDeletionFailedException,
)  # Need to create this exception file
from src.domain.models.booking import Booking
from src.domain.repositories.booking_repository import BookingRepository
from src.infrastructure.database.models.booking_entity import BookingEntity
from src.infrastructure.database.models.mappers.booking_entity_mappers import (
    BookingEntityMapper,
)


class BookingRepositoryImpl(BookingRepository):
    """Implementation of the booking repository using SQLAlchemy."""

    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        """Initialize the booking repository with a session factory.

        Args:
            sessionmaker: Factory for creating database sessions
        """
        self._sessionmaker = sessionmaker

    async def get_by_id(
        self, booking_id: str, session: AsyncSession
    ) -> Optional[Booking]:
        """Get a booking by ID.

        Args:
            booking_id: The booking ID to look up
            session: The database session to use

        Returns:
            The booking domain model

        Raises:
            BookingNotFoundException: If booking with given ID is not found
        """
        result = await session.execute(
            select(BookingEntity).where(BookingEntity.id == booking_id)
        )
        booking_entity = result.scalars().first()

        if not booking_entity:
            raise BookingNotFoundException(identifier=booking_id)

        return BookingEntityMapper.to_domain(booking_entity)

    async def create(self, booking: Booking, session: AsyncSession) -> Booking:
        """Create a new booking.

        Args:
            booking: The booking domain model to persist
            session: The database session to use

        Returns:
            The booking domain model with updated info
        """
        booking_entity = BookingEntityMapper.from_domain(booking)

        session.add(booking_entity)
        await session.flush()

        return BookingEntityMapper.to_domain(booking_entity)

    async def update(
        self, booking_id: str, session: AsyncSession, **kwargs: Any
    ) -> Booking:
        """Update an existing booking.

        Args:
            booking_id: The ID of the booking to update
            session: The database session to use
            **kwargs: Fields to update on the booking

        Returns:
            The updated booking domain model

        Raises:
            BookingNotFoundException: If booking with given ID is not found
        """
        result = await session.execute(
            select(BookingEntity).where(BookingEntity.id == booking_id)
        )
        booking_entity = result.scalars().first()

        if not booking_entity:
            raise BookingNotFoundException(identifier=booking_id)

        for attr, value in kwargs.items():
            if value is not None and hasattr(booking_entity, attr):
                setattr(booking_entity, attr, value)

        await session.flush()

        return BookingEntityMapper.to_domain(booking_entity)

    async def delete(self, booking_id: str, session: AsyncSession) -> None:
        """Delete a booking by ID.

        Args:
            booking_id: The booking ID to delete
            session: The database session to use

        Raises:
            BookingDeletionFailedException: If booking deletion fails
        """
        result = await session.execute(
            select(BookingEntity).where(BookingEntity.id == booking_id)
        )
        booking_entity = result.scalars().first()

        if not booking_entity:
            raise BookingDeletionFailedException(id=booking_id)

        await session.delete(booking_entity)

    async def get_bookings(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Booking]:
        """Get a list of bookings with pagination.

        Args:
            session: The database session to use
            skip: Number of bookings to skip (for pagination)
            limit: Maximum number of bookings to return

        Returns:
            List of booking domain models
        """
        result = await session.execute(select(BookingEntity).offset(skip).limit(limit))
        booking_entities = result.scalars().all()
        return [BookingEntityMapper.to_domain(entity) for entity in booking_entities]

    async def get_bookings_by_user_id(
        self, user_id: str, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Booking]:
        """Get a list of bookings by user ID with pagination

        Args:
            user_id: The ID of the user
            session: The database session to use
            skip: Number of bookings to skip
            limit: Maximum number of bookings to return

        Returns:
            List of bookings
        """
        result = await session.execute(
            select(BookingEntity)
            .where(BookingEntity.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        booking_entities = result.scalars().all()
        return [BookingEntityMapper.to_domain(entity) for entity in booking_entities]
