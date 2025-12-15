from datetime import date
from typing import Annotated, Optional, List

from fastapi import APIRouter, status, Query
from fastapi.params import Depends

from config.logging_config import logger
from src.application.use_cases.film.create_film_use_case import CreateFilmUseCase
from src.application.use_cases.film.get_film_use_case import GetFilmUseCase
from src.application.use_cases.film.get_films_use_case import GetFilmsUseCase
from src.application.use_cases.film.search_films_use_case import SearchFilmsUseCase
from src.application.use_cases.image.finalize_temp_image_use_case import (
    FinalizeTempImagesUseCase,
)
from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.interface.endpoints.dependencies.film_dependencies import (
    get_create_film_use_case,
    get_get_film_use_case,
    get_get_films_use_case,
    get_search_films_use_case,
)
from src.interface.endpoints.dependencies.image_dependencies import (
    get_finalize_temp_images_use_case,
)
from src.interface.endpoints.schemas.film_schemas import (
    FilmCreateRequest,
    FilmResponse,
    FilmsListResponse,
    FilmDetailResponse,
)
from src.interface.endpoints.schemas.mappers.film_schema_mappers import (
    FilmSchemaMappers,
)

router = APIRouter(prefix="/films", tags=["Films"])


@router.post(
    "/",
    response_model=FilmResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new film",
    responses={
        status.HTTP_201_CREATED: {
            "model": FilmResponse,
            "description": "Film created successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to create a film"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
        status.HTTP_409_CONFLICT: {
            "description": "Film with the same title already exists"
        },
    },
)
async def create_film(
    request: FilmCreateRequest,
    create_film_use_case: Annotated[
        CreateFilmUseCase, Depends(get_create_film_use_case)
    ],
    finalize_images_use_case: Annotated[
        FinalizeTempImagesUseCase, Depends(get_finalize_temp_images_use_case)
    ],
):
    """
    **Create a new film with comprehensive details**

    Create a new film entry in the system along with its associated information including
    cast members, promotions, and trailers. All operations are performed in a single
    transaction to ensure data consistency.

    ### What you can include:
    - **Film Details**: Title, description, duration, screening dates
    - **Images**: Thumbnail, poster, and background images
    - **Cast Members**: Actors/actresses with their roles and character names
    - **Promotions**: Special offers and promotional campaigns
    - **Trailers**: Video trailers with custom ordering
    - **Genres**: Associate the film with multiple genres

    ### Image Handling:
    Images should be uploaded first using the image upload endpoint, which returns
    temporary image IDs. These IDs are then passed in this request and will be
    finalized upon successful film creation.

    **Note**: All related data (casts, promotions, trailers) are created atomically
    with the film to maintain referential integrity.
    """
    logger.debug(f"Received create film request: {request}")

    # Convert schemas to domain models
    film_domain = FilmSchemaMappers.to_domain(request)

    casts_domain = (
        FilmSchemaMappers.cast_schemas_to_domain(request.casts)
        if request.casts
        else None
    )

    promotions_domain = (
        FilmSchemaMappers.promotion_schemas_to_domain(request.promotions)
        if request.promotions
        else None
    )

    trailers_domain = (
        FilmSchemaMappers.trailer_schemas_to_domain(request.trailers)
        if request.trailers
        else None
    )

    logger.info(f"Creating film: {film_domain.title}")

    # Execute the use case
    result = await create_film_use_case.execute(
        film=film_domain,
        genres=request.genres,
        casts=casts_domain,
        promotions=promotions_domain,
        trailers=trailers_domain,
    )

    # After successful film creation, finalize temporary images if provided
    temp_image_public_ids = []

    # Collect temporary image public IDs from the request (these are actually public_ids, not URLs)
    if request.film.thumbnail_image_url:
        temp_image_public_ids.append(request.film.thumbnail_image_url)

    if request.film.poster_image_url:
        temp_image_public_ids.append(request.film.poster_image_url)

    if request.film.background_image_url:
        temp_image_public_ids.append(request.film.background_image_url)

    # Finalize images if any were provided
    if temp_image_public_ids:
        logger.info(
            f"Finalizing {len(temp_image_public_ids)} temporary images for film {result.id}"
        )
        finalized_images = await finalize_images_use_case.execute(
            temp_image_ids=temp_image_public_ids,
            owner_id=result.id,
        )

        # Update the result with the actual image URLs from finalized images
        for image in finalized_images:
            if image.type.value == "film_thumbnail":
                result.thumbnail_image_url = image.url
            elif image.type.value == "film_poster":
                result.poster_image_url = image.url
            elif image.type.value == "film_background":
                result.background_image_url = image.url

        logger.info(
            f"Successfully finalized {len(finalized_images)} images for film {result.id}"
        )

    return FilmResponse.model_validate({"film": result})


@router.get(
    "/",
    response_model=FilmsListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get list of films with pagination",
    responses={
        status.HTTP_200_OK: {
            "model": FilmsListResponse,
            "description": "Films retrieved successfully",
        },
    },
)
async def get_films(
    page: Annotated[
        int, Query(ge=1, description="Page number (1-based)")
    ] = PAGE_DEFAULT,
    page_size: Annotated[
        int, Query(ge=1, le=100, description="Number of items per page")
    ] = PAGE_SIZE_DEFAULT,
    get_films_use_case: Annotated[
        GetFilmsUseCase, Depends(get_get_films_use_case)
    ] = None,
):
    """
    **Retrieve a paginated list of all films**

    Get a comprehensive list of films with pagination support. This endpoint returns
    basic film information for browsing and listing purposes.

    ### Pagination:
    - Default page size is configured in the system settings
    - Maximum page size is 100 items per request
    - Pages are 1-based (first page is 1, not 0)

    ### Response includes:
    - **Films**: Array of film objects with essential details
    - **Page Info**: Current page number and page size
    - **Total Count**: Total number of films available

    ### Example Usage:
    ```
    GET /films?page=1&page_size=20
    ```

    **Tip**: Use the `/films/search` endpoint for advanced filtering options.
    """
    logger.info(f"Retrieving films list - page: {page}, page_size: {page_size}")

    # Execute the use case to get films (returns FilmBrief objects)
    film_briefs = await get_films_use_case.execute(page=page, page_size=page_size)

    total = len(film_briefs) + (page - 1) * page_size if film_briefs else 0

    logger.info(f"Successfully retrieved {len(film_briefs)} films for page {page}")

    return FilmsListResponse(
        films=[
            FilmSchemaMappers.film_to_schema(film_brief.film)
            for film_brief in film_briefs
        ],
        page=page,
        page_size=page_size,
        total=total,
    )


@router.get(
    "/search",
    response_model=FilmsListResponse,
    status_code=status.HTTP_200_OK,
    summary="Search films with filters",
    responses={
        status.HTTP_200_OK: {
            "model": FilmsListResponse,
            "description": "Films retrieved successfully",
        },
    },
)
async def search_films(
    page: Annotated[
        int, Query(ge=1, description="Page number (1-based)")
    ] = PAGE_DEFAULT,
    page_size: Annotated[
        int, Query(ge=1, le=100, description="Number of items per page")
    ] = PAGE_SIZE_DEFAULT,
    title: Annotated[
        Optional[str],
        Query(description="Search by film title (partial match, case-insensitive)"),
    ] = None,
    genres: Annotated[
        Optional[List[str]],
        Query(description="Filter by genre names (e.g., ?genres=Action&genres=Comedy)"),
    ] = None,
    min_rating: Annotated[
        Optional[float], Query(ge=0, le=10, description="Minimum rating (0-10)")
    ] = None,
    max_rating: Annotated[
        Optional[float], Query(ge=0, le=10, description="Maximum rating (0-10)")
    ] = None,
    min_duration: Annotated[
        Optional[int], Query(ge=0, description="Minimum duration in minutes")
    ] = None,
    max_duration: Annotated[
        Optional[int], Query(ge=0, description="Maximum duration in minutes")
    ] = None,
    showing_from: Annotated[
        Optional[date],
        Query(description="Filter films showing from this date onwards (YYYY-MM-DD)"),
    ] = None,
    showing_until: Annotated[
        Optional[date],
        Query(description="Filter films showing until this date (YYYY-MM-DD)"),
    ] = None,
    search_films_use_case: Annotated[
        SearchFilmsUseCase, Depends(get_search_films_use_case)
    ] = None,
):
    """
    **Search and filter films with advanced criteria**

    Discover films using powerful search and filtering capabilities. Combine multiple
    criteria to find exactly what you're looking for.

    ### Search Options:
    - **Title Search**: Partial, case-insensitive text matching
    - **Genre Filter**: Select one or multiple genres
    - **Rating Range**: Set minimum and/or maximum ratings (0-10 scale)
    - **Duration Range**: Filter by film length in minutes
    - **Showing Dates**: Find films within a specific date range

    ### Filter Combinations:
    All filters can be combined for precise results. For example:
    - Action movies rated 8+ that are currently showing
    - Sci-Fi films between 90-150 minutes
    - Comedies with "love" in the title

    ### Usage Examples:

    **Search by title:**
    ```
    GET /films/search?title=quantum
    ```

    **Filter by multiple genres:**
    ```
    GET /films/search?genres=Sci-Fi&genres=Action
    ```

    **Filter by rating range:**
    ```
    GET /films/search?min_rating=7.5&max_rating=9.0
    ```

    **Filter by showing dates:**
    ```
    GET /films/search?showing_from=2024-01-01&showing_until=2024-12-31
    ```

    **Combine multiple filters:**
    ```
    GET /films/search?title=quantum&min_rating=8.0&genres=Sci-Fi&page=1&page_size=10
    ```

    ### Pagination:
    Results are paginated with configurable page size (max 100 items per page).
    """
    logger.info(
        f"Searching films - page: {page}, page_size: {page_size}, "
        f"title: {title}, genres: {genres}, min_rating: {min_rating}, "
        f"max_rating: {max_rating}, min_duration: {min_duration}, "
        f"max_duration: {max_duration}, showing_from: {showing_from}, "
        f"showing_until: {showing_until}"
    )

    # Execute the search use case
    film_briefs, total = await search_films_use_case.execute(
        page=page,
        page_size=page_size,
        title=title,
        genres=genres,
        min_rating=min_rating,
        max_rating=max_rating,
        min_duration=min_duration,
        max_duration=max_duration,
        showing_from=showing_from,
        showing_until=showing_until,
    )

    logger.info(
        f"Successfully retrieved {len(film_briefs)} films (total: {total}) for page {page}"
    )

    return FilmsListResponse(
        films=[
            FilmSchemaMappers.film_to_schema(film_brief.film)
            for film_brief in film_briefs
        ],
        page=page,
        page_size=page_size,
        total=total,
    )


@router.get(
    "/{film_id}",
    response_model=FilmDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Get film details by ID",
    responses={
        status.HTTP_200_OK: {
            "model": FilmDetailResponse,
            "description": "Film details retrieved successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Film not found with the provided ID"
        },
    },
)
async def get_film_details(
    film_id: str,
    get_film_use_case: Annotated[GetFilmUseCase, Depends(get_get_film_use_case)],
):
    """
    **Get comprehensive details for a specific film**

    Retrieve complete information about a film including all associated data such as
    cast, genres, trailers, promotions, and more.

    ### Response Includes:

    **Basic Information:**
    - Title, description, and duration
    - Ratings and vote counts
    - Screening start and end dates

    **Visual Assets:**
    - Thumbnail image
    - Poster image
    - Background image

    **Related Data:**
    - **Cast**: Actors with character names and roles
    - **Genres**: Associated genre classifications
    - **Trailers**: Video previews with custom ordering
    - **Promotions**: Active promotional campaigns
    - **Showtimes**: Available screening times
    - **Reviews**: User reviews and ratings

    ### Use Cases:
    - Display detailed film page
    - Show complete film information in modals
    - Fetch data for booking flow
    - Present comprehensive film catalog

    **Note**: This endpoint returns the complete film object with all relationships populated.
    """
    logger.info(f"Retrieving film details for film ID: {film_id}")

    # Execute the use case to get the film
    film_detail = await get_film_use_case.execute(film_id=film_id)

    logger.info(f"Successfully retrieved film details: {film_detail.film.title}")

    return FilmDetailResponse.model_validate(film_detail, from_attributes=True)
