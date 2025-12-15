from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config.logging_config import logger
from src.application.dtos.booking_dtos import BookingResponseDTO, BookingUpdateDTO
from src.domain.exceptions.booking_exceptions import (
    BookingNotFoundException,
    BookingUpdateFailedException,
)
from src.domain.repositories.booking_repository import BookingRepository
from src.domain.repositories.booking_seat_repository import BookingSeatRepository


class UpdateBookingUseCase:
    """
    Use case for updating an existing booking.
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

    async def execute(
        self, booking_id: str, booking_data: BookingUpdateDTO
    ) -> BookingResponseDTO:
        logger.info(f"Attempting to update booking {booking_id}")

        async with self._sessionmaker() as session:
            try:
                existing_booking = await self._booking_repository.get_by_id(
                    booking_id, session
                )
                if not existing_booking:
                    raise BookingNotFoundException(identifier=booking_id)

                updated_booking = await self._booking_repository.update(
                    booking_id, session, **booking_data.model_dump(exclude_unset=True)
                )
                await session.commit()

                booking_seats = (
                    await self._booking_seat_repository.get_booking_seats_by_booking_id(
                        booking_id, session
                    )
                )

                # Convert booking_seats to DTOs
                from src.application.dtos.booking_dtos import BookingSeatResponseDTO
                booking_seats_response = [
                    BookingSeatResponseDTO.model_validate(seat) for seat in booking_seats
                ]

                logger.info(f"Booking {booking_id} updated successfully.")
                return BookingResponseDTO(
                    id=updated_booking.id,
                    user_id=updated_booking.user_id,
                    status=updated_booking.status,
                    created_at=updated_booking.created_at,
                    paid_at=updated_booking.paid_at,
                    total_price=updated_booking.total_price,
                    payment_method_id=updated_booking.payment_method_id,
                    voucher_id=updated_booking.voucher_id,
                    payment_reference=updated_booking.payment_reference,
                    booking_seats=booking_seats_response,
                )

            except BookingNotFoundException:
                raise
            except Exception as e:
                await session.rollback()
                logger.error(f"Error updating booking {booking_id}: {str(e)}")
                raise BookingUpdateFailedException(
                    id=booking_id, message="Failed to update booking"
                )
