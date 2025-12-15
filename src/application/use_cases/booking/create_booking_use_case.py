from typing import List

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config.logging_config import logger
from src.application.dtos.booking_dtos import (
    BookingCreateDTO,
    BookingResponseDTO,
    BookingSeatResponseDTO,
)
from src.domain.enums.booking_status import BookingStatus
from src.domain.exceptions.booking_exceptions import BookingCreationFailedException
from src.domain.exceptions.seat_exceptions import (
    SeatAlreadyReservedException,
    SeatNotFoundException,
)
from src.domain.exceptions.showtime_exceptions import ShowTimeNotFoundException
from src.domain.models.booking import Booking
from src.domain.models.booking_seat import BookingSeat
from src.domain.repositories.booking_repository import BookingRepository
from src.domain.repositories.booking_seat_repository import BookingSeatRepository
from src.domain.repositories.seat_repository import SeatRepository
from src.domain.repositories.showtime_repository import ShowTimeRepository


class CreateBookingUseCase:
    """
    Use case for creating a new booking.
    """

    def __init__(
        self,
        booking_repository: BookingRepository,
        booking_seat_repository: BookingSeatRepository,
        showtime_repository: ShowTimeRepository,
        seat_repository: SeatRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._booking_repository = booking_repository
        self._booking_seat_repository = booking_seat_repository
        self._showtime_repository = showtime_repository
        self._seat_repository = seat_repository
        self._sessionmaker = sessionmaker

    async def execute(self, booking_data: BookingCreateDTO) -> BookingResponseDTO:
        logger.info(
            f"Attempting to create a new booking for user {booking_data.user_id}"
        )

        async with self._sessionmaker() as session:
            try:
                # Check if showtime exists
                showtime = await self._showtime_repository.get_by_id(
                    booking_data.showtime_id, session
                )
                if not showtime:
                    raise ShowTimeNotFoundException(
                        showtime_id=booking_data.showtime_id
                    )

                # Create the booking
                new_booking = Booking(
                    user_id=booking_data.user_id,
                    status=BookingStatus.CREATED,
                    payment_method_id=booking_data.payment_method_id,
                    voucher_id=booking_data.voucher_id,
                )
                created_booking = await self._booking_repository.create(
                    new_booking, session
                )

                total_price = 0.0
                booking_seats_response: List[BookingSeatResponseDTO] = []

                # Process booking seats
                for seat_data in booking_data.booking_seats:
                    # Check if seat exists
                    seat = await self._seat_repository.get_by_id(
                        seat_data.seat_id, session
                    )
                    if not seat:
                        raise SeatNotFoundException(seat_id=seat_data.seat_id)

                    # Get the price from the seat's category
                    seat_price = seat.category.base_price if seat.category else 0.0

                    # Check if seat is already booked for this showtime
                    existing_booking_seats = await self._booking_seat_repository.get_booking_seats_by_showtime_id(
                        booking_data.showtime_id, session
                    )
                    for existing_seat in existing_booking_seats:
                        if existing_seat.seat_id == seat_data.seat_id:
                            raise SeatAlreadyReservedException(seat_data.seat_id)

                    # Create booking seat
                    new_booking_seat = BookingSeat(
                        booking_id=created_booking.id,
                        showtime_id=booking_data.showtime_id,
                        seat_id=seat_data.seat_id,
                    )
                    created_booking_seat = await self._booking_seat_repository.create(
                        new_booking_seat, session
                    )
                    booking_seats_response.append(
                        BookingSeatResponseDTO.model_validate(created_booking_seat)
                    )
                    total_price += seat_price

                # Update total price of the booking
                updated_booking = await self._booking_repository.update(
                    created_booking.id, session, total_price=total_price
                )

                await session.commit()
                logger.info(f"Booking {updated_booking.id} created successfully.")

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

            except (
                ShowTimeNotFoundException,
                SeatNotFoundException,
                SeatAlreadyReservedException,
            ) as e:
                await session.rollback()
                logger.warning(f"Booking creation failed: {e.message}")
                raise
            except Exception as e:
                await session.rollback()
                logger.error(
                    f"Error creating booking for user {booking_data.user_id}: {e}"
                )

                error_str = str(e)
                error_type = type(e).__name__

                # Handle foreign key violations
                if (
                    "ForeignKeyViolation" in error_type
                    or "foreign key constraint" in error_str.lower()
                ):
                    if "user_id" in error_str:
                        raise BookingCreationFailedException(
                            message="Cannot create booking: User account not found",
                            details={
                                "reason": "The user account does not exist in our system",
                                "suggestion": "Please ensure you have completed the registration process",
                            },
                        )
                    elif "payment_method_id" in error_str:
                        raise BookingCreationFailedException(
                            message="Cannot create booking: Invalid payment method",
                            details={
                                "reason": "The selected payment method does not exist",
                                "suggestion": "Please select a valid payment method",
                            },
                        )
                    elif "voucher_id" in error_str:
                        raise BookingCreationFailedException(
                            message="Cannot create booking: Invalid voucher",
                            details={
                                "reason": "The voucher code does not exist or is invalid",
                                "suggestion": "Please check your voucher code and try again",
                            },
                        )

                # Handle integrity errors
                if "IntegrityError" in error_type:
                    raise BookingCreationFailedException(
                        message="Cannot create booking due to data integrity issue",
                        details={
                            "reason": "There was a problem with the booking data",
                            "suggestion": "Please verify all information and try again",
                        },
                    )

                # Generic error fallback
                raise BookingCreationFailedException(
                    message="Failed to create booking due to an unexpected error",
                    details={
                        "reason": "An unexpected error occurred while processing your booking",
                        "suggestion": "Please try again later or contact support if the problem persists",
                    },
                )
