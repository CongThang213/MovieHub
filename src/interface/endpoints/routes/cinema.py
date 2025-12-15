from typing import Annotated

from fastapi import APIRouter, status
from fastapi.params import Depends, Query

from config.logging_config import logger
from src.application.use_cases.cinema.create_cinema_use_case import (
    CreateCinemaUseCase,
)
from src.application.use_cases.cinema.delete_cinema_use_case import (
    DeleteCinemaUseCase,
)
from src.application.use_cases.cinema.get_cinema_use_case import GetCinemaUseCase
from src.application.use_cases.cinema.get_cinemas_by_city_use_case import (
    GetCinemasByCityUseCase,
)
from src.application.use_cases.cinema.get_cinemas_use_case import GetCinemasUseCase
from src.application.use_cases.cinema.update_cinema_use_case import (
    UpdateCinemaUseCase,
)
from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.exceptions.cinema_exceptions import CinemaNotFoundException
from src.interface.endpoints.dependencies.cinema_dependencies import (
    get_create_cinema_use_case,
    get_get_cinemas_use_case,
    get_get_cinema_use_case,
    get_get_cinemas_by_city_use_case,
    get_update_cinema_use_case,
    get_delete_cinema_use_case,
)
from src.interface.endpoints.schemas.mappers.cinema_schema_mappers import (
    CinemaSchemaMappers,
)
from src.interface.endpoints.schemas.cinema_schemas import (
    CinemaSchema,
    CinemaResponse,
    CinemasResponse,
    CinemaCreateRequest,
    CinemaUpdateRequest,
)

router = APIRouter(prefix="/cinemas", tags=["Cinemas"])


@router.post(
    "/",
    response_model=CinemaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new cinema",
    responses={
        status.HTTP_201_CREATED: {
            "model": CinemaSchema,
            "description": "Cinema created successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to create a cinema"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def create_cinema(
    request: CinemaCreateRequest,
    use_case: Annotated[CreateCinemaUseCase, Depends(get_create_cinema_use_case)],
):
    """Create a new cinema."""
    logger.debug(f"Received create cinema request: {request}")
    cinema_domain = CinemaSchemaMappers.to_domain(request)
    logger.info(f"Creating cinema: {cinema_domain.name}")
    result = await use_case.execute(cinema_domain)
    return CinemaResponse.model_validate({"cinema": result})


@router.get(
    "/",
    response_model=CinemasResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all cinemas with pagination",
    responses={
        status.HTTP_200_OK: {
            "model": CinemasResponse,
            "description": "List of cinemas retrieved successfully",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def get_cinemas(
    use_case: Annotated[GetCinemasUseCase, Depends(get_get_cinemas_use_case)],
    page: int = Query(PAGE_DEFAULT, ge=1, description="Page number (1-based)"),
    page_size: int = Query(
        PAGE_SIZE_DEFAULT, ge=1, le=100, description="Number of items per page"
    ),
):
    """Retrieve all cinemas with pagination."""
    logger.debug(f"Received get cinemas request: page={page}, page_size={page_size}")
    cinemas = await use_case.execute(page=page, page_size=page_size)
    return CinemasResponse.model_validate({"cinemas": cinemas})


@router.get(
    "/city/{city_id}",
    response_model=CinemasResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve cinemas by city with pagination",
    responses={
        status.HTTP_200_OK: {
            "model": CinemasResponse,
            "description": "List of cinemas for the city retrieved successfully",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def get_cinemas_by_city(
    city_id: str,
    use_case: Annotated[
        GetCinemasByCityUseCase, Depends(get_get_cinemas_by_city_use_case)
    ],
    page: int = Query(PAGE_DEFAULT, ge=1, description="Page number (1-based)"),
    page_size: int = Query(
        PAGE_SIZE_DEFAULT, ge=1, le=100, description="Number of items per page"
    ),
):
    """Retrieve all cinemas in a specific city with pagination."""
    logger.debug(
        f"Received get cinemas by city request: city_id={city_id}, page={page}, page_size={page_size}"
    )
    cinemas = await use_case.execute(city_id=city_id, page=page, page_size=page_size)
    return CinemasResponse.model_validate({"cinemas": cinemas})


@router.get(
    "/{cinema_id}",
    response_model=CinemaResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a cinema by ID",
    responses={
        status.HTTP_200_OK: {
            "model": CinemaSchema,
            "description": "Cinema retrieved successfully",
        },
        status.HTTP_404_NOT_FOUND: {"description": "Cinema not found"},
    },
)
async def get_cinema(
    cinema_id: str,
    use_case: Annotated[GetCinemaUseCase, Depends(get_get_cinema_use_case)],
):
    """Retrieve a cinema by its ID."""
    logger.debug(f"Received get cinema request: cinema_id={cinema_id}")
    cinema = await use_case.execute(cinema_id)
    return CinemaResponse.model_validate({"cinema": cinema})


@router.put(
    "/{cinema_id}",
    response_model=CinemaResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a cinema",
    responses={
        status.HTTP_200_OK: {
            "model": CinemaSchema,
            "description": "Cinema updated successfully",
        },
        status.HTTP_404_NOT_FOUND: {"description": "Cinema not found"},
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to update a cinema"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def update_cinema(
    cinema_id: str,
    request: CinemaUpdateRequest,
    use_case: Annotated[UpdateCinemaUseCase, Depends(get_update_cinema_use_case)],
):
    """Update a cinema."""
    logger.debug(f"Received update cinema request: cinema_id={cinema_id}, {request}")

    # Get existing cinema first
    get_use_case = use_case._cinema_repository
    async with use_case._sessionmaker() as session:
        existing_cinema = await get_use_case.get_by_id(cinema_id, session)
        if not existing_cinema:
            raise CinemaNotFoundException(cinema_id)

    # Create updated cinema domain model
    cinema_domain = CinemaSchemaMappers.to_domain(request, cinema_id)

    # Only update provided fields
    if request.city_id is not None:
        existing_cinema.city_id = cinema_domain.city_id
    if request.name is not None:
        existing_cinema.name = cinema_domain.name
    if request.address is not None:
        existing_cinema.address = cinema_domain.address
    if request.lat is not None:
        existing_cinema.lat = cinema_domain.lat
    if request.long is not None:
        existing_cinema.long = cinema_domain.long
    if request.rating is not None:
        existing_cinema.rating = cinema_domain.rating

    logger.info(f"Updating cinema: {cinema_id}")
    result = await use_case.execute(existing_cinema)
    return CinemaResponse.model_validate({"cinema": result})


@router.delete(
    "/{cinema_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a cinema",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Cinema deleted successfully"},
        status.HTTP_404_NOT_FOUND: {"description": "Cinema not found"},
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to delete a cinema"
        },
    },
)
async def delete_cinema(
    cinema_id: str,
    use_case: Annotated[DeleteCinemaUseCase, Depends(get_delete_cinema_use_case)],
):
    """Delete a cinema."""
    logger.debug(f"Received delete cinema request: cinema_id={cinema_id}")
    result = await use_case.execute(cinema_id)
    if not result:
        raise CinemaNotFoundException(cinema_id)
    logger.info(f"Cinema deleted: {cinema_id}")
