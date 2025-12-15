from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, Header, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from config.logging_config import logger
from src.application.dtos.payment_dtos import PaymentCreateDTO
from src.application.use_cases.booking.process_vnpay_ipn_use_case import (
    ProcessVNPayIPNUseCase,
)
from src.application.use_cases.booking.process_vnpay_return_use_case import (
    ProcessVNPayReturnUseCase,
)
from src.application.use_cases.payment.create_payment_use_case import (
    CreatePaymentUseCase,
)
from src.containers import AppContainer
from src.domain.gateway.payment_gateway import PaymentGateway
from src.domain.repositories.payment_repository import PaymentRepository
from src.interface.endpoints.schemas.payment_schemas import (
    CreatePaymentRequest,
    PaymentResponse,
)

router = APIRouter(prefix="/payment", tags=["Payment"])


def get_client_ip(request: Request) -> str:
    """
    Extract the real client IP address from request headers, accounting for common proxy and load balancer setups.

    The function checks headers in the following order of priority to determine the most accurate client IP:

    1\. X-Forwarded-For: Used by proxies/load balancers

    2\. X-Real-IP: Commonly set by nginx or similar reverse proxies to indicate the real client IP.

    3\. request.client.host: The direct connection IP, used as a fallback if no proxy headers are present.

    Args:
        request (fastapi.Request): The incoming FastAPI request object.

    Returns:
        str: The best-effort client IP address as a string.
    """
    # Check X-Forwarded-For header (used by proxies/load balancers)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # X-Forwarded-For can contain multiple IPs, first one is the client
        return forwarded_for.split(",")[0].strip()

    # Check X-Real-IP header (used by nginx)
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()

    # Fallback to direct client host
    if request.client and request.client.host:
        return request.client.host

    # Fallback to loopback
    return "127.0.0.1"


@router.post(
    "/bookings/{booking_id}/payments",
    status_code=status.HTTP_201_CREATED,
    response_model=PaymentResponse,
    summary="Create payment for a booking",
    description="Create a payment record and generate payment URL for a booking. Requires Idempotency-Key header.",
)
@inject
async def create_payment_for_booking(
    request: Request,
    booking_id: str,
    payment_request: CreatePaymentRequest,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    create_payment_use_case: CreatePaymentUseCase = Depends(
        Provide[AppContainer.use_cases.create_payment_use_case]
    ),
    payment_repository: PaymentRepository = Depends(
        Provide[AppContainer.repositories.payment_repository]
    ),
    payment_gateway: PaymentGateway = Depends(
        Provide[AppContainer.payment_gateway.vnpay_gateway]
    ),
    sessionmaker: async_sessionmaker[AsyncSession] = Depends(
        Provide[AppContainer.database_settings.sessionmaker]
    ),
):
    """
        Create a payment for a booking and return the payment URL.

    This endpoint implements idempotency at the HTTP layer to prevent duplicate payments:

    1\. Checks for an existing pending payment for the given booking and payment method with the same idempotency key.

    2\. If such a payment exists, it regenerates the payment URL and returns the existing payment details.

    3\. If no such payment exists, it creates a new payment record and generates a new payment URL.

        **Idempotency-Key Header**:
        - Required: Yes (UUID format recommended)
        - Purpose: Ensures that repeated requests (e.g., due to network retries) do not result in duplicate payments.

        Returns:
            PaymentResponse: Details of the created or existing payment, including a payment URL for the user to complete the transaction.
    """
    # Extract real client IP from request headers
    client_ip = get_client_ip(request)
    logger.debug(f"Client IP extracted: {client_ip}")

    # Check for existing payment with this idempotency key
    async with sessionmaker() as session:
        existing_payment = await payment_repository.get_pending_by_booking_and_method(
            booking_id,
            payment_request.payment_method_id,
            session,
        )

        if existing_payment:
            existing_key = existing_payment.metadata.get("idempotency_key")
            if existing_key == idempotency_key:
                logger.info(
                    f"Idempotency hit: Returning existing payment {existing_payment.id} "
                    f"for idempotency_key {idempotency_key}"
                )

                # Regenerate payment URL from gateway with real client IP
                payment_url = payment_gateway.createPayment(
                    orderId=existing_payment.id,
                    amount=existing_payment.amount,
                    metadata={
                        "booking_id": existing_payment.booking_id,
                        "payment_method_id": existing_payment.payment_method_id,
                        "orderDes": f"Payment for booking {existing_payment.booking_id}",
                        "ipAddr": client_ip,
                    },
                )

                return PaymentResponse(
                    id=existing_payment.id,
                    booking_id=existing_payment.booking_id,
                    payment_method_id=existing_payment.payment_method_id,
                    external_txn_id=existing_payment.external_txn_id,
                    amount=existing_payment.amount,
                    currency=existing_payment.currency,
                    status=existing_payment.status,
                    created_at=existing_payment.created_at,
                    confirmed_at=existing_payment.confirmed_at,
                    payment_url=payment_url,
                )

    # Create new payment via use case
    payment_data = PaymentCreateDTO(
        booking_id=booking_id,
        payment_method_id=payment_request.payment_method_id,
        client_ip=client_ip,
    )

    result = await create_payment_use_case.execute(payment_data, idempotency_key)

    return PaymentResponse(
        id=result.id,
        booking_id=result.booking_id,
        payment_method_id=result.payment_method_id,
        external_txn_id=result.external_txn_id,
        amount=result.amount,
        currency=result.currency,
        status=result.status,
        created_at=result.created_at,
        confirmed_at=result.confirmed_at,
        payment_url=result.payment_url,
    )


@router.get(
    "/payments/{payment_id}",
    status_code=status.HTTP_200_OK,
    response_model=PaymentResponse,
    summary="Get payment by ID",
    description="Retrieve payment details by payment ID",
)
@inject
async def get_payment(
    payment_id: str,
    payment_repository: PaymentRepository = Depends(
        Provide[AppContainer.repositories.payment_repository]
    ),
    sessionmaker: async_sessionmaker[AsyncSession] = Depends(
        Provide[AppContainer.database_settings.sessionmaker]
    ),
):
    """
    Get payment details by payment ID.

    Note: payment_url is not persisted and will be None in this response.
    To get a new payment URL, use the create payment endpoint.
    """
    async with sessionmaker() as session:
        payment = await payment_repository.get_by_id(payment_id, session)

        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payment with ID {payment_id} not found",
            )

        return PaymentResponse(
            id=payment.id,
            booking_id=payment.booking_id,
            payment_method_id=payment.payment_method_id,
            external_txn_id=payment.external_txn_id,
            amount=payment.amount,
            currency=payment.currency,
            status=payment.status,
            created_at=payment.created_at,
            confirmed_at=payment.confirmed_at,
            payment_url=None,  # Not persisted
        )


@router.get(
    "/vnpay/return",
    status_code=status.HTTP_200_OK,
    summary="VNPay payment return callback",
    description="Handles the return callback from VNPay after customer completes payment",
)
@inject
async def vnpay_return(
    request: Request,
    process_vnpay_return_use_case: ProcessVNPayReturnUseCase = Depends(
        Provide[AppContainer.use_cases.process_vnpay_return_use_case]
    ),
):
    """
    Handle VNPay return callback.
    This endpoint is called when the user is redirected back from VNPay payment page.
    """
    params = dict(request.query_params)
    result = await process_vnpay_return_use_case.execute(params)

    if result["success"]:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": result["message"],
                "data": {
                    "booking_id": result.get("booking_id"),
                    "transaction_no": result.get("transaction_no"),
                },
            },
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "message": result["message"],
                "code": result.get("code"),
            },
        )


@router.get(
    "/IPN",
    status_code=status.HTTP_200_OK,
    summary="VNPay IPN (Instant Payment Notification) callback",
    description="Handles the IPN callback from VNPay server to confirm payment status",
)
@inject
async def vnpay_ipn(
    request: Request,
    process_vnpay_ipn_use_case: ProcessVNPayIPNUseCase = Depends(
        Provide[AppContainer.use_cases.process_vnpay_ipn_use_case]
    ),
):
    """
    Handle VNPay IPN (Instant Payment Notification) callback.

    This endpoint is called by the VNPay server to notify the system about the payment status of a transaction.
    It is used for server-to-server communication to ensure payment status is reliably updated, even if the user
    does not return to the site.

    Full URL: https://{domain}/payment/IPN
    VNPay will send GET request with query parameters to this endpoint.

    The response must follow VNPay's required format, typically including fields like `RspCode` and `Message`
    to indicate processing results.
    """
    params = dict(request.query_params)
    result = await process_vnpay_ipn_use_case.execute(params)

    # VNPay expects a JSON response with RspCode and Message
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
