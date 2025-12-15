from typing import Annotated

from fastapi import APIRouter, status
from fastapi.params import Depends, Query

from config.logging_config import logger
from src.application.use_cases.service.create_service_use_case import (
    CreateServiceUseCase,
)
from src.application.use_cases.service.delete_service_use_case import (
    DeleteServiceUseCase,
)
from src.application.use_cases.service.get_service_use_case import GetServiceUseCase
from src.application.use_cases.service.get_services_use_case import GetServicesUseCase
from src.application.use_cases.service.update_service_use_case import (
    UpdateServiceUseCase,
)
from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.interface.endpoints.dependencies.service_dependencies import (
    get_create_service_use_case,
    get_get_services_use_case,
    get_get_service_use_case,
    get_update_service_use_case,
    get_delete_service_use_case,
)
from src.interface.endpoints.schemas.mappers.service_schema_mappers import (
    ServiceSchemaMappers,
)
from src.interface.endpoints.schemas.service_schemas import (
    ServiceSchema,
    ServiceResponse,
    ServicesResponse,
    ServiceCreateRequest,
    ServiceUpdateRequest,
)

router = APIRouter(prefix="/services", tags=["Services"])


@router.post(
    "/",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new service",
    responses={
        status.HTTP_201_CREATED: {
            "model": ServiceSchema,
            "description": "Service created successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to create a service"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def create_service(
    request: ServiceCreateRequest,
    use_case: Annotated[CreateServiceUseCase, Depends(get_create_service_use_case)],
):
    """Create a new service."""
    logger.debug(f"Received create service request: {request}")
    service_domain = ServiceSchemaMappers.to_domain(request)
    logger.info(f"Creating service: {service_domain.name}")
    result = await use_case.execute(service_domain)
    return ServiceResponse.model_validate({"service": result})


@router.get(
    "/",
    response_model=ServicesResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all services with pagination",
    responses={
        status.HTTP_200_OK: {
            "model": ServicesResponse,
            "description": "List of services retrieved successfully",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def get_services(
    use_case: Annotated[GetServicesUseCase, Depends(get_get_services_use_case)],
    page: int = Query(PAGE_DEFAULT, ge=1, description="Page number (1-based)"),
    page_size: int = Query(
        PAGE_SIZE_DEFAULT, ge=1, le=100, description="Number of items per page"
    ),
):
    """Retrieve all services with pagination."""
    logger.debug(f"Received get services request: page={page}, page_size={page_size}")
    services = await use_case.execute(page=page, page_size=page_size)
    return ServicesResponse.model_validate({"services": services})


@router.get(
    "/{service_id}",
    response_model=ServiceResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a specific service by ID",
    responses={
        status.HTTP_200_OK: {
            "model": ServiceResponse,
            "description": "Service retrieved successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Service not found",
        },
    },
)
async def get_service(
    service_id: str,
    use_case: Annotated[GetServiceUseCase, Depends(get_get_service_use_case)],
):
    """Retrieve a specific service by ID."""
    logger.debug(f"Received get service request for id: {service_id}")
    service = await use_case.execute(service_id)
    return ServiceResponse.model_validate({"service": service})


@router.patch(
    "/{service_id}",
    response_model=ServiceResponse,
    status_code=status.HTTP_200_OK,
    summary="Partially update a service",
    responses={
        status.HTTP_200_OK: {
            "model": ServiceResponse,
            "description": "Service updated successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to update this service"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Service not found",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def update_service(
    service_id: str,
    request: ServiceUpdateRequest,
    use_case: Annotated[UpdateServiceUseCase, Depends(get_update_service_use_case)],
    get_use_case: Annotated[GetServiceUseCase, Depends(get_get_service_use_case)],
):
    """Partially update a service (PATCH)."""
    logger.debug(
        f"Received update service request for id: {service_id}, data: {request}"
    )

    # Get the existing service
    existing_service = await get_use_case.execute(service_id)

    # Update only the fields that were provided in the request
    update_data = request.model_dump(exclude_unset=True)

    # Merge the updates with existing data
    if "name" in update_data:
        existing_service.name = update_data["name"]
    if "detail" in update_data:
        existing_service.detail = update_data["detail"]
    if "price" in update_data:
        existing_service.price = update_data["price"]

    logger.info(
        f"Updating service: {service_id} with fields: {list(update_data.keys())}"
    )
    result = await use_case.execute(existing_service)
    return ServiceResponse.model_validate({"service": result})


@router.delete(
    "/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a service",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Service deleted successfully"},
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to delete a service"
        },
        status.HTTP_404_NOT_FOUND: {"description": "Service not found"},
    },
)
async def delete_service(
    service_id: str,
    use_case: Annotated[DeleteServiceUseCase, Depends(get_delete_service_use_case)],
):
    """Delete a service."""
    logger.debug(f"Received delete service request for id: {service_id}")
    logger.info(f"Deleting service: {service_id}")
    await use_case.execute(service_id)
