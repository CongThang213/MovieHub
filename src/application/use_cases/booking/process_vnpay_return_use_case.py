from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config.logging_config import logger
from src.domain.gateway.payment_gateway import PaymentGateway
from src.domain.repositories.booking_repository import BookingRepository


class ProcessVNPayReturnUseCase:
    """
    Use case for processing VNPay return callback.
    """

    def __init__(
        self,
        payment_gateway: PaymentGateway,
        booking_repository: BookingRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._payment_gateway = payment_gateway
        self._booking_repository = booking_repository
        self._sessionmaker = sessionmaker

    async def execute(self, params: dict) -> dict:
        """
        Process VNPay return callback.
        Note: This only verifies and returns status to user.

        Args:
            params: Query parameters from VNPay return URL

        Returns:
            dict: Result with status and message for user display
        """
        logger.info(f"Processing VNPay return callback with params: {params}")

        try:
            # Verify payment signature
            is_valid = self._payment_gateway.verifyPayment(params)

            if not is_valid:
                logger.error("Invalid VNPay signature")
                return {
                    "success": False,
                    "message": "Invalid payment signature",
                    "code": "INVALID_SIGNATURE",
                }

            # Extract parameters
            booking_id = params.get("vnp_TxnRef")
            response_code = params.get("vnp_ResponseCode")
            transaction_no = params.get("vnp_TransactionNo")

            # Check if payment was successful (response code 00 = success)
            if response_code == "00":
                logger.info(f"Payment successful for booking {booking_id}")
                return {
                    "success": True,
                    "message": "Payment successful. Your booking is being processed.",
                    "code": "SUCCESS",
                    "booking_id": booking_id,
                    "transaction_no": transaction_no,
                }
            else:
                logger.warning(
                    f"Payment failed for booking {booking_id}, response code: {response_code}"
                )
                return {
                    "success": False,
                    "message": "Payment failed",
                    "code": f"PAYMENT_FAILED_{response_code}",
                    "booking_id": booking_id,
                }

        except Exception as e:
            logger.error(f"Error processing VNPay return callback: {e}")
            return {
                "success": False,
                "message": "Error processing payment",
                "code": "PROCESSING_ERROR",
            }
