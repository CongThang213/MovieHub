from src.domain.exceptions.app_exception import AppException


class FilmFormatNotFoundException(AppException):
    """Exception raised when a film format is not found."""

    def __init__(self, format_id: str):
        """
        Exception raised when a film format with the specified ID is not found.
        :param format_id: The ID of the film format that was not found.
        """
        super().__init__(
            status_code=404,
            error_code="FILM_FORMAT_NOT_FOUND",
            message=f"Film format with id '{format_id}' not found.",
            details={"format_id": format_id},
        )
