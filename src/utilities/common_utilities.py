from starlette.responses import JSONResponse

from src.domain.exceptions.app_exception import AppException
from src.interface.endpoints.schemas.common_schemas import ErrorResponse


def to_exception_response(exception: AppException) -> JSONResponse:
    """Create a JSON response from a custom AppException using the standardized ErrorResponse schema."""
    error_response = ErrorResponse(
        error_code=exception.error_code,
        message=exception.message,
        details=exception.details,
    )

    return JSONResponse(
        status_code=exception.status_code,
        content=error_response.model_dump(exclude_none=True),
    )
