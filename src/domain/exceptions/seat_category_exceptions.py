from src.domain.exceptions.app_exception import AppException


class SeatCategoryNotFoundException(AppException):
    def __init__(self, seat_category_id: str):
        """
        Exception raised when a seat category is not found by ID.
        :param seat_category_id: The ID of the seat category that was not found.
        """
        super().__init__(
            status_code=404,  # HTTP 404 Not Found
            error_code="SEAT_CATEGORY_NOT_FOUND",
            message=f"Seat category with id {seat_category_id} not found",
            details={"seat_category_id": seat_category_id},
        )


class SeatCategoryAlreadyExistsException(AppException):
    def __init__(self, seat_category_name: str):
        """
        Exception raised when a seat category with the same name already exists.
        :param seat_category_name: The name of the seat category that already exists.
        """
        super().__init__(
            status_code=409,  # HTTP 409 Conflict
            error_code="SEAT_CATEGORY_ALREADY_EXISTS",
            message=f"Seat category with name '{seat_category_name}' already exists",
            details={"seat_category_name": seat_category_name},
        )


class InvalidSeatCategoryException(AppException):
    def __init__(self, message: str):
        """
        Exception raised when a seat category is invalid.
        :param message: The error message.
        """
        super().__init__(
            status_code=400,  # HTTP 400 Bad Request
            error_code="INVALID_SEAT_CATEGORY",
            message=message,
            details={},
        )
