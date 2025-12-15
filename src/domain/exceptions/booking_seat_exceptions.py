from src.domain.exceptions.app_exception import AppException


class BookingSeatNotFoundException(AppException):
    def __init__(self, identifier: str):
        """
        Exception raised when a booking seat is not found by ID.
        :param identifier: The identifier (ID) of the booking seat that was not found.
        """
        super().__init__(
            status_code=404,  # HTTP 404 Not Found
            error_code="BOOKING_SEAT_NOT_FOUND",
            message=f"Booking seat with id {identifier} not found",
            details={"identifier": identifier},
        )


class BookingSeatCreationFailedException(AppException):
    def __init__(self, message: str):
        """
        Exception raised when booking seat creation fails for any reason.
        :param message: A message describing the failure.
        """
        super().__init__(
            status_code=500,  # HTTP 500 Internal Server Error
            error_code="BOOKING_SEAT_CREATION_FAILED",
            message=message,
        )


class BookingSeatDeletionFailedException(AppException):
    def __init__(self, id: str, message: str = None):
        """
        Exception raised when booking seat deletion fails.
        :param id: The ID of the booking seat that could not be deleted.
        """
        super().__init__(
            status_code=500,  # HTTP 500 Internal Server Error
            error_code="BOOKING_SEAT_DELETION_FAILED",
            message=(
                message if message else f"Failed to delete booking seat with id {id}"
            ),
            details={"id": id},
        )


class BookingSeatUpdateFailedException(AppException):
    def __init__(self, id: str, message: str = None):
        """
        Exception raised when booking seat update fails.
        :param id: The ID of the booking seat that could not be updated.
        """
        super().__init__(
            status_code=500,  # HTTP 500 Internal Server Error
            error_code="BOOKING_SEAT_UPDATE_FAILED",
            message=(
                message if message else f"Failed to update booking seat with id {id}"
            ),
            details={"id": id},
        )
