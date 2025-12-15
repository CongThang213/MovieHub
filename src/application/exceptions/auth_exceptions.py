from src.domain.exceptions.app_exception import AppException


class UserAlreadyExistsError(AppException):
    def __init__(self, email: str):
        """
        Exception raised when trying to create a user that already exists.
        :param email: The email of the user that already exists.
        """
        super().__init__(
            status_code=409,  # HTTP 409 Conflict
            error_code="USER_ALREADY_EXISTS",
            message=f"User with email {email} already exists",
            details={"email": email},
        )


class AuthenticationError(AppException):
    def __init__(self, message: str = "Authentication failed"):
        """
        Exception raised when authentication fails.
        :param message: Error message.
        """
        super().__init__(
            status_code=401,  # HTTP 401 Unauthorized
            error_code="AUTHENTICATION_FAILED",
            message=message,
        )


class ServiceUserNotFoundError(AppException):
    def __init__(self, identifier: str):
        """
        Exception raised when a user is not found.
        :param identifier: The identifier (email or ID) used to look up the user.
        """
        super().__init__(
            status_code=404,  # HTTP 404 Not Found
            error_code="USER_NOT_FOUND",
            message=f"User not found: {identifier}",
            details={"identifier": identifier},
        )


class InvalidCredentialsError(AppException):
    def __init__(self):
        """
        Exception raised when the provided credentials are invalid.
        """
        super().__init__(
            status_code=401,  # HTTP 401 Unauthorized
            error_code="INVALID_CREDENTIALS",
            message="Invalid email or password",
        )


class TokenExpiredError(AppException):
    def __init__(self):
        """
        Exception raised when the provided token has expired.
        """
        super().__init__(
            status_code=401,  # HTTP 401 Unauthorized
            error_code="TOKEN_EXPIRED",
            message="Authentication token has expired",
        )


class TokenMissingError(AppException):
    def __init__(self, message: str = "Authentication token is required"):
        """
        Exception raised when no authentication token is provided.
        """
        super().__init__(
            status_code=401,  # HTTP 401 Unauthorized
            error_code="TOKEN_MISSING",
            message=message,
        )


class InsufficientPermissionsError(AppException):

    def __init__(self, resource: str = None, action: str = None):
        """
        Exception raised when user lacks required permissions.

        Args:
            resource: The resource being accessed.
            action: The action being attempted.
        """
        message = "Insufficient permissions to access this resource"
        details = {}

        if resource:
            details["resource"] = resource
            message = f"Insufficient permissions to access {resource}"

        if action:
            details["action"] = action
            message = (
                f"Insufficient permissions to {action} {resource or 'this resource'}"
            )

        super().__init__(
            status_code=403,  # HTTP 403 Forbidden
            error_code="INSUFFICIENT_PERMISSIONS",
            message=message,
            details=details if details else None,
        )
