from typing import Annotated

from fastapi import APIRouter, status
from fastapi.params import Depends

from config.logging_config import logger
from src.application.use_cases.banner.create_banner_use_case import (
    CreateBannerUseCase,
)
from src.application.use_cases.banner.delete_banner_use_case import (
    DeleteBannerUseCase,
)
from src.application.use_cases.banner.get_active_banners_use_case import (
    GetActiveBannersUseCase,
)
from src.application.use_cases.banner.get_banner_use_case import GetBannerUseCase
from src.application.use_cases.banner.update_banner_use_case import (
    UpdateBannerUseCase,
)
from src.domain.exceptions.banner_exceptions import BannerNotFoundException
from src.interface.endpoints.dependencies.banner_dependencies import (
    get_active_banners_use_case,
    get_create_banner_use_case,
    get_banner_use_case,
    get_update_banner_use_case,
    get_delete_banner_use_case,
)
from src.interface.endpoints.schemas.banner_schemas import (
    BannersListResponse,
    BannerResponse,
    BannerCreateRequest,
    BannerUpdateRequest,
)
from src.interface.endpoints.schemas.mappers.banner_schema_mappers import (
    BannerSchemaMappers,
)

router = APIRouter(prefix="/banners", tags=["Banners"])


@router.get(
    "/",
    response_model=BannersListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get active banners for hero section",
    responses={
        status.HTTP_200_OK: {
            "model": BannersListResponse,
            "description": "Successfully retrieved active banners",
        },
    },
)
async def get_active_banners(
    use_case: Annotated[GetActiveBannersUseCase, Depends(get_active_banners_use_case)],
) -> BannersListResponse:
    """
    Retrieve all active banners for the hero section.

    Returns banners that are currently active (based on start_at and end_at times)
    ordered by priority in descending order.

    Returns:
        BannersListResponse: List of active banners
    """
    banners = await use_case.execute()
    banner_schemas = [BannerSchemaMappers.to_schema(banner) for banner in banners]

    return BannersListResponse(banners=banner_schemas)


@router.post(
    "/",
    response_model=BannerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new banner",
    responses={
        status.HTTP_201_CREATED: {
            "model": BannerResponse,
            "description": "Banner created successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to create a banner"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def create_banner(
    request: BannerCreateRequest,
    use_case: Annotated[CreateBannerUseCase, Depends(get_create_banner_use_case)],
) -> BannerResponse:
    """
    Create a new banner for the hero section.

    This endpoint allows the creation of a new banner with all necessary details
    including images, CTA, target information, and scheduling.

    Args:
        request: The banner details to create
        use_case: The use case instance with injected repository dependencies

    Returns:
        BannerResponse: The created banner details
    """
    logger.debug(f"Received create banner request: {request}")

    banner_domain = BannerSchemaMappers.to_domain(request)
    created_banner = await use_case.execute(banner_domain)

    banner_schema = BannerSchemaMappers.to_schema(created_banner)
    logger.info(f"Created banner with ID: {created_banner.id}")

    return BannerResponse(banner=banner_schema)


@router.get(
    "/{banner_id}",
    response_model=BannerResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a banner by its ID",
    responses={
        status.HTTP_200_OK: {
            "model": BannerResponse,
            "description": "Successfully retrieved banner",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Banner not found with the provided ID"
        },
    },
)
async def get_banner(
    banner_id: str,
    use_case: Annotated[GetBannerUseCase, Depends(get_banner_use_case)],
) -> BannerResponse:
    """
    Retrieve a banner by its ID.

    Args:
        banner_id: The ID of the banner to retrieve
        use_case: The use case instance with injected repository dependencies

    Returns:
        BannerResponse: The details of the retrieved banner
    """
    logger.debug(f"Received get banner by ID request: banner_id={banner_id}")

    banner = await use_case.execute(banner_id)
    if not banner:
        logger.warning(f"Banner with ID {banner_id} not found")
        raise BannerNotFoundException(banner_id=banner_id)

    logger.info(f"Retrieved banner: {banner.title} (ID: {banner.id})")

    banner_schema = BannerSchemaMappers.to_schema(banner)
    return BannerResponse(banner=banner_schema)


@router.patch(
    "/{banner_id}",
    response_model=BannerResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing banner",
    responses={
        status.HTTP_200_OK: {
            "model": BannerResponse,
            "description": "Banner updated successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Banner not found with the provided ID"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to update this banner"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def update_banner(
    banner_id: str,
    request: BannerUpdateRequest,
    use_case: Annotated[UpdateBannerUseCase, Depends(get_update_banner_use_case)],
) -> BannerResponse:
    """
    Update an existing banner.

    This endpoint allows updating the details of an existing banner. Only the fields
    provided in the request will be updated.

    Args:
        banner_id: The ID of the banner to update
        request: The updated banner details
        use_case: The use case instance with injected repository dependencies

    Returns:
        BannerResponse: The updated banner details
    """
    logger.debug(
        f"Received update banner request: banner_id={banner_id}, request={request}"
    )

    try:
        updated_banner = await use_case.execute(
            banner_id, **request.model_dump(exclude_unset=True)
        )
        banner_schema = BannerSchemaMappers.to_schema(updated_banner)
        logger.info(f"Updated banner with ID: {banner_id}")
        return BannerResponse(banner=banner_schema)
    except ValueError as e:
        logger.warning(f"Banner with ID {banner_id} not found")
        raise BannerNotFoundException(banner_id=banner_id)


@router.delete(
    "/{banner_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a banner by its ID",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Banner deleted successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Banner not found with the provided ID"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to delete this banner"
        },
    },
)
async def delete_banner(
    banner_id: str,
    use_case: Annotated[DeleteBannerUseCase, Depends(get_delete_banner_use_case)],
) -> None:
    """
    Delete a banner by its ID.

    This endpoint deletes a banner based on the provided banner ID.

    Args:
        banner_id: The ID of the banner to delete
        use_case: The use case instance with injected repository dependencies

    Returns:
        None
    """
    logger.debug(f"Received delete banner request: banner_id={banner_id}")

    try:
        await use_case.execute(banner_id)
        logger.info(f"Deleted banner with ID: {banner_id}")
    except ValueError as e:
        logger.warning(f"Banner with ID {banner_id} not found")
        raise BannerNotFoundException(banner_id=banner_id)
