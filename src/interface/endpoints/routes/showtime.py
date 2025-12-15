from datetime import datetime
from typing import Annotated, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Query
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config.logging_config import logger
from src.application.use_cases.showtime.create_showtime_use_case import (
    CreateShowTimeUseCase,
)
from src.application.use_cases.showtime.delete_showtime_use_case import (
    DeleteShowTimeUseCase,
)
from src.application.use_cases.showtime.get_showtime_use_case import GetShowTimeUseCase
from src.application.use_cases.showtime.update_showtime_use_case import (
    UpdateShowTimeUseCase,
)
from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.containers import AppContainer
from src.infrastructure.repositories.showtime_repository_impl import (
    ShowTimeRepositoryImpl,
)
from src.interface.endpoints.dependencies.showtime_dependencies import (
    get_create_showtime_use_case,
    get_delete_showtime_use_case,
    get_get_showtime_use_case,
    get_update_showtime_use_case,
)
from src.interface.endpoints.schemas.mappers.showtime_schema_mappers import (
    ShowTimeSchemaMappers,
)
from src.interface.endpoints.schemas.showtime_schemas import (
    ShowTimeCreateRequest,
    ShowTimeResponse,
    ShowTimesResponse,
    ShowTimesListResponse,
    ShowTimeUpdateRequest,
    ShowTimesByFilmResponse,
)

router = APIRouter(prefix="/showtimes", tags=["Showtimes"])


@router.post(
    "/",
    response_model=ShowTimeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new showtime",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Showtime created successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to create a showtime"
        },
        status.HTTP_409_CONFLICT: {
            "description": "Time conflict: Hall is already booked for this time slot"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def create_showtime(
    request: ShowTimeCreateRequest,
    use_case: Annotated[CreateShowTimeUseCase, Depends(get_create_showtime_use_case)],
):
    """
    Create a new showtime for a film in a specific hall.

    This endpoint allows admins to schedule a film showing with specific start and end times.
    The system automatically validates for time conflicts to prevent double-booking halls.
    """
    logger.debug(f"Received create showtime request: {request}")
    showtime_domain = ShowTimeSchemaMappers.to_domain(request)
    logger.info(
        f"Creating showtime for film {showtime_domain.film_id} in hall {showtime_domain.hall_id}"
    )
    result = await use_case.execute(showtime_domain)
    return ShowTimeResponse.model_validate({"showtime": result})


@router.get(
    "/",
    response_model=ShowTimesResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all showtimes with pagination",
    responses={
        status.HTTP_200_OK: {
            "description": "List of showtimes retrieved successfully",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
@inject
async def get_showtimes(
    repository: Annotated[
        ShowTimeRepositoryImpl,
        Depends(Provide[AppContainer.repositories.showtime_repository]),
    ],
    sessionmaker: Annotated[
        async_sessionmaker[AsyncSession],
        Depends(Provide[AppContainer.database_settings.sessionmaker]),
    ],
    page: int = Query(PAGE_DEFAULT, ge=1, description="Page number (1-based)"),
    page_size: int = Query(
        PAGE_SIZE_DEFAULT, ge=1, le=100, description="Number of items per page"
    ),
    start_date: Optional[datetime] = Query(
        None, description="Start date and time to filter showtimes"
    ),
    end_date: Optional[datetime] = Query(
        None, description="End date and time to filter showtimes"
    ),
    film_id: Optional[str] = Query(None, description="Filter by film ID"),
    cinema_id: Optional[str] = Query(None, description="Filter by cinema ID"),
):
    """
    Retrieve all showtimes with pagination and optional filtering.

    Optionally filter by date range, film ID, and/or cinema ID to narrow down results.
    """
    logger.debug(
        f"Received get showtimes request: page={page}, page_size={page_size}, "
        f"start_date={start_date}, end_date={end_date}, film_id={film_id}, cinema_id={cinema_id}"
    )
    async with sessionmaker() as session:
        result = await repository.get_entities_all(
            page=page,
            page_size=page_size,
            session=session,
            start_date=start_date,
            end_date=end_date,
            film_id=film_id,
            cinema_id=cinema_id,
        )
    return ShowTimesResponse.model_validate(result)


@router.get(
    "/{showtime_id}",
    response_model=ShowTimeResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a specific showtime by ID",
    responses={
        status.HTTP_200_OK: {
            "description": "Showtime retrieved successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Showtime not found with the provided ID"
        },
    },
)
@inject
async def get_showtime(
    showtime_id: str,
    repository: Annotated[
        ShowTimeRepositoryImpl,
        Depends(Provide[AppContainer.repositories.showtime_repository]),
    ],
    sessionmaker: Annotated[
        async_sessionmaker[AsyncSession],
        Depends(Provide[AppContainer.database_settings.sessionmaker]),
    ],
):
    """Retrieve a specific showtime by its ID."""
    logger.debug(f"Received get showtime request for ID: {showtime_id}")
    async with sessionmaker() as session:
        showtime = await repository.get_entity_by_id(showtime_id, session)
        if not showtime:
            from src.domain.exceptions.showtime_exceptions import (
                ShowTimeNotFoundException,
            )

            raise ShowTimeNotFoundException(showtime_id)
    return ShowTimeResponse.model_validate({"showtime": showtime})


@router.get(
    "/film/{film_id}",
    response_model=ShowTimesByFilmResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all showtimes for a specific film grouped by cinema and hall",
    responses={
        status.HTTP_200_OK: {
            "description": "List of showtimes for the film grouped by cinema and hall retrieved successfully",
        },
    },
)
@inject
async def get_showtimes_by_film(
    film_id: str,
    repository: Annotated[
        ShowTimeRepositoryImpl,
        Depends(Provide[AppContainer.repositories.showtime_repository]),
    ],
    sessionmaker: Annotated[
        async_sessionmaker[AsyncSession],
        Depends(Provide[AppContainer.database_settings.sessionmaker]),
    ],
):
    """Retrieve all showtimes for a specific film grouped by cinema and hall.

    This endpoint is designed for displaying available showtimes before seat selection.
    Showtimes are organized hierarchically: Cinema -> Hall -> Showtimes.
    """
    logger.debug(f"Received get showtimes by film request for film ID: {film_id}")
    async with sessionmaker() as session:
        grouped_data = await repository.get_showtimes_grouped_by_cinema_and_hall(
            film_id, session
        )
    return ShowTimesByFilmResponse.model_validate(grouped_data)


@router.get(
    "/hall/{hall_id}",
    response_model=ShowTimesListResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all showtimes for a specific hall",
    responses={
        status.HTTP_200_OK: {
            "description": "List of showtimes for the hall retrieved successfully",
        },
    },
)
@inject
async def get_showtimes_by_hall(
    hall_id: str,
    repository: Annotated[
        ShowTimeRepositoryImpl,
        Depends(Provide[AppContainer.repositories.showtime_repository]),
    ],
    sessionmaker: Annotated[
        async_sessionmaker[AsyncSession],
        Depends(Provide[AppContainer.database_settings.sessionmaker]),
    ],
):
    """Retrieve all showtimes for a specific hall."""
    logger.debug(f"Received get showtimes by hall request for hall ID: {hall_id}")
    async with sessionmaker() as session:
        showtimes = await repository.get_entities_by_hall_id(hall_id, session)
    return ShowTimesListResponse.model_validate({"showtimes": showtimes})


@router.get(
    "/cinema/{cinema_id}",
    response_model=ShowTimesListResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all showtimes for a specific cinema",
    responses={
        status.HTTP_200_OK: {
            "description": "List of showtimes for the cinema retrieved successfully",
        },
    },
)
@inject
async def get_showtimes_by_cinema(
    cinema_id: str,
    repository: Annotated[
        ShowTimeRepositoryImpl,
        Depends(Provide[AppContainer.repositories.showtime_repository]),
    ],
    sessionmaker: Annotated[
        async_sessionmaker[AsyncSession],
        Depends(Provide[AppContainer.database_settings.sessionmaker]),
    ],
):
    """Retrieve all showtimes for a specific cinema."""
    logger.debug(f"Received get showtimes by cinema request for cinema ID: {cinema_id}")
    async with sessionmaker() as session:
        showtimes = await repository.get_entities_by_cinema_id(cinema_id, session)
    return ShowTimesListResponse.model_validate({"showtimes": showtimes})


@router.put(
    "/{showtime_id}",
    response_model=ShowTimeResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a showtime",
    responses={
        status.HTTP_200_OK: {
            "description": "Showtime updated successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to update a showtime"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Showtime not found with the provided ID"
        },
        status.HTTP_409_CONFLICT: {
            "description": "Time conflict: Hall is already booked for this time slot"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def update_showtime(
    showtime_id: str,
    request: ShowTimeUpdateRequest,
    get_showtime_use_case: Annotated[
        GetShowTimeUseCase, Depends(get_get_showtime_use_case)
    ],
    update_use_case: Annotated[
        UpdateShowTimeUseCase, Depends(get_update_showtime_use_case)
    ],
):
    """Update an existing showtime."""
    logger.debug(f"Received update showtime request for ID: {showtime_id}")

    # First get the existing showtime
    existing = await get_showtime_use_case.execute(showtime_id)

    # Merge with update data
    showtime_domain = ShowTimeSchemaMappers.update_to_domain(
        showtime_id, request, existing
    )
    logger.info(f"Updating showtime: {showtime_id}")
    result = await update_use_case.execute(showtime_domain)
    return ShowTimeResponse.model_validate({"showtime": result})


@router.patch(
    "/{showtime_id}",
    response_model=ShowTimeResponse,
    status_code=status.HTTP_200_OK,
    summary="Partially update a showtime",
    responses={
        status.HTTP_200_OK: {
            "description": "Showtime updated successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to update a showtime"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Showtime not found with the provided ID"
        },
        status.HTTP_409_CONFLICT: {
            "description": "Time conflict: Hall is already booked for this time slot"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def patch_showtime(
    showtime_id: str,
    request: ShowTimeUpdateRequest,
    get_showtime_use_case: Annotated[
        GetShowTimeUseCase, Depends(get_get_showtime_use_case)
    ],
    update_use_case: Annotated[
        UpdateShowTimeUseCase, Depends(get_update_showtime_use_case)
    ],
):
    """Partially update an existing showtime."""
    logger.debug(f"Received patch showtime request for ID: {showtime_id}")

    # First get the existing showtime
    existing = await get_showtime_use_case.execute(showtime_id)

    # Merge with update data
    showtime_domain = ShowTimeSchemaMappers.update_to_domain(
        showtime_id, request, existing
    )
    logger.info(f"Patching showtime: {showtime_id}")
    result = await update_use_case.execute(showtime_domain)
    return ShowTimeResponse.model_validate({"showtime": result})


@router.delete(
    "/{showtime_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a showtime",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Showtime deleted successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to delete a showtime"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Showtime not found with the provided ID"
        },
    },
)
async def delete_showtime(
    showtime_id: str,
    use_case: Annotated[DeleteShowTimeUseCase, Depends(get_delete_showtime_use_case)],
):
    """Delete a showtime."""

    logger.debug(f"Received delete showtime request for ID: {showtime_id}")
    await use_case.execute(showtime_id)
    logger.info(f"Deleted showtime: {showtime_id}")
