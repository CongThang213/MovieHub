from src.domain.exceptions.app_exception import AppException


class HallNotFoundException(AppException):
    def __init__(self, hall_id: str):
        """
        Exception raised when a hall is not found by ID.
        :param hall_id: The ID of the hall that was not found.
        """
        super().__init__(
            status_code=404,  # HTTP 404 Not Found
            error_code="HALL_NOT_FOUND",
            message=f"Hall with id {hall_id} not found",
            details={"hall_id": hall_id},
        )


class HallAlreadyExistsException(AppException):
    def __init__(self, hall_name: str, cinema_id: str):
        """
        Exception raised when a hall with the same name already exists in a cinema.
        :param hall_name: The name of the hall that already exists.
        :param cinema_id: The cinema ID where the hall exists.
        """
        super().__init__(
            status_code=409,  # HTTP 409 Conflict
            error_code="HALL_ALREADY_EXISTS",
            message=f"Hall with name '{hall_name}' already exists in cinema {cinema_id}",
            details={"hall_name": hall_name, "cinema_id": cinema_id},
        )


class InvalidHallException(AppException):
    def __init__(self, message: str):
        """
        Exception raised when a hall is invalid.
        :param message: The error message.
        """
        super().__init__(
            status_code=400,  # HTTP 400 Bad Request
            error_code="INVALID_HALL",
            message=message,
            details={},
        )
