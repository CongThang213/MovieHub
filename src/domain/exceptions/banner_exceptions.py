from src.domain.exceptions.app_exception import AppException


class BannerNotFoundException(AppException):
    def __init__(self, banner_id: str):
        """
        Exception raised when a banner is not found by ID.
        :param banner_id: The ID of the banner that was not found.
        """
        super().__init__(
            status_code=404,  # HTTP 404 Not Found
            error_code="BANNER_NOT_FOUND",
            message=f"Banner with id {banner_id} not found",
            details={"banner_id": banner_id},
        )
