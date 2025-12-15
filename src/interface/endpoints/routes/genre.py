from typing import Annotated

from fastapi import APIRouter, Query, status
from fastapi.params import Depends

from config.logging_config import logger
from src.application.use_cases.genre.create_genre_use_case import CreateGenreUseCase
from src.application.use_cases.genre.delete_genre_use_case import DeleteGenreUseCase
from src.application.use_cases.genre.get_genre_use_case import GetGenreUseCase
from src.application.use_cases.genre.get_genres_use_case import GetGenresUseCase
from src.application.use_cases.genre.get_random_genres_use_case import (
    GetRandomGenresUseCase,
)
from src.application.use_cases.genre.update_genre_use_case import UpdateGenreUseCase
from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.exceptions.genre_exceptions import GenreNotFoundException
from src.interface.endpoints.dependencies.genre_dependencies import (
    get_create_genre_use_case,
    get_get_genres_use_case,
    get_get_genre_use_case,
    get_update_genre_use_case,
    get_delete_genre_use_case,
    get_get_random_genres_use_case,
)
from src.interface.endpoints.schemas.genre_schemas import (
    GenreSchema,
    GenreResponse,
    GenresResponse,
    GenreCreateRequest,
    GenreUpdateRequest,
    RandomGenresResponse,
)
from src.interface.endpoints.schemas.mappers.genre_schema_mappers import (
    GenreSchemaMappers,
)

router = APIRouter(prefix="/genres", tags=["Genres"])


@router.post(
    "/",
    response_model=GenreResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new genre for films",
    responses={
        status.HTTP_201_CREATED: {
            "model": GenreSchema,
            "description": "Genre created successfully",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Genre with the same name already exists"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Genre does not exist with the provided ID"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to create a genre"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def create_genre(
    request: GenreCreateRequest,
    use_case: Annotated[CreateGenreUseCase, Depends(get_create_genre_use_case)],
):
    """Create a new genre.

    This endpoint allows the creation of a new genre for films. It accepts a JSON payload
    containing the genre details and returns the created genre.

    Args:
        request (GenreSchema): The genre details to create.
        use_case (CreateGenreUseCase): The use case instance with injected repository dependencies.

    Returns:
        GenreSchema: The created genre details.
    """
    logger.debug(f"Received create genre request: {request}")
    genre_domain = GenreSchemaMappers.to_domain(request)

    logger.info(f"Creating genre: {genre_domain.name}")

    result = await use_case.execute(genre_domain)
    return GenreResponse.model_validate({"genre": result})


@router.get(
    "/",
    response_model=GenresResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all genres with pagination",
    responses={
        status.HTTP_200_OK: {
            "model": GenresResponse,
            "description": "List of genres retrieved successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to view genres"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the pagination parameters provided"
        },
    },
)
async def get_genres(
    page: int = PAGE_DEFAULT,
    page_size: int = PAGE_SIZE_DEFAULT,
    use_case: GetGenresUseCase = Depends(get_get_genres_use_case),
) -> GenresResponse:
    """Retrieve all genres with pagination and metadata (without total_items)."""
    logger.debug(f"Received get genres request: page={page}, page_size={page_size}")
    genres, total_items = await use_case.execute(page, page_size)
    logger.info(f"Retrieved {len(genres)} genres for page {page} with size {page_size}")
    genre_schemas = GenreSchemaMappers.from_domains(genres)
    total_pages = (total_items + page_size - 1) // page_size if page_size else 1
    return GenresResponse(
        genres=genre_schemas, page=page, page_size=page_size, total_pages=total_pages
    )


@router.get(
    "/random",
    response_model=RandomGenresResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve random genres",
    responses={
        status.HTTP_200_OK: {
            "model": RandomGenresResponse,
            "description": "Random genres retrieved successfully",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the limit parameter provided"
        },
    },
)
async def get_random_genres(
    limit: int = Query(4, ge=1),
    use_case: GetRandomGenresUseCase = Depends(get_get_random_genres_use_case),
) -> RandomGenresResponse:
    """Retrieve a random selection of genres."""
    genres, total_items = await use_case.execute(limit)
    genre_schemas = GenreSchemaMappers.from_domains(genres)
    return RandomGenresResponse(
        genres=genre_schemas, limit=limit, total_items=total_items
    )


@router.get(
    "/{genre_id}",
    response_model=GenreResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a genre by its ID",
    responses={
        status.HTTP_200_OK: {
            "model": GenreResponse,
            "description": "Genre retrieved successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Genre not found with the provided ID"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to view this genre"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the genre ID provided"
        },
    },
)
async def get_genre_by_id(
    genre_id: str,
    use_case: Annotated[GetGenreUseCase, Depends(get_get_genre_use_case)],
) -> GenreResponse:
    """Retrieve a genre by its ID.

    This endpoint retrieves a genre based on the provided genre ID.

    Args:
        genre_id (str): The ID of the genre to retrieve.
        use_case (GetGenreUseCase): The use case instance with injected repository dependencies.

    Returns:
        GenreResponse: The details of the retrieved genre.
    """
    logger.debug(f"Received get genre by ID request: genre_id={genre_id}")

    genre = await use_case.execute(genre_id)
    if not genre:
        logger.warning(f"Genre with ID {genre_id} not found")
        raise GenreNotFoundException(genre_id=genre_id)

    logger.info(f"Retrieved genre: {genre.name} (ID: {genre.id})")

    # Convert domain model to response schema for the response
    genre_schema = GenreSchemaMappers.from_domain(genre)
    return GenreResponse.model_validate({"genre": genre_schema})


@router.patch(
    "/{genre_id}",
    response_model=GenreResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing genre",
    responses={
        status.HTTP_200_OK: {
            "model": GenreResponse,
            "description": "Genre updated successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Genre not found with the provided ID"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to update this genre"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def update_genre(
    genre_id: str,
    request: GenreUpdateRequest,
    use_case: Annotated[UpdateGenreUseCase, Depends(get_update_genre_use_case)],
) -> GenreResponse:
    """Update an existing genre.

    This endpoint allows updating the details of an existing genre. It accepts a JSON payload
    containing the updated genre details and returns the updated genre.

    Args:
        genre_id (str): The ID of the genre to update.
        request (GenreUpdateRequest): The updated genre details.
        use_case (UpdateGenreUseCase): The use case instance with injected repository dependencies.

    Returns:
        GenreResponse: The updated genre details
    """
    logger.debug(
        f"Received update genre request: genre_id={genre_id}, request={request}"
    )
    result = await use_case.execute(genre_id, **request.model_dump(exclude_unset=True))
    # Convert domain model to response schema for the response and return
    return GenreResponse.model_validate({"genre": result})


@router.delete(
    "/{genre_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a genre by its ID",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Genre deleted successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Genre not found with the provided ID"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to delete this genre"
        },
    },
)
async def delete_genre(
    genre_id: str,
    use_case: Annotated[DeleteGenreUseCase, Depends(get_delete_genre_use_case)],
) -> None:
    """Delete a genre by its ID.

    This endpoint deletes a genre based on the provided genre ID.

    Args:
        genre_id (str): The ID of the genre to delete.
        use_case (UpdateGenreUseCase): The use case instance with injected repository dependencies.

    Returns:
        None
    """
    logger.debug(f"Received delete genre request: genre_id={genre_id}")
    await use_case.execute(genre_id)  # Perform deletion operation
    logger.info(f"Deleted genre with ID: {genre_id}")
