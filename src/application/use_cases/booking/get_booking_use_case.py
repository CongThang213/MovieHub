from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config.logging_config import logger
from src.application.dtos.booking_dtos import (
    BookingResponseDTO,
    BookingSeatResponseDTO,
)
from src.domain.exceptions.booking_exceptions import BookingNotFoundException
from src.domain.repositories.booking_repository import BookingRepository
from src.domain.repositories.booking_seat_repository import BookingSeatRepository


class GetBookingUseCase:
    """
    Use case for retrieving booking information.
    """

    def __init__(
        self,
        booking_repository: BookingRepository,
        booking_seat_repository: BookingSeatRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._booking_repository = booking_repository
        self._booking_seat_repository = booking_seat_repository
        self._sessionmaker = sessionmaker

    async def execute(self, booking_id: str) -> BookingResponseDTO:
        logger.info(f"Retrieving booking information for booking ID: {booking_id}")

        async with self._sessionmaker() as session:
            try:
                booking = await self._booking_repository.get_by_id(booking_id, session)

                if not booking:
                    logger.warning(f"Booking not found with ID: {booking_id}")
                    raise BookingNotFoundException(identifier=booking_id)

                booking_seats = (
                    await self._booking_seat_repository.get_booking_seats_by_booking_id(
                        booking_id, session
                    )
                )

                # Convert booking_seats to DTOs
                booking_seats_response = [
                    BookingSeatResponseDTO.model_validate(seat) for seat in booking_seats
                ]

                logger.info(f"Successfully retrieved booking: {booking.id}")
                return BookingResponseDTO(
                    id=booking.id,
                    user_id=booking.user_id,
                    status=booking.status,
                    created_at=booking.created_at,
                    paid_at=booking.paid_at,
                    total_price=booking.total_price,
                    payment_method_id=booking.payment_method_id,
                    voucher_id=booking.voucher_id,
                    payment_reference=booking.payment_reference,
                    booking_seats=booking_seats_response,
                )

            except BookingNotFoundException:
                raise
            except Exception as e:
                logger.error(f"Error retrieving booking {booking_id}: {str(e)}")
                raise
