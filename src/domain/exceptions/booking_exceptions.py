from src.domain.exceptions.app_exception import AppException


class BookingNotFoundException(AppException):
    def __init__(self, identifier: str):
        """
        Exception raised when a booking is not found by ID.
        :param identifier: The identifier (ID) of the booking that was not found.
        """
        super().__init__(
            status_code=404,  # HTTP 404 Not Found
            error_code="BOOKING_NOT_FOUND",
            message=f"Booking with id {identifier} not found",
            details={"identifier": identifier},
        )


class BookingCreationFailedException(AppException):

    def __init__(self, message: str, details: dict = None):
        """
        Exception raised when booking creation fails for any reason.
        :param message: A message describing the failure.
        :param details: Additional details about the failure.
        """
        super().__init__(
            status_code=500,  # HTTP 500 Internal Server Error
            error_code="BOOKING_CREATION_FAILED",
            message=message,
            details=details or {},
        )


class BookingDeletionFailedException(AppException):
    def __init__(self, id: str, message: str = None):
        """
        Exception raised when booking deletion fails.
        :param id: The ID of the booking that could not be deleted.
        """
        super().__init__(
            status_code=500,  # HTTP 500 Internal Server Error
            error_code="BOOKING_DELETION_FAILED",
            message=message if message else f"Failed to delete booking with id {id}",
            details={"id": id},
        )


class BookingUpdateFailedException(AppException):
    def __init__(self, id: str, message: str = None):
        """
        Exception raised when booking update fails.
        :param id: The ID of the booking that could not be updated.
        """
        super().__init__(
            status_code=500,  # HTTP 500 Internal Server Error
            error_code="BOOKING_UPDATE_FAILED",
            message=message if message else f"Failed to update booking with id {id}",
            details={"id": id},
        )
