from src.domain.exceptions.app_exception import AppException


class SeatNotFoundException(AppException):
    def __init__(self, seat_id: str):
        """
        Exception raised when a seat is not found by ID.
        :param seat_id: The ID of the seat that was not found.
        """
        super().__init__(
            status_code=404,  # HTTP 404 Not Found
            error_code="SEAT_NOT_FOUND",
            message=f"Seat with id {seat_id} not found",
            details={"seat_id": seat_id},
        )


class SeatAlreadyExistsException(AppException):
    def __init__(self, row_id: str, seat_number: int):
        """
        Exception raised when a seat with the same number already exists in a row.
        :param row_id: The row ID where the seat exists.
        :param seat_number: The seat number that already exists.
        """
        super().__init__(
            status_code=409,  # HTTP 409 Conflict
            error_code="SEAT_ALREADY_EXISTS",
            message=f"Seat number {seat_number} already exists in row {row_id}",
            details={"row_id": row_id, "seat_number": seat_number},
        )


class InvalidSeatException(AppException):
    def __init__(self, message: str):
        """
        Exception raised when a seat is invalid.
        :param message: The error message.
        """
        super().__init__(
            status_code=400,  # HTTP 400 Bad Request
            error_code="INVALID_SEAT",
            message=message,
            details={},
        )


class SeatAlreadyReservedException(AppException):
    def __init__(self, seat_id: str):
        """
        Exception raised when a seat is already reserved or purchased.
        :param seat_id: The ID of the seat that is already reserved.
        """
        super().__init__(
            status_code=409,  # HTTP 409 Conflict
            error_code="SEAT_ALREADY_RESERVED",
            message=f"Seat with id {seat_id} is already reserved or purchased",
            details={"seat_id": seat_id},
        )
