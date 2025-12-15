from src.domain.exceptions.app_exception import AppException


class ShowTimeNotFoundException(AppException):
    """Exception raised when a showtime is not found."""

    def __init__(self, showtime_id: str):
        super().__init__(
            status_code=404,
            message=f"Showtime with ID '{showtime_id}' not found",
            error_code="SHOWTIME_NOT_FOUND",
        )


class ShowTimeConflictException(AppException):
    """Exception raised when there's a time conflict for a showtime."""

    def __init__(self, hall_id: str, start_time: str, end_time: str):
        super().__init__(
            status_code=409,
            message=f"Time conflict: Hall '{hall_id}' is already booked between {start_time} and {end_time}",
            error_code="SHOWTIME_CONFLICT",
        )


class InvalidShowTimeException(AppException):
    """Exception raised when showtime data is invalid."""

    def __init__(self, message: str):
        super().__init__(
            status_code=400,
            message=message,
            error_code="INVALID_SHOWTIME",
        )
