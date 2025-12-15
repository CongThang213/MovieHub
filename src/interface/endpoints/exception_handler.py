from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from src.domain.exceptions.app_exception import AppException
from src.utilities.common_utilities import to_exception_response


async def app_exception_handler(
    request: Request, exception: AppException
) -> JSONResponse:
    """
    This function formats the response for exceptions raised in the application.

    Args:
        request (Request): The incoming request object.
        exception (AppException): The exception that was raised.

    Returns:
        JSONResponse: A JSON response containing the error details.
    """
    return to_exception_response(exception)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    This function formats validation errors to match the AppException structure.

    Args:
        request (Request): The incoming request object.
        exc (RequestValidationError): The validation exception that was raised.

    Returns:
        JSONResponse: A JSON response containing the validation error details.
    """
    errors = []
    for err in exc.errors():
        # Skip 'body' or 'query' in the location path for cleaner field names
        field_path = (
            ".".join(str(loc) for loc in err["loc"][1:])
            if len(err["loc"]) > 1
            else str(err["loc"][0])
        )

        error_detail = {
            "field": field_path,
            "message": err["msg"],
            "input": err.get("input"),
        }

        # Add expected value if available (for enum errors)
        if "ctx" in err and "expected" in err["ctx"]:
            error_detail["expected"] = err["ctx"]["expected"]

        errors.append(error_detail)

    return JSONResponse(
        status_code=422,
        content={
            "status_code": 422,
            "error_code": "VALIDATION_ERROR",
            "message": "Input validation error occurred",
            "details": errors,
        },
    )
