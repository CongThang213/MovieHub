from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException

from config.logging_config import logger
from src.application.use_cases.film_review.create_film_review_use_case import (
    CreateFilmReviewUseCase,
)
from src.application.use_cases.film_review.delete_film_review_use_case import (
    DeleteFilmReviewUseCase,
)
from src.application.use_cases.film_review.get_film_review_use_case import (
    GetFilmReviewUseCase,
)
from src.application.use_cases.film_review.get_film_reviews_by_film_id_use_case import (
    GetFilmReviewsByFilmIdUseCase,
)
from src.application.use_cases.film_review.get_film_reviews_use_case import (
    GetFilmReviewsUseCase,
)
from src.application.use_cases.film_review.update_film_review_use_case import (
    UpdateFilmReviewUseCase,
)
from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.enums.account_type import AccountType
from src.domain.exceptions.film_review_exceptions import (
    UnauthorizedReviewAccessError,
)
from src.interface.endpoints.dependencies.auth_dependencies import (
    get_current_user,
    TokenData,
)
from src.interface.endpoints.dependencies.film_review_dependencies import (
    get_create_film_review_use_case,
    get_get_film_review_use_case,
    get_get_film_reviews_use_case,
    get_get_film_reviews_by_film_id_use_case,
    get_update_film_review_use_case,
    get_delete_film_review_use_case,
)
from src.interface.endpoints.schemas.film_review_schemas import (
    FilmReviewCreateRequest,
    FilmReviewUpdateRequest,
    FilmReviewResponse,
    FilmReviewsResponse,
)
from src.interface.endpoints.schemas.mappers.film_review_schema_mappers import (
    FilmReviewSchemaMappers,
)

router = APIRouter(prefix="/film-reviews", tags=["Film Reviews"])


@router.post(
    "/",
    response_model=FilmReviewResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new film review",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Film review created successfully",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Authentication required",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You can only review films you have watched",
        },
        status.HTTP_409_CONFLICT: {
            "description": "You have already reviewed this film",
        },
    },
)
async def create_film_review(
    request: FilmReviewCreateRequest,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    use_case: Annotated[
        CreateFilmReviewUseCase, Depends(get_create_film_review_use_case)
    ],
):
    """
    **Create a new film review (Customer only)**

    Customers can create reviews for films they have watched (have a paid booking for).

    ### Requirements:
    - User must be authenticated as a Customer
    - User must have watched the film (paid booking)
    - User cannot review the same film twice

    ### Request Body:
    - **film_id**: The ID of the film to review
    - **rating**: Rating from 1 to 5
    - **content**: Review text/comment
    """
    logger.debug(
        f"Received create film review request from user {current_user.user_id}"
    )

    # Only customers can create reviews
    if current_user.account_type != AccountType.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can create film reviews",
        )

    review_domain = FilmReviewSchemaMappers.to_domain(request, current_user.user_id)

    result = await use_case.execute(
        review=review_domain,
        user_id=current_user.user_id,
        film_id=request.film_id,
    )
    logger.info(f"Film review created successfully: {result.id}")
    return FilmReviewResponse(review=FilmReviewSchemaMappers.to_schema(result))


@router.get(
    "/",
    response_model=FilmReviewsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all film reviews",
    responses={
        status.HTTP_200_OK: {
            "description": "List of film reviews retrieved successfully",
        },
    },
)
async def get_film_reviews(
    use_case: Annotated[GetFilmReviewsUseCase, Depends(get_get_film_reviews_use_case)],
    page: int = PAGE_DEFAULT,
    page_size: int = PAGE_SIZE_DEFAULT,
):
    """
    **Get all film reviews with pagination**

    Retrieve all film reviews in the system. Public endpoint, no authentication required.
    """
    logger.debug(f"Retrieving film reviews - page: {page}, page_size: {page_size}")

    reviews, total_items = await use_case.execute(page=page, page_size=page_size)
    total_pages = (total_items + page_size - 1) // page_size if page_size else 1

    return FilmReviewsResponse(
        reviews=[FilmReviewSchemaMappers.to_schema(review) for review in reviews],
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get(
    "/film/{film_id}",
    response_model=FilmReviewsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all reviews for a specific film",
    responses={
        status.HTTP_200_OK: {
            "description": "List of film reviews retrieved successfully",
        },
    },
)
async def get_film_reviews_by_film_id(
    film_id: str,
    use_case: Annotated[
        GetFilmReviewsByFilmIdUseCase, Depends(get_get_film_reviews_by_film_id_use_case)
    ],
    page: int = PAGE_DEFAULT,
    page_size: int = PAGE_SIZE_DEFAULT,
):
    """
    **Get all reviews for a specific film**

    Retrieve all reviews for a given film with pagination. Public endpoint.
    """
    logger.debug(
        f"Retrieving reviews for film {film_id} - page: {page}, page_size: {page_size}"
    )

    reviews, total_items = await use_case.execute(
        film_id=film_id, page=page, page_size=page_size
    )
    total_pages = (total_items + page_size - 1) // page_size if page_size else 1

    return FilmReviewsResponse(
        reviews=[FilmReviewSchemaMappers.to_schema(review) for review in reviews],
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get(
    "/{review_id}",
    response_model=FilmReviewResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a specific film review",
    responses={
        status.HTTP_200_OK: {
            "description": "Film review retrieved successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Film review not found",
        },
    },
)
async def get_film_review(
    review_id: str,
    use_case: Annotated[GetFilmReviewUseCase, Depends(get_get_film_review_use_case)],
):
    """
    **Get a specific film review by ID**

    Retrieve detailed information about a specific review. Public endpoint.
    """
    logger.debug(f"Retrieving film review: {review_id}")

    result = await use_case.execute(review_id=review_id)
    return FilmReviewResponse(review=FilmReviewSchemaMappers.to_schema(result))


@router.patch(
    "/{review_id}",
    response_model=FilmReviewResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a film review",
    responses={
        status.HTTP_200_OK: {
            "description": "Film review updated successfully",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Authentication required",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You can only update your own reviews",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Film review not found",
        },
    },
)
async def update_film_review(
    review_id: str,
    request: FilmReviewUpdateRequest,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    get_use_case: Annotated[
        GetFilmReviewUseCase, Depends(get_get_film_review_use_case)
    ],
    update_use_case: Annotated[
        UpdateFilmReviewUseCase, Depends(get_update_film_review_use_case)
    ],
):
    """
    **Update a film review (Customer only - own reviews)**

    Customers can update their own film reviews. Cannot update reviews created by others.

    ### Request Body:
    - **rating**: New rating from 1 to 5 (optional)
    - **content**: New review text/comment (optional)
    """
    logger.debug(f"User {current_user.user_id} updating film review: {review_id}")

    # Only customers can update reviews
    if current_user.account_type != AccountType.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can update film reviews",
        )

    # Get the existing review to check ownership
    existing_review = await get_use_case.execute(review_id=review_id)

    # Check if the user owns this review
    if existing_review.author_id != current_user.user_id:
        raise UnauthorizedReviewAccessError(current_user.user_id, review_id)

    # Update the review
    result = await update_use_case.execute(
        review_id=review_id,
        rating=request.rating,
        content=request.content,
    )
    logger.info(f"Film review updated successfully: {review_id}")
    return FilmReviewResponse(review=FilmReviewSchemaMappers.to_schema(result))


@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a film review",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Film review deleted successfully",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Authentication required",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Insufficient permissions",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Film review not found",
        },
    },
)
async def delete_film_review(
    review_id: str,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    get_use_case: Annotated[
        GetFilmReviewUseCase, Depends(get_get_film_review_use_case)
    ],
    delete_use_case: Annotated[
        DeleteFilmReviewUseCase, Depends(get_delete_film_review_use_case)
    ],
):
    """
    **Delete a film review**

    - **Customers**: Can delete their own reviews
    - **Administrators**: Can delete any review
    """
    logger.debug(f"User {current_user.user_id} deleting film review: {review_id}")

    # Get the existing review to check ownership
    existing_review = await get_use_case.execute(review_id=review_id)

    # Check permissions
    if current_user.account_type == AccountType.ADMIN:
        # Admins can delete any review
        pass
    elif current_user.account_type == AccountType.CUSTOMER:
        # Customers can only delete their own reviews
        if existing_review.author_id != current_user.user_id:
            raise UnauthorizedReviewAccessError(current_user.user_id, review_id)
    else:
        # Staff cannot delete reviews
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete film reviews",
        )

    await delete_use_case.execute(review_id=review_id)
    logger.info(f"Film review deleted successfully: {review_id}")
