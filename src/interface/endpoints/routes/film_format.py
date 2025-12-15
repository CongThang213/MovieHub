from typing import Annotated

from fastapi import APIRouter, status
from fastapi.params import Depends

from config.logging_config import logger
from src.application.use_cases.film_format.create_film_format_use_case import (
    CreateFilmFormatUseCase,
)
from src.application.use_cases.film_format.delete_film_format_use_case import (
    DeleteFilmFormatUseCase,
)
from src.application.use_cases.film_format.get_film_format_use_case import (
    GetFilmFormatUseCase,
)
from src.application.use_cases.film_format.get_film_formats_use_case import (
    GetFilmFormatsUseCase,
)
from src.application.use_cases.film_format.update_film_format_use_case import (
    UpdateFilmFormatUseCase,
)
from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.exceptions.film_format_exceptions import FilmFormatNotFoundException
from src.interface.endpoints.dependencies.film_format_dependencies import (
    get_create_film_format_use_case,
    get_get_film_formats_use_case,
    get_get_film_format_use_case,
    get_update_film_format_use_case,
    get_delete_film_format_use_case,
)
from src.interface.endpoints.schemas.film_format_schemas import (
    FilmFormatSchema,
    FilmFormatResponse,
    FilmFormatsResponse,
    FilmFormatCreateRequest,
    FilmFormatUpdateRequest,
)
from src.interface.endpoints.schemas.mappers.film_format_schema_mappers import (
    FilmFormatSchemaMappers,
)

router = APIRouter(prefix="/film-formats", tags=["Film Formats"])


@router.post(
    "/",
    response_model=FilmFormatResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new film format",
    responses={
        status.HTTP_201_CREATED: {
            "model": FilmFormatSchema,
            "description": "Film format created successfully",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Film format with the same name already exists"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to create a film format"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def create_film_format(
    request: FilmFormatCreateRequest,
    use_case: Annotated[
        CreateFilmFormatUseCase, Depends(get_create_film_format_use_case)
    ],
):
    """Create a new film format.

    This endpoint allows the creation of a new film format. It accepts a JSON payload
    containing the film format details and returns the created film format.

    Args:
        request (FilmFormatCreateRequest): The film format details to create.
        use_case (CreateFilmFormatUseCase): The use case instance with injected repository dependencies.

    Returns:
        FilmFormatResponse: The created film format details.
    """
    logger.debug(f"Received create film format request: {request}")
    film_format_domain = FilmFormatSchemaMappers.to_domain(request)

    logger.info(f"Creating film format: {film_format_domain.name}")

    result = await use_case.execute(film_format_domain)
    return FilmFormatResponse.model_validate({"film_format": result})


@router.get(
    "/",
    response_model=FilmFormatsResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all film formats with pagination",
    responses={
        status.HTTP_200_OK: {
            "model": FilmFormatsResponse,
            "description": "List of film formats retrieved successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to view film formats"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the pagination parameters provided"
        },
    },
)
async def get_film_formats(
    page: int = PAGE_DEFAULT,
    page_size: int = PAGE_SIZE_DEFAULT,
    use_case: GetFilmFormatsUseCase = Depends(get_get_film_formats_use_case),
) -> FilmFormatsResponse:
    """Retrieve all film formats with pagination.

    This endpoint retrieves a paginated list of all film formats. You can specify the page number
    and the number of items per page using query parameters.

    Args:
        page (int): The page number for pagination (default is 1).
        page_size (int): The number of items per page (default is 10).
        use_case (GetFilmFormatsUseCase): The use case instance with injected repository dependencies.

    Returns:
        FilmFormatsResponse: A list of film formats for the specified page and page size.
    """
    logger.debug(
        f"Received get film formats request: page={page}, page_size={page_size}"
    )

    film_formats = await use_case.execute(page, page_size)
    logger.info(
        f"Retrieved {len(film_formats)} film formats for page {page} with size {page_size}"
    )

    # Convert domain models to response schemas for the response
    film_format_schemas = FilmFormatSchemaMappers.from_domains(film_formats)
    # The response model wraps the list of film formats in an outer object under the 'film_formats' key
    return FilmFormatsResponse.model_validate({"film_formats": film_format_schemas})


@router.get(
    "/{format_id}",
    response_model=FilmFormatResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a film format by its ID",
    responses={
        status.HTTP_200_OK: {
            "model": FilmFormatResponse,
            "description": "Film format retrieved successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Film format not found with the provided ID"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to view this film format"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the film format ID provided"
        },
    },
)
async def get_film_format_by_id(
    format_id: str,
    use_case: Annotated[GetFilmFormatUseCase, Depends(get_get_film_format_use_case)],
) -> FilmFormatResponse:
    """Retrieve a film format by its ID.

    This endpoint retrieves a film format based on the provided film format ID.

    Args:
        format_id (str): The ID of the film format to retrieve.
        use_case (GetFilmFormatUseCase): The use case instance with injected repository dependencies.

    Returns:
        FilmFormatResponse: The details of the retrieved film format.
    """
    logger.debug(f"Received get film format by ID request: format_id={format_id}")

    film_format = await use_case.execute(format_id)
    if not film_format:
        logger.warning(f"Film format with ID {format_id} not found")
        raise FilmFormatNotFoundException(format_id=format_id)

    logger.info(f"Retrieved film format: {film_format.name} (ID: {film_format.id})")

    # Convert domain model to response schema for the response
    film_format_schema = FilmFormatSchemaMappers.from_domain(film_format)
    return FilmFormatResponse.model_validate({"film_format": film_format_schema})


@router.patch(
    "/{format_id}",
    response_model=FilmFormatResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing film format",
    responses={
        status.HTTP_200_OK: {
            "model": FilmFormatResponse,
            "description": "Film format updated successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Film format not found with the provided ID"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to update this film format"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def update_film_format(
    format_id: str,
    request: FilmFormatUpdateRequest,
    use_case: Annotated[
        UpdateFilmFormatUseCase, Depends(get_update_film_format_use_case)
    ],
) -> FilmFormatResponse:
    """Update an existing film format.

    This endpoint allows updating the details of an existing film format. It accepts a JSON payload
    containing the updated film format details and returns the updated film format.

    Args:
        format_id (str): The ID of the film format to update.
        request (FilmFormatUpdateRequest): The updated film format details.
        use_case (UpdateFilmFormatUseCase): The use case instance with injected repository dependencies.

    Returns:
        FilmFormatResponse: The updated film format details
    """
    logger.debug(
        f"Received update film format request: format_id={format_id}, request={request}"
    )
    result = await use_case.execute(format_id, **request.model_dump(exclude_unset=True))
    # Convert domain model to response schema for the response and return
    return FilmFormatResponse.model_validate({"film_format": result})


@router.delete(
    "/{format_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a film format by its ID",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Film format deleted successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Film format not found with the provided ID"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to delete this film format"
        },
    },
)
async def delete_film_format(
    format_id: str,
    use_case: Annotated[
        DeleteFilmFormatUseCase, Depends(get_delete_film_format_use_case)
    ],
) -> None:
    """Delete a film format by its ID.

    This endpoint deletes a film format based on the provided film format ID.

    Args:
        format_id (str): The ID of the film format to delete.
        use_case (DeleteFilmFormatUseCase): The use case instance with injected repository dependencies.

    Returns:
        None
    """
    logger.debug(f"Received delete film format request: format_id={format_id}")
    await use_case.execute(format_id)  # Perform deletion operation
    logger.info(f"Deleted film format with ID: {format_id}")
