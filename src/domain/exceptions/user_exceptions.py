from src.domain.exceptions.app_exception import AppException


class UserNotFoundException(AppException):
    def __init__(self, identifier: str):
        """
        Exception raised when a user is not found by ID or email.
        :param identifier: The identifier (ID or email) of the user that was not found.
        """
        super().__init__(
            status_code=404,  # HTTP 404 Not Found
            error_code="USER_NOT_FOUND",
            message=f"User with id/email {identifier} not found",
            details={"identifier": identifier},
        )


class UserCreationFailedException(AppException):
    def __init__(self, message: str):
        """
        Exception raised when user creation fails for any reason.
        :param message: A message describing the failure.
        """
        super().__init__(
            status_code=500,  # HTTP 500 Internal Server Error
            error_code="USER_CREATION_FAILED",
            message=message,
        )


class UserDeletionFailedException(AppException):
    def __init__(self, id: str, message: str = None):
        """
        Exception raised when user deletion fails.
        :param id: The ID of the user that could not be deleted.
        """
        super().__init__(
            status_code=500,  # HTTP 500 Internal Server Error
            error_code="USER_DELETION_FAILED",
            message=message if message else f"Failed to delete user with id {id}",
            details={"id": id},
        )
