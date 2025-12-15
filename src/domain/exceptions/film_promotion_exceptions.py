from src.domain.exceptions.app_exception import AppException


class FilmPromotionNotFoundException(AppException):
    """Exception raised when a film promotion is not found."""

    def __init__(self, promotion_id: str):
        """
        Exception raised when a film promotion with the specified ID is not found.
        :param promotion_id: The ID of the film promotion that was not found.
        """
        super().__init__(
            status_code=404,
            error_code="FILM_PROMOTION_NOT_FOUND",
            message=f"Film promotion with id '{promotion_id}' not found.",
            details={"promotion_id": promotion_id},
        )
