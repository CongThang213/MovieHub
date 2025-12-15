from src.domain.exceptions.app_exception import AppException


class FilmNotFoundException(AppException):
    """Exception raised when a film is not found."""

    def __init__(self, film_id: str):
        """
        Exception raised when a film with the specified ID is not found.
        :param film_id: The ID of the film that was not found.
        """
        super().__init__(
            status_code=404,
            error_code="FILM_NOT_FOUND",
            message=f"Film with id '{film_id}' not found.",
            details={"film_id": film_id},
        )
