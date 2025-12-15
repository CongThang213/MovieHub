from typing import Annotated

from fastapi import APIRouter, status
from fastapi.params import Depends, Query

from config.logging_config import logger
from src.application.use_cases.hall.create_hall_use_case import CreateHallUseCase
from src.application.use_cases.hall.delete_hall_use_case import DeleteHallUseCase
from src.application.use_cases.hall.get_hall_use_case import GetHallUseCase
from src.application.use_cases.hall.get_halls_by_cinema_use_case import (
    GetHallsByCinemaUseCase,
)
from src.application.use_cases.hall.get_halls_use_case import GetHallsUseCase
from src.application.use_cases.hall.update_hall_use_case import UpdateHallUseCase
from src.application.use_cases.hall_layout.create_hall_layout_use_case import (
    CreateHallLayoutUseCase,
)
from src.application.use_cases.hall_layout.get_hall_layout_use_case import (
    GetHallLayoutUseCase,
)
from src.application.use_cases.hall_layout.update_hall_layout_use_case import (
    UpdateHallLayoutUseCase,
)
from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.interface.endpoints.dependencies.hall_dependencies import (
    get_create_hall_use_case,
    get_get_halls_use_case,
    get_get_hall_use_case,
    get_get_halls_by_cinema_use_case,
    get_update_hall_use_case,
    get_delete_hall_use_case,
    get_create_hall_layout_use_case,
    get_update_hall_layout_use_case,
    get_get_hall_layout_use_case,
)
from src.interface.endpoints.schemas.hall_layout_schemas import (
    HallLayoutCreateRequest,
    HallLayoutUpdateRequest,
    HallLayoutSuccessResponse,
)
from src.interface.endpoints.schemas.hall_schemas import (
    HallSchema,
    HallResponse,
    HallsResponse,
    HallCreateRequest,
    HallUpdateRequest,
)
from src.interface.endpoints.schemas.mappers.hall_schema_mappers import (
    HallSchemaMappers,
)

router = APIRouter(prefix="/halls", tags=["Halls"])


@router.post(
    "/",
    response_model=HallResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new hall",
    responses={
        status.HTTP_201_CREATED: {
            "model": HallSchema,
            "description": "Hall created successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to create a hall"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def create_hall(
    request: HallCreateRequest,
    use_case: Annotated[CreateHallUseCase, Depends(get_create_hall_use_case)],
):
    """Create a new hall."""
    logger.debug(f"Received create hall request: {request}")
    hall_domain = HallSchemaMappers.to_domain(request)
    logger.info(f"Creating hall: {hall_domain.name} in cinema: {hall_domain.cinema_id}")
    result = await use_case.execute(hall_domain)
    return HallResponse.model_validate({"hall": result})


@router.get(
    "/",
    response_model=HallsResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all halls with pagination",
    responses={
        status.HTTP_200_OK: {
            "model": HallsResponse,
            "description": "List of halls retrieved successfully",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def get_halls(
    use_case: Annotated[GetHallsUseCase, Depends(get_get_halls_use_case)],
    page: int = Query(PAGE_DEFAULT, ge=1, description="Page number (1-based)"),
    page_size: int = Query(
        PAGE_SIZE_DEFAULT, ge=1, le=100, description="Number of items per page"
    ),
):
    """Retrieve all halls with pagination."""
    logger.debug(f"Received get halls request: page={page}, page_size={page_size}")
    halls = await use_case.execute(page=page, page_size=page_size)
    return HallsResponse.model_validate({"halls": halls})


@router.get(
    "/{hall_id}",
    response_model=HallResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a specific hall by ID",
    responses={
        status.HTTP_200_OK: {
            "model": HallResponse,
            "description": "Hall retrieved successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Hall not found",
        },
    },
)
async def get_hall(
    hall_id: str,
    use_case: Annotated[GetHallUseCase, Depends(get_get_hall_use_case)],
):
    """Retrieve a specific hall by ID."""
    logger.debug(f"Received get hall request: hall_id={hall_id}")
    hall = await use_case.execute(hall_id)
    return HallResponse.model_validate({"hall": hall})


@router.get(
    "/cinema/{cinema_id}",
    response_model=HallsResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all halls for a specific cinema with pagination",
    responses={
        status.HTTP_200_OK: {
            "model": HallsResponse,
            "description": "List of halls for the cinema retrieved successfully",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def get_halls_by_cinema(
    cinema_id: str,
    use_case: Annotated[
        GetHallsByCinemaUseCase, Depends(get_get_halls_by_cinema_use_case)
    ],
    page: int = Query(PAGE_DEFAULT, ge=1, description="Page number (1-based)"),
    page_size: int = Query(
        PAGE_SIZE_DEFAULT, ge=1, le=100, description="Number of items per page"
    ),
):
    """Retrieve all halls for a specific cinema with pagination."""
    logger.debug(
        f"Received get halls by cinema request: cinema_id={cinema_id}, page={page}, page_size={page_size}"
    )
    halls = await use_case.execute(cinema_id=cinema_id, page=page, page_size=page_size)
    return HallsResponse.model_validate({"halls": halls})


@router.patch(
    "/{hall_id}",
    response_model=HallResponse,
    status_code=status.HTTP_200_OK,
    summary="Partially update a hall",
    responses={
        status.HTTP_200_OK: {
            "model": HallResponse,
            "description": "Hall updated successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to update this hall"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Hall not found",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def update_hall(
    hall_id: str,
    request: HallUpdateRequest,
    use_case: Annotated[UpdateHallUseCase, Depends(get_update_hall_use_case)],
    get_use_case: Annotated[GetHallUseCase, Depends(get_get_hall_use_case)],
):
    """Partially update a hall (PATCH)."""
    logger.debug(f"Received update hall request: hall_id={hall_id}, request={request}")

    # Get the existing hall
    existing_hall = await get_use_case.execute(hall_id)

    # Update only the fields that were provided in the request
    update_data = request.model_dump(exclude_unset=True)

    # Merge the updates with existing data
    if "cinema_id" in update_data:
        existing_hall.cinema_id = update_data["cinema_id"]
    if "name" in update_data:
        existing_hall.name = update_data["name"]
    if "capacity" in update_data:
        existing_hall.capacity = update_data["capacity"]
    if "description" in update_data:
        existing_hall.description = update_data["description"]

    logger.info(f"Updating hall: {hall_id} with fields: {list(update_data.keys())}")
    result = await use_case.execute(existing_hall)
    return HallResponse.model_validate({"hall": result})


@router.delete(
    "/{hall_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a hall",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Hall deleted successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to delete this hall"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Hall not found",
        },
    },
)
async def delete_hall(
    hall_id: str,
    use_case: Annotated[DeleteHallUseCase, Depends(get_delete_hall_use_case)],
):
    """Delete a hall."""
    logger.debug(f"Received delete hall request: hall_id={hall_id}")
    logger.info(f"Deleting hall: {hall_id}")
    await use_case.execute(hall_id)
    return None


# Hall Layout Endpoints


@router.post(
    "/{hall_id}/layout",
    response_model=HallLayoutSuccessResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create hall layout with rows and seats",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Hall layout created successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Hall not found or seat category not found",
        },
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid layout configuration"},
    },
)
async def create_hall_layout(
    hall_id: str,
    request: HallLayoutCreateRequest,
    use_case: Annotated[
        CreateHallLayoutUseCase, Depends(get_create_hall_layout_use_case)
    ],
):
    """Create a complete hall layout with rows and seats.

    This endpoint creates all rows and seats for a hall in a single transaction.
    Seat codes (like A1, B3) are auto-generated based on row_label + seat_number.

    The request validates:
    - Hall exists
    - All seat category IDs are valid
    - Row labels and seat numbers are provided
    """
    logger.debug(f"Received create layout request for hall: {hall_id}")
    logger.info(f"Creating layout for hall {hall_id} with {len(request.rows)} rows")

    # Convert Pydantic models to dictionaries for the use case
    rows_data = [row.model_dump() for row in request.rows]

    result = await use_case.execute(hall_id, rows_data)

    return HallLayoutSuccessResponse(
        message="Hall layout created successfully",
        hall_id=result["hall_id"],
        total_rows=result["total_rows"],
        total_seats=result["total_seats"],
        layout={
            "hall_id": result["hall_id"],
            "total_seats": result["total_seats"],
            "rows": [
                {
                    "id": row_data["row"].id,
                    "row_label": row_data["row"].row_label,
                    "row_order": row_data["row"].row_order,
                    "seats": [
                        {
                            "id": seat.id,
                            "seat_number": seat.seat_number,
                            "seat_code": f"{row_data['row'].row_label}{seat.seat_number}",
                            "category_id": seat.category_id,
                            "pos_x": seat.pos_x,
                            "pos_y": seat.pos_y,
                            "is_accessible": seat.is_accessible,
                            "external_label": seat.external_label,
                        }
                        for seat in row_data["seats"]
                    ],
                }
                for row_data in result["rows"]
            ],
        },
    )


@router.put(
    "/{hall_id}/layout",
    response_model=HallLayoutSuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Update hall layout (replaces entire layout)",
    responses={
        status.HTTP_200_OK: {
            "description": "Hall layout updated successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Hall not found or seat category not found",
        },
    },
)
async def update_hall_layout(
    hall_id: str,
    request: HallLayoutUpdateRequest,
    use_case: Annotated[
        UpdateHallLayoutUseCase, Depends(get_update_hall_layout_use_case)
    ],
):
    """Update the complete hall layout.

    This endpoint replaces the entire existing layout with the new configuration.
    All existing rows and seats will be deleted and replaced in a single transaction.

    The request validates:
    - Hall exists
    - All seat category IDs are valid
    - Row labels and seat numbers are provided
    """
    logger.debug(f"Received update layout request for hall: {hall_id}")
    logger.info(f"Updating layout for hall {hall_id} with {len(request.rows)} rows")

    # Convert Pydantic models to dictionaries for the use case
    rows_data = [row.model_dump() for row in request.rows]

    result = await use_case.execute(hall_id, rows_data)

    return HallLayoutSuccessResponse(
        message="Hall layout updated successfully",
        hall_id=result["hall_id"],
        total_rows=result["total_rows"],
        total_seats=result["total_seats"],
        layout={
            "hall_id": result["hall_id"],
            "total_seats": result["total_seats"],
            "rows": [
                {
                    "id": row_data["row"].id,
                    "row_label": row_data["row"].row_label,
                    "row_order": row_data["row"].row_order,
                    "seats": [
                        {
                            "id": seat.id,
                            "seat_number": seat.seat_number,
                            "seat_code": f"{row_data['row'].row_label}{seat.seat_number}",
                            "category_id": seat.category_id,
                            "pos_x": seat.pos_x,
                            "pos_y": seat.pos_y,
                            "is_accessible": seat.is_accessible,
                            "external_label": seat.external_label,
                        }
                        for seat in row_data["seats"]
                    ],
                }
                for row_data in result["rows"]
            ],
        },
    )


@router.get(
    "/{hall_id}/layout",
    status_code=status.HTTP_200_OK,
    summary="Get complete hall layout with rows and seats",
    responses={
        status.HTTP_200_OK: {
            "description": "Hall layout retrieved successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Hall not found",
        },
    },
)
async def get_hall_layout(
    hall_id: str,
    use_case: Annotated[GetHallLayoutUseCase, Depends(get_get_hall_layout_use_case)],
):
    """Get the complete seating layout for a hall.

    Returns all rows and their seats, ordered by row_order.
    Each seat includes its auto-generated seat code (e.g., 'A1', 'B3') and category information.
    """
    logger.debug(f"Received get layout request for hall: {hall_id}")

    result = await use_case.execute(hall_id)

    return {
        "hall_id": result["hall_id"],
        "total_seats": result["total_seats"],
        "rows": [
            {
                "id": row_data["row"].id,
                "row_label": row_data["row"].row_label,
                "row_order": row_data["row"].row_order,
                "seats": [
                    {
                        "id": seat.id,
                        "seat_number": seat.seat_number,
                        "seat_code": f"{row_data['row'].row_label}{seat.seat_number}",
                        "category_id": seat.category_id,
                        "pos_x": seat.pos_x,
                        "pos_y": seat.pos_y,
                        "is_accessible": seat.is_accessible,
                        "external_label": seat.external_label,
                        "seat_category": (
                            {
                                "id": seat.category.id,
                                "name": seat.category.name,
                                "base_price": seat.category.base_price,
                                "attributes": seat.category.attributes,
                            }
                            if seat.category
                            else None
                        ),
                    }
                    for seat in row_data["seats"]
                ],
            }
            for row_data in result["rows"]
        ],
    }
