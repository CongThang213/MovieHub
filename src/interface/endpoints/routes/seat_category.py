from typing import Annotated

from fastapi import APIRouter, status
from fastapi.params import Depends, Query

from config.logging_config import logger
from src.application.use_cases.seat_category.create_seat_category_use_case import (
    CreateSeatCategoryUseCase,
)
from src.application.use_cases.seat_category.delete_seat_category_use_case import (
    DeleteSeatCategoryUseCase,
)
from src.application.use_cases.seat_category.get_seat_category_use_case import (
    GetSeatCategoryUseCase,
)
from src.application.use_cases.seat_category.get_seat_categories_use_case import (
    GetSeatCategoriesUseCase,
)
from src.application.use_cases.seat_category.update_seat_category_use_case import (
    UpdateSeatCategoryUseCase,
)
from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.interface.endpoints.dependencies.seat_category_dependencies import (
    get_create_seat_category_use_case,
    get_get_seat_categories_use_case,
    get_get_seat_category_use_case,
    get_update_seat_category_use_case,
    get_delete_seat_category_use_case,
)
from src.interface.endpoints.schemas.mappers.seat_category_schema_mappers import (
    SeatCategorySchemaMappers,
)
from src.interface.endpoints.schemas.seat_category_schemas import (
    SeatCategorySchema,
    SeatCategoryResponse,
    SeatCategoriesResponse,
    SeatCategoryCreateRequest,
    SeatCategoryUpdateRequest,
)

router = APIRouter(prefix="/seat-categories", tags=["Seat Categories"])


@router.post(
    "/",
    response_model=SeatCategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new seat category",
    responses={
        status.HTTP_201_CREATED: {
            "model": SeatCategorySchema,
            "description": "Seat category created successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to create a seat category"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def create_seat_category(
    request: SeatCategoryCreateRequest,
    use_case: Annotated[
        CreateSeatCategoryUseCase, Depends(get_create_seat_category_use_case)
    ],
):
    """Create a new seat category."""
    logger.debug(f"Received create seat category request: {request}")
    seat_category_domain = SeatCategorySchemaMappers.to_domain(request)
    logger.info(f"Creating seat category: {seat_category_domain.name}")
    result = await use_case.execute(seat_category_domain)
    return SeatCategoryResponse.model_validate({"seat_category": result})


@router.get(
    "/",
    response_model=SeatCategoriesResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all seat categories with pagination",
    responses={
        status.HTTP_200_OK: {
            "model": SeatCategoriesResponse,
            "description": "List of seat categories retrieved successfully",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def get_seat_categories(
    use_case: Annotated[
        GetSeatCategoriesUseCase, Depends(get_get_seat_categories_use_case)
    ],
    page: int = Query(PAGE_DEFAULT, ge=1, description="Page number (1-based)"),
    page_size: int = Query(
        PAGE_SIZE_DEFAULT, ge=1, le=100, description="Number of items per page"
    ),
):
    """Retrieve all seat categories with pagination."""
    logger.debug(
        f"Received get seat categories request: page={page}, page_size={page_size}"
    )
    seat_categories = await use_case.execute(page=page, page_size=page_size)
    return SeatCategoriesResponse.model_validate({"seat_categories": seat_categories})


@router.get(
    "/{seat_category_id}",
    response_model=SeatCategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a specific seat category by ID",
    responses={
        status.HTTP_200_OK: {
            "model": SeatCategorySchema,
            "description": "Seat category retrieved successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Seat category not found with the provided ID"
        },
    },
)
async def get_seat_category(
    seat_category_id: str,
    use_case: Annotated[
        GetSeatCategoryUseCase, Depends(get_get_seat_category_use_case)
    ],
):
    """Retrieve a specific seat category by ID."""
    logger.debug(f"Received get seat category request for id: {seat_category_id}")
    seat_category = await use_case.execute(seat_category_id)
    return SeatCategoryResponse.model_validate({"seat_category": seat_category})


@router.patch(
    "/{seat_category_id}",
    response_model=SeatCategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing seat category",
    responses={
        status.HTTP_200_OK: {
            "model": SeatCategorySchema,
            "description": "Seat category updated successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to update a seat category"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Seat category not found with the provided ID"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def update_seat_category(
    seat_category_id: str,
    request: SeatCategoryUpdateRequest,
    use_case: Annotated[
        UpdateSeatCategoryUseCase, Depends(get_update_seat_category_use_case)
    ],
    get_use_case: Annotated[
        GetSeatCategoryUseCase, Depends(get_get_seat_category_use_case)
    ],
):
    """Partially update an existing seat category (PATCH)."""
    logger.debug(
        f"Received update seat category request for id: {seat_category_id}, data: {request}"
    )

    # Get the existing seat category
    existing_seat_category = await get_use_case.execute(seat_category_id)

    # Update only the fields that were provided in the request
    update_data = request.model_dump(exclude_unset=True)

    # Merge the updates with existing data
    if "name" in update_data:
        existing_seat_category.name = update_data["name"]
    if "base_price" in update_data:
        existing_seat_category.base_price = update_data["base_price"]
    if "attributes" in update_data:
        existing_seat_category.attributes = update_data["attributes"]

    logger.info(
        f"Updating seat category: {seat_category_id} with fields: {list(update_data.keys())}"
    )
    result = await use_case.execute(existing_seat_category)
    return SeatCategoryResponse.model_validate({"seat_category": result})


@router.delete(
    "/{seat_category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a seat category",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Seat category deleted successfully"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to delete a seat category"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Seat category not found with the provided ID"
        },
    },
)
async def delete_seat_category(
    seat_category_id: str,
    use_case: Annotated[
        DeleteSeatCategoryUseCase, Depends(get_delete_seat_category_use_case)
    ],
):
    """Delete a seat category."""
    logger.debug(f"Received delete seat category request for id: {seat_category_id}")
    logger.info(f"Deleting seat category: {seat_category_id}")
    await use_case.execute(seat_category_id)
