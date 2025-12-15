from src.domain.exceptions.app_exception import AppException


class ImageNotFoundException(AppException):
    def __init__(self, **kwargs):
        """Exception raised when an image is not found by ID or owner/type.

        Args:
            kwargs: Additional context for the exception

        Keyword Args:
            image_id: The ID of the image that was not found(if applicable)
            owner_id: The owner ID used in the lookup (if applicable)
            image_type: The type of image used in the lookup (if applicable)
        """
        # If none of the specific identifiers are provided, use a generic message
        if not any(k in kwargs for k in ("image_id", "owner_id", "image_type")):
            message = "Image not found with the provided criteria"
        else:
            parts = []
            if "image_id" in kwargs:
                parts.append(f"id {kwargs['image_id']}")
            if "owner_id" in kwargs:
                parts.append(f"owner ID {kwargs['owner_id']}")
            if "image_type" in kwargs:
                parts.append(f"type {kwargs['image_type']}")
            message = "Image with " + " and ".join(parts) + " not found"

        super().__init__(
            status_code=404,  # HTTP 404 Not Found
            error_code="IMAGE_NOT_FOUND",
            message=message,
            details=kwargs,
        )
