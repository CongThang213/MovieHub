from src.domain.exceptions.app_exception import AppException


class GenreNotFoundException(AppException):
    def __init__(self, genre_id: str):
        """
        Exception raised when a genre is not found by ID.
        :param genre_id: The ID of the genre that was not found.
        """
        super().__init__(
            status_code=404,  # HTTP 404 Not Found
            error_code="GENRE_NOT_FOUND",
            message=f"Genre with id {genre_id} not found",
            details={"genre_id": genre_id},
        )
