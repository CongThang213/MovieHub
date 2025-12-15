from src.domain.exceptions.app_exception import AppException


class FilmTrailerNotFoundException(AppException):
    """Exception raised when a film trailer is not found."""

    def __init__(self, trailer_id: str):
        """
        Exception raised when a film trailer with the specified ID is not found.
        :param trailer_id: The ID of the film trailer that was not found.
        """
        super().__init__(
            status_code=404,
            error_code="FILM_TRAILER_NOT_FOUND",
            message=f"Film trailer with id '{trailer_id}' not found.",
            details={"trailer_id": trailer_id},
        )
