from src.domain.exceptions.app_exception import AppException


class CinemaNotFoundException(AppException):
    def __init__(self, cinema_id: str):
        """
        Exception raised when a cinema is not found by ID.
        :param cinema_id: The ID of the cinema that was not found.
        """
        super().__init__(
            status_code=404,  # HTTP 404 Not Found
            error_code="CINEMA_NOT_FOUND",
            message=f"Cinema with id {cinema_id} not found",
            details={"cinema_id": cinema_id},
        )


class CinemaAlreadyExistsException(AppException):
    def __init__(self, cinema_name: str):
        """
        Exception raised when a cinema with the same name already exists.
        :param cinema_name: The name of the cinema that already exists.
        """
        super().__init__(
            status_code=409,  # HTTP 409 Conflict
            error_code="CINEMA_ALREADY_EXISTS",
            message=f"Cinema with name '{cinema_name}' already exists",
            details={"cinema_name": cinema_name},
        )
