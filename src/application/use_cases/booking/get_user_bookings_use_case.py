from typing import List

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config.logging_config import logger
from src.application.dtos.booking_dtos import (
    BookingResponseDTO,
    BookingSeatResponseDTO,
)
from src.domain.repositories.booking_repository import BookingRepository
from src.domain.repositories.booking_seat_repository import BookingSeatRepository


class GetUserBookingsUseCase:
    """
    Use case for retrieving all bookings for a specific user.
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
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[BookingResponseDTO]:
        logger.info(
            f"Retrieving bookings for user {user_id} with skip={skip}, limit={limit}"
        )

        async with self._sessionmaker() as session:
            try:
                bookings = await self._booking_repository.get_bookings_by_user_id(
                    user_id, session, skip, limit
                )
                booking_response_dtos = []
                for booking in bookings:
                    booking_seats = await self._booking_seat_repository.get_booking_seats_by_booking_id(
                        booking.id, session
                    )
                    booking_seats_response = [
                        BookingSeatResponseDTO.model_validate(seat)
                        for seat in booking_seats
                    ]
                    booking_response_dtos.append(
                        BookingResponseDTO(
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
                    )

                logger.info(
                    f"Successfully retrieved {len(bookings)} bookings for user {user_id}."
                )
                return booking_response_dtos

            except Exception as e:
                logger.error(f"Error retrieving bookings for user {user_id}: {str(e)}")
                raise
