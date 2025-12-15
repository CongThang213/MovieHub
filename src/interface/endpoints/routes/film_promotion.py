from typing import Annotated

from fastapi import APIRouter, status, Depends

from config.logging_config import logger
from src.application.use_cases.film_promotion.create_film_promotion_usecase import (
    CreateFilmPromotionUseCase,
)
from src.application.use_cases.film_promotion.delete_film_promotion_usecase import (
    DeleteFilmPromotionUseCase,
)
from src.application.use_cases.film_promotion.get_film_promotion_usecase import (
    GetFilmPromotionUseCase,
)
from src.application.use_cases.film_promotion.get_film_promotions_by_film_id_usecase import (
    GetFilmPromotionsByFilmIdUseCase,
)
from src.application.use_cases.film_promotion.update_film_promotion_usecase import (
    UpdateFilmPromotionUseCase,
)
from src.domain.exceptions.film_promotion_exceptions import (
    FilmPromotionNotFoundException,
)
from src.interface.endpoints.dependencies.film_promotion_dependencies import (
    get_create_film_promotion_use_case,
    get_delete_film_promotion_use_case,
    get_get_film_promotion_use_case,
    get_get_film_promotions_by_film_id_use_case,
    get_update_film_promotion_use_case,
)
from src.interface.endpoints.schemas.film_promotion_schemas import (
    FilmPromotionCreateRequest,
    FilmPromotionResponse,
    FilmPromotionsResponse,
    FilmPromotionUpdateRequest,
)
from src.interface.endpoints.schemas.mappers.film_promotion_schema_mappers import (
    FilmPromotionSchemaMappers,
)

router = APIRouter(prefix="/film-promotions", tags=["Film Promotions"])


@router.post(
    "/",
    response_model=FilmPromotionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new film promotion",
    responses={
        status.HTTP_201_CREATED: {
            "model": FilmPromotionResponse,
            "description": "Film promotion created successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to create a film promotion"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def create_film_promotion(
    request: FilmPromotionCreateRequest,
    use_case: Annotated[
        CreateFilmPromotionUseCase, Depends(get_create_film_promotion_use_case)
    ],
):
    """Create a new film promotion.

    This endpoint allows the creation of a new promotional offer for a film. It accepts a JSON payload
    containing the promotion details and returns the created promotion.

    ### Promotion Types:
    - **discount**: Promotional discounts or special pricing
    - **featured**: Featured/highlighted films
    - **premiere**: Premiere events
    - **special_event**: Special screenings or events

    Args:
        request (FilmPromotionCreateRequest): The promotion details to create.
        use_case (CreateFilmPromotionUseCase): The use case instance with injected repository dependencies.

    Returns:
        FilmPromotionResponse: The created film promotion details.
    """
    logger.debug(f"Received create film promotion request: {request}")
    promotion_domain = FilmPromotionSchemaMappers.to_domain(request)

    logger.info(
        f"Creating film promotion: {promotion_domain.title} for film {promotion_domain.film_id}"
    )

    result = await use_case.execute(promotion_domain)
    return FilmPromotionResponse.model_validate({"promotion": result})


@router.get(
    "/film/{film_id}",
    response_model=FilmPromotionsResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all promotions for a specific film",
    responses={
        status.HTTP_200_OK: {
            "model": FilmPromotionsResponse,
            "description": "List of film promotions retrieved successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to view film promotions"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the film ID provided"
        },
    },
)
async def get_film_promotions_by_film_id(
    film_id: str,
    use_case: Annotated[
        GetFilmPromotionsByFilmIdUseCase,
        Depends(get_get_film_promotions_by_film_id_use_case),
    ],
) -> FilmPromotionsResponse:
    """Retrieve all promotions for a specific film.

    This endpoint retrieves a list of all promotional offers associated with a specific film.

    Args:
        film_id (str): The ID of the film to retrieve promotions for.
        use_case (GetFilmPromotionsByFilmIdUseCase): The use case instance with injected repository dependencies.

    Returns:
        FilmPromotionsResponse: A list of film promotions for the specified film.
    """
    logger.debug(f"Received get film promotions by film ID request: film_id={film_id}")

    promotions = await use_case.execute(film_id)
    logger.info(f"Retrieved {len(promotions)} promotions for film {film_id}")

    # Convert domain models to response schemas for the response
    promotion_schemas = FilmPromotionSchemaMappers.from_domains(promotions)
    return FilmPromotionsResponse.model_validate({"promotions": promotion_schemas})


@router.get(
    "/{promotion_id}",
    response_model=FilmPromotionResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a film promotion by ID",
    responses={
        status.HTTP_200_OK: {
            "model": FilmPromotionResponse,
            "description": "Film promotion retrieved successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Film promotion not found with the provided ID"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to view this film promotion"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the promotion ID provided"
        },
    },
)
async def get_film_promotion_by_id(
    promotion_id: str,
    use_case: Annotated[
        GetFilmPromotionUseCase, Depends(get_get_film_promotion_use_case)
    ],
) -> FilmPromotionResponse:
    """Retrieve a film promotion by ID.

    This endpoint retrieves a film promotion based on the provided promotion ID.

    Args:
        promotion_id (str): The ID of the film promotion to retrieve.
        use_case (GetFilmPromotionUseCase): The use case instance with injected repository dependencies.

    Returns:
        FilmPromotionResponse: The details of the retrieved film promotion.
    """
    logger.debug(
        f"Received get film promotion by ID request: promotion_id={promotion_id}"
    )

    promotion = await use_case.execute(promotion_id)
    if not promotion:
        logger.warning(f"Film promotion with ID {promotion_id} not found")
        raise FilmPromotionNotFoundException(promotion_id=promotion_id)

    logger.info(f"Retrieved film promotion: {promotion.title} (ID: {promotion.id})")

    # Convert domain model to response schema for the response
    promotion_schema = FilmPromotionSchemaMappers.from_domain(promotion)
    return FilmPromotionResponse.model_validate({"promotion": promotion_schema})


@router.patch(
    "/{promotion_id}",
    response_model=FilmPromotionResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a film promotion",
    responses={
        status.HTTP_200_OK: {
            "model": FilmPromotionResponse,
            "description": "Film promotion updated successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Film promotion not found with the provided ID"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to update this film promotion"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def update_film_promotion(
    promotion_id: str,
    request: FilmPromotionUpdateRequest,
    use_case: Annotated[
        UpdateFilmPromotionUseCase, Depends(get_update_film_promotion_use_case)
    ],
) -> FilmPromotionResponse:
    """Update a film promotion.

    This endpoint allows updating the details of an existing film promotion. It accepts a JSON payload
    containing the updated promotion details and returns the updated promotion.

    Args:
        promotion_id (str): The ID of the film promotion to update.
        request (FilmPromotionUpdateRequest): The updated promotion details.
        use_case (UpdateFilmPromotionUseCase): The use case instance with injected repository dependencies.

    Returns:
        FilmPromotionResponse: The updated film promotion details.
    """
    logger.debug(
        f"Received update film promotion request: promotion_id={promotion_id}, request={request}"
    )
    result = await use_case.execute(
        promotion_id, **request.model_dump(exclude_unset=True)
    )

    if not result:
        logger.warning(f"Film promotion with ID {promotion_id} not found during update")
        raise FilmPromotionNotFoundException(promotion_id=promotion_id)

    logger.info(f"Updated film promotion: {result.title} (ID: {result.id})")
    # Convert domain model to response schema for the response and return
    promotion_schema = FilmPromotionSchemaMappers.from_domain(result)
    return FilmPromotionResponse.model_validate({"promotion": promotion_schema})


@router.delete(
    "/{promotion_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a film promotion",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Film promotion deleted successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Film promotion not found with the provided ID"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to delete this film promotion"
        },
    },
)
async def delete_film_promotion(
    promotion_id: str,
    use_case: Annotated[
        DeleteFilmPromotionUseCase, Depends(get_delete_film_promotion_use_case)
    ],
    get_promotion_use_case: Annotated[
        GetFilmPromotionUseCase, Depends(get_get_film_promotion_use_case)
    ],
) -> None:
    """Delete a film promotion.

    This endpoint allows deleting an existing film promotion by its ID.

    Args:
        promotion_id (str): The ID of the film promotion to delete.
        use_case (DeleteFilmPromotionUseCase): The use case instance with injected repository dependencies.
        get_promotion_use_case (GetFilmPromotionUseCase): The use case for checking if promotion exists.

    Returns:
        None: Returns 204 No Content on successful deletion.
    """
    logger.debug(f"Received delete film promotion request: promotion_id={promotion_id}")

    # Check if the promotion exists before attempting to delete
    promotion = await get_promotion_use_case.execute(promotion_id)
    if not promotion:
        logger.warning(f"Film promotion with ID {promotion_id} not found during delete")
        raise FilmPromotionNotFoundException(promotion_id=promotion_id)

    await use_case.execute(promotion_id)
    logger.info(f"Deleted film promotion with ID: {promotion_id}")
