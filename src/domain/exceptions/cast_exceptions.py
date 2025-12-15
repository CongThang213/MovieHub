from src.domain.exceptions.app_exception import AppException


class CastNotFoundException(AppException):
    """Exception raised when a cast member is not found."""

    def __init__(self, cast_id: str):
        """
        Exception raised when a cast member with the specified ID is not found.
        :param cast_id: The ID of the cast member that was not found.
        """
        super().__init__(
            status_code=404,
            error_code="CAST_NOT_FOUND",
            message=f"Cast member with id '{cast_id}' not found.",
            details={"cast_id": cast_id},
        )
