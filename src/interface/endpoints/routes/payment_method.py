from typing import Annotated

from fastapi import APIRouter, status
from fastapi.params import Depends, Query

from config.logging_config import logger
from src.application.use_cases.payment_method.create_payment_method_use_case import (
    CreatePaymentMethodUseCase,
)
from src.application.use_cases.payment_method.delete_payment_method_use_case import (
    DeletePaymentMethodUseCase,
)
from src.application.use_cases.payment_method.get_active_payment_methods_use_case import (
    GetActivePaymentMethodsUseCase,
)
from src.application.use_cases.payment_method.get_payment_method_use_case import (
    GetPaymentMethodUseCase,
)
from src.application.use_cases.payment_method.get_payment_methods_use_case import (
    GetPaymentMethodsUseCase,
)
from src.application.use_cases.payment_method.update_payment_method_use_case import (
    UpdatePaymentMethodUseCase,
)
from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.interface.endpoints.dependencies.payment_method_dependencies import (
    get_create_payment_method_use_case,
    get_payment_method_use_case,
    get_payment_methods_use_case,
    get_active_payment_methods_use_case,
    get_update_payment_method_use_case,
    get_delete_payment_method_use_case,
)
from src.interface.endpoints.schemas.mappers.payment_method_schema_mappers import (
    PaymentMethodSchemaMappers,
)
from src.interface.endpoints.schemas.payment_method_schemas import (
    PaymentMethodSchema,
    PaymentMethodResponse,
    PaymentMethodsResponse,
    PaymentMethodCreateRequest,
    PaymentMethodUpdateRequest,
)

router = APIRouter(prefix="/payment-methods", tags=["Payment Methods"])


@router.post(
    "/",
    response_model=PaymentMethodResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new payment method",
    responses={
        status.HTTP_201_CREATED: {
            "model": PaymentMethodSchema,
            "description": "Payment method created successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to create a payment method"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def create_payment_method(
    request: PaymentMethodCreateRequest,
    use_case: Annotated[
        CreatePaymentMethodUseCase, Depends(get_create_payment_method_use_case)
    ],
):
    """Create a new payment method."""
    logger.debug(f"Received create payment method request: {request}")
    payment_method_domain = PaymentMethodSchemaMappers.to_domain(request)
    logger.info(f"Creating payment method: {payment_method_domain.name}")
    result = await use_case.execute(payment_method_domain)
    return PaymentMethodResponse.model_validate({"payment_method": result})


@router.get(
    "/",
    response_model=PaymentMethodsResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all payment methods with pagination",
    responses={
        status.HTTP_200_OK: {
            "model": PaymentMethodsResponse,
            "description": "List of payment methods retrieved successfully",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def get_payment_methods(
    page: int = Query(default=PAGE_DEFAULT, ge=1, description="Page number"),
    page_size: int = Query(
        default=PAGE_SIZE_DEFAULT, ge=1, le=100, description="Page size"
    ),
    use_case: Annotated[
        GetPaymentMethodsUseCase, Depends(get_payment_methods_use_case)
    ] = None,
):
    """Retrieve all payment methods with pagination."""
    logger.info(f"Retrieving payment methods - page: {page}, page_size: {page_size}")
    payment_methods = await use_case.execute(page, page_size)
    payment_method_schemas = PaymentMethodSchemaMappers.from_domains(payment_methods)
    return PaymentMethodsResponse(payment_methods=payment_method_schemas)


@router.get(
    "/active",
    response_model=PaymentMethodsResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all active payment methods",
    responses={
        status.HTTP_200_OK: {
            "model": PaymentMethodsResponse,
            "description": "List of active payment methods retrieved successfully",
        },
    },
)
async def get_active_payment_methods(
    use_case: Annotated[
        GetActivePaymentMethodsUseCase, Depends(get_active_payment_methods_use_case)
    ],
):
    """Retrieve all active payment methods."""
    logger.info("Retrieving active payment methods")
    payment_methods = await use_case.execute()
    payment_method_schemas = PaymentMethodSchemaMappers.from_domains(payment_methods)
    return PaymentMethodsResponse(payment_methods=payment_method_schemas)


@router.get(
    "/{payment_method_id}",
    response_model=PaymentMethodResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a payment method by ID",
    responses={
        status.HTTP_200_OK: {
            "model": PaymentMethodResponse,
            "description": "Payment method retrieved successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Payment method not found with the specified ID"
        },
    },
)
async def get_payment_method(
    payment_method_id: str,
    use_case: Annotated[GetPaymentMethodUseCase, Depends(get_payment_method_use_case)],
):
    """Retrieve a payment method by its ID."""
    logger.info(f"Retrieving payment method with ID: {payment_method_id}")
    payment_method = await use_case.execute(payment_method_id)
    return PaymentMethodResponse.model_validate({"payment_method": payment_method})


@router.patch(
    "/{payment_method_id}",
    response_model=PaymentMethodResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a payment method by ID",
    responses={
        status.HTTP_200_OK: {
            "model": PaymentMethodResponse,
            "description": "Payment method updated successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Payment method not found with the specified ID"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to update this payment method"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def update_payment_method(
    payment_method_id: str,
    request: PaymentMethodUpdateRequest,
    use_case: Annotated[
        UpdatePaymentMethodUseCase, Depends(get_update_payment_method_use_case)
    ],
    get_use_case: Annotated[
        GetPaymentMethodUseCase, Depends(get_payment_method_use_case)
    ],
):
    """Update a payment method by its ID."""
    logger.debug(
        f"Received update request for payment method ID {payment_method_id}: {request}"
    )

    # Get existing payment method
    existing_payment_method = await get_use_case.execute(payment_method_id)

    # Update only provided fields
    if request.name is not None:
        existing_payment_method.name = request.name
    if request.active is not None:
        existing_payment_method.active = request.active
    if request.surcharge is not None:
        existing_payment_method.surcharge = request.surcharge

    logger.info(f"Updating payment method: {payment_method_id}")
    result = await use_case.execute(existing_payment_method)
    return PaymentMethodResponse.model_validate({"payment_method": result})


@router.delete(
    "/{payment_method_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a payment method by ID",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Payment method deleted successfully"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Payment method not found with the specified ID"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to delete this payment method"
        },
    },
)
async def delete_payment_method(
    payment_method_id: str,
    use_case: Annotated[
        DeletePaymentMethodUseCase, Depends(get_delete_payment_method_use_case)
    ],
):
    """Delete a payment method by its ID."""
    logger.info(f"Deleting payment method with ID: {payment_method_id}")
    await use_case.execute(payment_method_id)
    return None
