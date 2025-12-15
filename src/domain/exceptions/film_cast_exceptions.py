from src.domain.exceptions.app_exception import AppException


class FilmCastNotFoundException(AppException):
    """Exception raised when a film cast is not found."""

    def __init__(self, film_id: str, cast_id: str):
        """
        Exception raised when a film cast with the specified ID is not found.
        :param film_id: The ID of the film that was not found.
        :param cast_id: The ID of the cast that was not found.
        """
        super().__init__(
            status_code=404,
            error_code="FILM_NOT_FOUND",
            message=f"FilmCast not found.",
            details={
                "film cast_id": film_id,
                "cast_id": cast_id,
            },
        )
