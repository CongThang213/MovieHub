from src.domain.exceptions.app_exception import AppException


class FilmReviewNotFoundError(AppException):
    """Exception raised when a film review is not found."""

    def __init__(self, review_id: str):
        """
        Exception raised when a film review with the specified ID is not found.
        :param review_id: The ID of the review that was not found.
        """
        super().__init__(
            status_code=404,
            error_code="FILM_REVIEW_NOT_FOUND",
            message=f"Film review with id '{review_id}' not found.",
            details={"review_id": review_id},
        )


class FilmNotWatchedByUserError(AppException):
    """Exception raised when a user tries to review a film they haven't watched."""

    def __init__(self, user_id: str, film_id: str):
        """
        Exception raised when a user tries to review a film they haven't watched.
        :param user_id: The ID of the user.
        :param film_id: The ID of the film.
        """
        super().__init__(
            status_code=403,
            error_code="FILM_NOT_WATCHED",
            message="You can only review films you have watched.",
            details={"user_id": user_id, "film_id": film_id},
        )


class DuplicateReviewError(AppException):
    """Exception raised when a user tries to create a duplicate review."""

    def __init__(self, user_id: str, film_id: str):
        """
        Exception raised when a user tries to create a duplicate review for a film.
        :param user_id: The ID of the user.
        :param film_id: The ID of the film.
        """
        super().__init__(
            status_code=409,
            error_code="DUPLICATE_REVIEW",
            message="You have already reviewed this film. Please update your existing review instead.",
            details={"user_id": user_id, "film_id": film_id},
        )


class UnauthorizedReviewAccessError(AppException):
    """Exception raised when a user tries to access/modify a review they don't own."""

    def __init__(self, user_id: str, review_id: str):
        """
        Exception raised when a user tries to access/modify a review they don't own.
        :param user_id: The ID of the user attempting the action.
        :param review_id: The ID of the review.
        """
        super().__init__(
            status_code=403,
            error_code="UNAUTHORIZED_REVIEW_ACCESS",
            message="You can only modify your own reviews.",
            details={"user_id": user_id, "review_id": review_id},
        )
