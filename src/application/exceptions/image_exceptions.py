from src.domain.exceptions.app_exception import AppException


class ImageUploadException(AppException):
    def __init__(self, message: str, details: dict = None):
        """Exception raised for errors from the image storage provider.

        Args:
            message: A descriptive error message.
            details: Optional additional details about the error.
        """
        super().__init__(
            status_code=500,  # HTTP 500 Internal Server Error
            error_code="IMAGE_UPLOAD_ERROR",
            message=message,
            details=details or {},
        )


class ImageDeletionException(AppException):
    def __init__(self, public_id: str = None, details: dict = None):
        """Exception raised when image deletion fails.

        Args:
            public_id: The public ID of the image that failed to delete.
            details: Optional additional details about the failure.
        """
        super().__init__(
            status_code=500,  # HTTP 500 Internal Server Error
            error_code="IMAGE_DELETION_ERROR",
            message="Failed to delete the image",
            details={
                **({"public_id": public_id} if public_id is not None else {}),
                **(details or {}),
            },
        )


class ImageSizeLimitExceededException(AppException):
    def __init__(self, message: str, detail=None):
        """Exception raised when the uploaded image exceeds the size limit.

        Args:
            message: A descriptive error message.
            detail: Optional additional details about the error.
        """
        super().__init__(
            status_code=400,  # HTTP 400 Bad Request
            error_code="IMAGE_SIZE_LIMIT_EXCEEDED",
            message=message,
            details=detail or {},
        )
