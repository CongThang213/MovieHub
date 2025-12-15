from typing import Annotated

from fastapi import APIRouter, Request, status
from fastapi.params import Depends

from config.logging_config import logger
from src.application.use_cases.voucher.create_voucher_use_case import (
    CreateVoucherUseCase,
)
from src.application.use_cases.voucher.delete_voucher_use_case import (
    DeleteVoucherUseCase,
)
from src.application.use_cases.voucher.get_voucher_by_code_use_case import (
    GetVoucherByCodeUseCase,
)
from src.application.use_cases.voucher.get_voucher_use_case import GetVoucherUseCase
from src.application.use_cases.voucher.get_vouchers_use_case import GetVouchersUseCase
from src.application.use_cases.voucher.update_voucher_use_case import (
    UpdateVoucherUseCase,
)
from src.application.use_cases.voucher.validate_voucher_use_case import (
    ValidateVoucherUseCase,
)
from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.enums.account_type import AccountType
from src.domain.exceptions.voucher_exceptions import (
    VoucherNotFoundException,
    VoucherCodeNotFoundException,
)
from src.interface.endpoints.dependencies.voucher_dependencies import (
    get_create_voucher_use_case,
    get_get_vouchers_use_case,
    get_get_voucher_use_case,
    get_get_voucher_by_code_use_case,
    get_update_voucher_use_case,
    get_delete_voucher_use_case,
    get_validate_voucher_use_case,
)
from src.interface.endpoints.schemas.mappers.voucher_schema_mappers import (
    VoucherSchemaMappers,
)
from src.interface.endpoints.schemas.voucher_schemas import (
    VoucherSchema,
    VoucherResponse,
    VouchersResponse,
    VoucherCreateRequest,
    VoucherUpdateRequest,
    VoucherValidateRequest,
    VoucherValidateResponse,
)

router = APIRouter(prefix="/vouchers", tags=["Vouchers"])


@router.post(
    "/",
    response_model=VoucherResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new voucher",
    responses={
        status.HTTP_201_CREATED: {
            "model": VoucherSchema,
            "description": "Voucher created successfully",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Voucher with the same code already exists"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to create a voucher"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def create_voucher(
    request: VoucherCreateRequest,
    use_case: Annotated[CreateVoucherUseCase, Depends(get_create_voucher_use_case)],
):
    """Create a new voucher."""
    logger.debug(f"Received create voucher request: {request}")
    voucher_domain = VoucherSchemaMappers.to_domain(request)
    logger.info(f"Creating voucher: {voucher_domain.code}")
    result = await use_case.execute(voucher_domain)
    return VoucherResponse.model_validate({"voucher": result})


@router.get(
    "/",
    response_model=VouchersResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all vouchers with pagination",
    responses={
        status.HTTP_200_OK: {
            "model": VouchersResponse,
            "description": "List of vouchers retrieved successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to view vouchers"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def get_vouchers(
    request: Request,
    page: int = PAGE_DEFAULT,
    page_size: int = PAGE_SIZE_DEFAULT,
    use_case: GetVouchersUseCase = Depends(get_get_vouchers_use_case),
) -> VouchersResponse:
    """Retrieve all vouchers with pagination. Customers see only valid vouchers, admins see all."""
    logger.debug(f"Received get vouchers request: page={page}, page_size={page_size}")
    vouchers = await use_case.execute(page, page_size)

    # Filter vouchers based on user role
    account_type = getattr(request.state, "account_type", AccountType.CUSTOMER)
    if account_type == AccountType.CUSTOMER:
        # Customers only see valid vouchers
        vouchers = [v for v in vouchers if v.is_valid()]
        logger.info(f"Retrieved {len(vouchers)} valid vouchers for customer")
    else:
        logger.info(f"Retrieved {len(vouchers)} vouchers for {account_type.value}")

    voucher_schemas = VoucherSchemaMappers.from_domains(vouchers)
    return VouchersResponse.model_validate({"vouchers": voucher_schemas})


@router.get(
    "/code/{code}",
    response_model=VoucherResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a voucher by its code",
    responses={
        status.HTTP_200_OK: {
            "model": VoucherResponse,
            "description": "Voucher retrieved successfully by code",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Voucher not found with the provided code"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to view this voucher"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def get_voucher_by_code(
    code: str,
    use_case: Annotated[
        GetVoucherByCodeUseCase, Depends(get_get_voucher_by_code_use_case)
    ],
) -> VoucherResponse:
    """Retrieve a voucher by its code."""
    logger.debug(f"Received get voucher by code request: code={code}")
    voucher = await use_case.execute(code)
    if not voucher:
        logger.warning(f"Voucher with code {code} not found")
        raise VoucherCodeNotFoundException(code=code)
    logger.info(f"Retrieved voucher: {voucher.code} (ID: {voucher.id})")
    voucher_schema = VoucherSchemaMappers.from_domain(voucher)
    return VoucherResponse.model_validate({"voucher": voucher_schema})


@router.get(
    "/{voucher_id}",
    response_model=VoucherResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a voucher by its ID",
    responses={
        status.HTTP_200_OK: {
            "model": VoucherResponse,
            "description": "Voucher retrieved successfully by ID",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Voucher not found with the provided ID"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to view this voucher"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def get_voucher_by_id(
    voucher_id: str,
    use_case: Annotated[GetVoucherUseCase, Depends(get_get_voucher_use_case)],
) -> VoucherResponse:
    """Retrieve a voucher by its ID."""
    logger.debug(f"Received get voucher by ID request: voucher_id={voucher_id}")
    voucher = await use_case.execute(voucher_id)
    if not voucher:
        logger.warning(f"Voucher with ID {voucher_id} not found")
        raise VoucherNotFoundException(voucher_id=voucher_id)
    logger.info(f"Retrieved voucher: {voucher.code} (ID: {voucher.id})")
    voucher_schema = VoucherSchemaMappers.from_domain(voucher)
    return VoucherResponse.model_validate({"voucher": voucher_schema})


@router.patch(
    "/{voucher_id}",
    response_model=VoucherResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing voucher",
    responses={
        status.HTTP_200_OK: {
            "model": VoucherResponse,
            "description": "Voucher updated successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Voucher not found with the provided ID"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to update this voucher"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def update_voucher(
    voucher_id: str,
    request: VoucherUpdateRequest,
    use_case: Annotated[UpdateVoucherUseCase, Depends(get_update_voucher_use_case)],
) -> VoucherResponse:
    """Update an existing voucher."""
    logger.debug(f"Received update voucher request for ID {voucher_id}: {request}")
    update_data = request.model_dump(exclude_unset=True)
    result = await use_case.execute(voucher_id, update_data)
    logger.info(f"Updated voucher with ID: {voucher_id}")
    voucher_schema = VoucherSchemaMappers.from_domain(result)
    return VoucherResponse.model_validate({"voucher": voucher_schema})


@router.delete(
    "/{voucher_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a voucher",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Voucher deleted successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Voucher not found with the provided ID"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to delete this voucher"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def delete_voucher(
    voucher_id: str,
    use_case: Annotated[DeleteVoucherUseCase, Depends(get_delete_voucher_use_case)],
):
    """Delete a voucher."""
    logger.debug(f"Received delete voucher request: voucher_id={voucher_id}")
    result = await use_case.execute(voucher_id)
    if not result:
        logger.warning(f"Voucher with ID {voucher_id} not found")
        raise VoucherNotFoundException(voucher_id=voucher_id)
    logger.info(f"Deleted voucher with ID: {voucher_id}")


@router.post(
    "/validate",
    response_model=VoucherValidateResponse,
    status_code=status.HTTP_200_OK,
    summary="Validate a voucher by code",
    responses={
        status.HTTP_200_OK: {
            "model": VoucherValidateResponse,
            "description": "Voucher validated successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Voucher not found with the provided code"
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Voucher is invalid (expired, used up, etc.)"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the input data provided"
        },
    },
)
async def validate_voucher(
    request: VoucherValidateRequest,
    use_case: Annotated[ValidateVoucherUseCase, Depends(get_validate_voucher_use_case)],
) -> VoucherValidateResponse:
    """Validate a voucher by code."""
    logger.debug(f"Received validate voucher request: code={request.code}")
    result = await use_case.execute(request.code)
    logger.info(f"Validated voucher: {request.code}")
    return VoucherValidateResponse.model_validate(result)
