from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config.logging_config import logger
from src.domain.exceptions.booking_exceptions import (
    BookingNotFoundException,
    BookingDeletionFailedException,
)
from src.domain.repositories.booking_repository import BookingRepository


class DeleteBookingUseCase:
    """
    Use case for deleting a booking.
    """

    def __init__(
        self,
        booking_repository: BookingRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._booking_repository = booking_repository
        self._sessionmaker = sessionmaker

    async def execute(self, booking_id: str) -> None:
        logger.info(f"Attempting to delete booking {booking_id}")

        async with self._sessionmaker() as session:
            try:
                existing_booking = await self._booking_repository.get_by_id(
                    booking_id, session
                )
                if not existing_booking:
                    raise BookingNotFoundException(identifier=booking_id)

                await self._booking_repository.delete(booking_id, session)
                await session.commit()

                logger.info(f"Booking {booking_id} deleted successfully.")

            except BookingNotFoundException:
                raise
            except Exception as e:
                await session.rollback()
                logger.error(f"Error deleting booking {booking_id}: {str(e)}")
                raise BookingDeletionFailedException(
                    id=booking_id, message="Failed to delete booking"
                )
