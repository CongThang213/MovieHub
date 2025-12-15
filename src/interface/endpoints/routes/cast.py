from typing import Annotated

from fastapi import APIRouter, status, Depends
from fastapi.params import Depends

from config.logging_config import logger
from src.application.use_cases.cast.create_cast_use_case import CreateCastUseCase
from src.application.use_cases.cast.delete_cast_use_case import DeleteCastUseCase
from src.application.use_cases.cast.get_cast_use_case import GetCastUseCase
from src.application.use_cases.cast.get_casts_use_case import GetCastsUseCase
from src.application.use_cases.cast.update_cast_use_case import UpdateCastUseCase
from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.exceptions.cast_exceptions import CastNotFoundException
from src.interface.endpoints.dependencies.cast_dependencies import (
    get_create_cast_use_case,
    get_get_casts_use_case,
    get_get_cast_use_case,
    get_update_cast_use_case,
    get_delete_cast_use_case,
)
from src.interface.endpoints.schemas.cast_schemas import (
    CastSchema,
    CastResponse,
    CastsResponse,
    CastCreateRequest,
    CastUpdateRequest,
)
from src.interface.endpoints.schemas.mappers.cast_schema_mappers import (
    CastSchemaMappers,
)

router = APIRouter(prefix="/casts", tags=["Casts"])


@router.post(
    "/",
    response_model=CastResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new cast member",
    responses={
        status.HTTP_201_CREATED: {
            "model": CastSchema,
            "description": "Cast member created successfully",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Cast member with the same name already exists"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to create a cast member"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def create_cast(
    request: CastCreateRequest,
    use_case: Annotated[CreateCastUseCase, Depends(get_create_cast_use_case)],
):
    """Create a new cast member.

    This endpoint allows the creation of a new cast member. It accepts a JSON payload
    containing the cast member details and returns the created cast member.

    Args:
        request (CastCreateRequest): The cast member details to create.
        use_case (CreateCastUseCase): The use case instance with injected repository dependencies.

    Returns:
        CastResponse: The created cast member details.
    """
    logger.debug(f"Received create cast request: {request}")
    cast_domain = CastSchemaMappers.to_domain(request)

    logger.info(f"Creating cast member: {cast_domain.name}")

    result = await use_case.execute(cast_domain)
    return CastResponse.model_validate({"cast": result})


@router.get(
    "/",
    response_model=CastsResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all cast members",
    responses={
        status.HTTP_200_OK: {
            "model": CastsResponse,
            "description": "List of cast members retrieved successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to view cast members"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the pagination parameters provided"
        },
    },
)
async def get_casts(
    page: int = PAGE_DEFAULT,
    page_size: int = PAGE_SIZE_DEFAULT,
    use_case: GetCastsUseCase = Depends(get_get_casts_use_case),
) -> CastsResponse:
    """Retrieve all cast members.

    This endpoint retrieves a list of all cast members.

    Args:
        page (int): The page number for pagination (default is 1).
        page_size (int): The number of items per page (default is 10).
        use_case (GetCastsUseCase): The use case instance with injected repository dependencies.

    Returns:
        CastsResponse: A list of cast members.
    """
    logger.debug(f"Received get casts request: page={page}, page_size={page_size}")

    casts = await use_case.execute(page, page_size)
    logger.info(f"Retrieved {len(casts)} cast members")

    # Convert domain models to response schemas for the response
    cast_schemas = CastSchemaMappers.from_domains(casts)
    # The response model wraps the list of casts in an outer object under the 'casts' key
    return CastsResponse.model_validate({"casts": cast_schemas})


@router.get(
    "/{cast_id}",
    response_model=CastResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a cast member by ID",
    responses={
        status.HTTP_200_OK: {
            "model": CastResponse,
            "description": "Cast member retrieved successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Cast member not found with the provided ID"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to view this cast member"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the cast member ID provided"
        },
    },
)
async def get_cast_by_id(
    cast_id: str,
    use_case: Annotated[GetCastUseCase, Depends(get_get_cast_use_case)],
) -> CastResponse:
    """Retrieve a cast member by ID.

    This endpoint retrieves a cast member based on the provided cast ID.

    Args:
        cast_id (str): The ID of the cast member to retrieve.
        use_case (GetCastUseCase): The use case instance with injected repository dependencies.

    Returns:
        CastResponse: The details of the retrieved cast member.
    """
    logger.debug(f"Received get cast by ID request: cast_id={cast_id}")

    cast = await use_case.execute(cast_id)
    if not cast:
        logger.warning(f"Cast member with ID {cast_id} not found")
        raise CastNotFoundException(cast_id=cast_id)

    logger.info(f"Retrieved cast member: {cast.name} (ID: {cast.id})")

    # Convert domain model to response schema for the response
    cast_schema = CastSchemaMappers.from_domain(cast)
    return CastResponse.model_validate({"cast": cast_schema})


@router.patch(
    "/{cast_id}",
    response_model=CastResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a cast member",
    responses={
        status.HTTP_200_OK: {
            "model": CastResponse,
            "description": "Cast member updated successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Cast member not found with the provided ID"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to update this cast member"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def update_cast(
    cast_id: str,
    request: CastUpdateRequest,
    use_case: Annotated[UpdateCastUseCase, Depends(get_update_cast_use_case)],
) -> CastResponse:
    """Update a cast member.

    This endpoint allows updating the details of an existing cast member. It accepts a JSON payload
    containing the updated cast member details and returns the updated cast member.

    Args:
        cast_id (str): The ID of the cast member to update.
        request (CastUpdateRequest): The updated cast member details.
        use_case (UpdateCastUseCase): The use case instance with injected repository dependencies.

    Returns:
        CastResponse: The updated cast member details.
    """
    logger.debug(f"Received update cast request: cast_id={cast_id}, request={request}")
    result = await use_case.execute(cast_id, **request.model_dump(exclude_unset=True))

    if not result:
        logger.warning(f"Cast member with ID {cast_id} not found during update")
        raise CastNotFoundException(cast_id=cast_id)

    logger.info(f"Updated cast member: {result.name} (ID: {result.id})")
    # Convert domain model to response schema for the response and return
    cast_schema = CastSchemaMappers.from_domain(result)
    return CastResponse.model_validate({"cast": cast_schema})


@router.delete(
    "/{cast_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a cast member",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Cast member deleted successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Cast member not found with the provided ID"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to delete this cast member"
        },
    },
)
async def delete_cast(
    cast_id: str,
    use_case: Annotated[DeleteCastUseCase, Depends(get_delete_cast_use_case)],
    get_cast_use_case: Annotated[GetCastUseCase, Depends(get_get_cast_use_case)],
) -> None:
    """Delete a cast member.

    This endpoint deletes a cast member based on the provided cast ID.

    Args:
        cast_id (str): The ID of the cast member to delete.
        use_case (DeleteCastUseCase): The use case instance with injected repository dependencies.
        get_cast_use_case (GetCastUseCase): The use case instance for retrieving a cast member.

    Returns:
        None
    """
    logger.debug(f"Received delete cast request: cast_id={cast_id}")

    # Check if the cast exists before attempting to delete
    cast = await get_cast_use_case.execute(cast_id)
    if not cast:
        logger.warning(f"Cast member with ID {cast_id} not found during delete")
        raise CastNotFoundException(cast_id=cast_id)

    await use_case.execute(cast_id)  # Perform deletion operation
    logger.info(f"Deleted cast member with ID: {cast_id}")
