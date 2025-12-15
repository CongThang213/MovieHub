from typing import Annotated, List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from src.application.dtos.booking_dtos import (
    BookingCreateDTO,
    BookingSeatCreateDTO,
    BookingUpdateDTO,
)
from src.application.use_cases.booking.create_booking_use_case import (
    CreateBookingUseCase,
)
from src.application.use_cases.booking.delete_booking_use_case import (
    DeleteBookingUseCase,
)
from src.application.use_cases.booking.get_all_bookings_use_case import (
    GetAllBookingsUseCase,
)
from src.application.use_cases.booking.get_booking_use_case import GetBookingUseCase
from src.application.use_cases.booking.get_user_bookings_use_case import (
    GetUserBookingsUseCase,
)
from src.application.use_cases.booking.update_booking_use_case import (
    UpdateBookingUseCase,
)
from src.containers import AppContainer
from src.interface.endpoints.dependencies.auth_dependencies import (
    get_current_user,
    TokenData,
)
from src.interface.endpoints.schemas.booking_schemas import (
    BookingCreateRequest,
    BookingResponse,
    BookingUpdateRequest,
)
from src.interface.endpoints.schemas.common_schemas import MessageResponse

router = APIRouter(prefix="/bookings", tags=["Booking"])


@router.post(
    "/",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new booking",
    description="Creates a new booking with specified seats and optional payment/voucher details.",
)
@inject
async def create_booking(
    booking_request: BookingCreateRequest,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    create_booking_use_case: CreateBookingUseCase = Depends(
        Provide[AppContainer.use_cases.create_booking_use_case]
    ),
) -> BookingResponse:
    # Convert seat IDs to BookingSeatCreateDTO objects
    booking_seats = [
        BookingSeatCreateDTO(seat_id=seat_id)
        for seat_id in booking_request.booking_seat_ids
    ]

    booking_dto = BookingCreateDTO(
        user_id=current_user.user_id,
        showtime_id=booking_request.showtime_id,
        booking_seats=booking_seats,
        payment_method_id=booking_request.payment_method_id,
        voucher_id=booking_request.voucher_id,
    )
    return await create_booking_use_case.execute(booking_dto)


@router.get(
    "/{booking_id}",
    response_model=BookingResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a booking by ID",
    description="Retrieves a single booking's details by its unique ID.",
)
@inject
async def get_booking(
    booking_id: str,
    get_booking_use_case: GetBookingUseCase = Depends(
        Provide[AppContainer.use_cases.get_booking_use_case]
    ),
) -> BookingResponse:
    return await get_booking_use_case.execute(booking_id)


@router.put(
    "/{booking_id}",
    response_model=BookingResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a booking",
    description="Updates an existing booking's details by its unique ID.",
)
@inject
async def update_booking(
    booking_id: str,
    booking_request: BookingUpdateRequest,
    update_booking_use_case: UpdateBookingUseCase = Depends(
        Provide[AppContainer.use_cases.update_booking_use_case]
    ),
) -> BookingResponse:
    booking_dto = BookingUpdateDTO(**booking_request.model_dump(exclude_unset=True))
    return await update_booking_use_case.execute(booking_id, booking_dto)


@router.delete(
    "/{booking_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete a booking",
    description="Deletes a booking by its unique ID.",
)
@inject
async def delete_booking(
    booking_id: str,
    delete_booking_use_case: DeleteBookingUseCase = Depends(
        Provide[AppContainer.use_cases.delete_booking_use_case]
    ),
) -> MessageResponse:
    await delete_booking_use_case.execute(booking_id)
    return MessageResponse(message=f"Booking {booking_id} deleted successfully")


@router.get(
    "/",
    response_model=List[BookingResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all bookings",
    description="Retrieves a list of all bookings with pagination.",
)
@inject
async def get_all_bookings(
    skip: int = 0,
    limit: int = 100,
    get_all_bookings_use_case: GetAllBookingsUseCase = Depends(
        Provide[AppContainer.use_cases.get_all_bookings_use_case]
    ),
) -> List[BookingResponse]:
    return await get_all_bookings_use_case.execute(skip, limit)


@router.get(
    "/users/{user_id}/bookings",
    response_model=List[BookingResponse],
    status_code=status.HTTP_200_OK,
    summary="Get bookings by user ID",
    description="Retrieves a list of bookings for a specific user with pagination.",
)
@inject
async def get_user_bookings(
    user_id: str,
    skip: int = 0,
    limit: int = 100,
    get_user_bookings_use_case: GetUserBookingsUseCase = Depends(
        Provide[AppContainer.use_cases.get_user_bookings_use_case]
    ),
) -> List[BookingResponse]:
    return await get_user_bookings_use_case.execute(user_id, skip, limit)
