from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config.logging_config import logger
from src.domain.enums.booking_status import BookingStatus
from src.domain.enums.payment_status import PaymentStatus
from src.domain.gateway.payment_gateway import PaymentGateway
from src.domain.repositories.booking_repository import BookingRepository
from src.domain.repositories.booking_seat_repository import BookingSeatRepository
from src.domain.repositories.payment_repository import PaymentRepository


class ProcessVNPayIPNUseCase:
    """
    Use case for processing VNPay IPN (Instant Payment Notification) callback.
    This is called by VNPay server to notify payment status.
    """

    def __init__(
        self,
        payment_gateway: PaymentGateway,
        payment_repository: PaymentRepository,
        booking_repository: BookingRepository,
        booking_seat_repository: BookingSeatRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._payment_gateway = payment_gateway
        self._payment_repository = payment_repository
        self._booking_repository = booking_repository
        self._booking_seat_repository = booking_seat_repository
        self._sessionmaker = sessionmaker

    async def execute(self, params: dict) -> dict:
        """
        Process VNPay IPN callback.

        Args:
            params: Query parameters from VNPay IPN

        Returns:
            dict: Response to send back to VNPay (RspCode and Message)
        """
        logger.info(f"Processing VNPay IPN callback with params: {params}")

        async with self._sessionmaker() as session:
            try:
                # Verify payment signature
                is_valid = self._payment_gateway.verifyPayment(params)

                if not is_valid:
                    logger.error("Invalid VNPay signature in IPN")
                    return {"RspCode": "97", "Message": "Invalid signature"}

                # Extract parameters
                booking_id = params.get("vnp_TxnRef")
                response_code = params.get("vnp_ResponseCode")
                transaction_no = params.get("vnp_TransactionNo")
                amount = (
                    float(params.get("vnp_Amount", 0)) / 100
                )  # VNPay sends amount * 100

                # Get booking
                booking = await self._booking_repository.get_by_id(booking_id, session)
                if not booking:
                    logger.error(f"Booking {booking_id} not found in IPN")
                    return {"RspCode": "01", "Message": "Order not found"}

                # Check if already processed (to handle duplicate IPN)
                if booking.status in [BookingStatus.PAID, BookingStatus.CANCELLED]:
                    logger.info(
                        f"Booking {booking_id} already processed, status: {booking.status}"
                    )
                    return {"RspCode": "00", "Message": "Already processed"}

                # Verify amount matches
                if booking.total_price != amount:
                    logger.error(
                        f"Amount mismatch for booking {booking_id}: expected {booking.total_price}, got {amount}"
                    )
                    return {"RspCode": "04", "Message": "Invalid amount"}

                # Check if payment was successful (response code 00 = success)
                if response_code == "00":
                    # Update booking status to PAID
                    await self._booking_repository.update(
                        booking_id,
                        session,
                        status=BookingStatus.PAID.value,
                        paid_at=datetime.now(),
                        payment_reference=transaction_no,
                    )

                    # Generate ticket codes for all booking seats
                    booking_seats = await self._booking_seat_repository.get_booking_seats_by_booking_id(
                        booking_id, session
                    )
                    current_time = datetime.now()
                    for booking_seat in booking_seats:
                        ticket_code = booking_seat.generate_ticket_code()
                        await self._booking_seat_repository.update(
                            booking_seat.id,
                            session,
                            purchased_at=current_time,
                            ticket_code=ticket_code,
                        )

                    # Get or create payment record
                    payment = await self._payment_repository.get_by_booking_id(
                        booking_id, session
                    )
                    if payment:
                        # Update existing payment
                        await self._payment_repository.update(
                            payment.id,
                            session,
                            status=PaymentStatus.SUCCESS.value,
                            external_txn_id=transaction_no,
                            confirmed_at=datetime.now(),
                            metadata={**payment.metadata, "vnp_ipn_response": params},
                        )
                    else:
                        logger.warning(
                            f"Payment record not found for booking {booking_id} in IPN"
                        )

                    await session.commit()

                    logger.info(f"IPN: Payment successful for booking {booking_id}")
                    return {"RspCode": "00", "Message": "Confirm Success"}
                else:
                    # Payment failed - update booking to CANCELLED
                    await self._booking_repository.update(
                        booking_id, session, status=BookingStatus.CANCELLED.value
                    )

                    # Update payment status to FAILED
                    payment = await self._payment_repository.get_by_booking_id(
                        booking_id, session
                    )
                    if payment:
                        await self._payment_repository.update(
                            payment.id,
                            session,
                            status=PaymentStatus.FAILED.value,
                            metadata={
                                **payment.metadata,
                                "vnp_ipn_response": params,
                                "failure_reason": f"VNPay response code: {response_code}",
                            },
                        )

                    await session.commit()

                    logger.warning(
                        f"IPN: Payment failed for booking {booking_id}, response code: {response_code}"
                    )
                    return {
                        "RspCode": "00",
                        "Message": "Confirm Success",  # Still return success to VNPay as we processed it
                    }

            except Exception as e:
                await session.rollback()
                logger.error(f"Error processing VNPay IPN callback: {e}")
                return {"RspCode": "99", "Message": "Unknown error"}
