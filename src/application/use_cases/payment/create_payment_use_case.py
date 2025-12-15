from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config.logging_config import logger
from src.application.dtos.payment_dtos import PaymentCreateDTO, PaymentResponseDTO
from src.domain.enums.booking_status import BookingStatus
from src.domain.enums.payment_status import PaymentStatus
from src.domain.exceptions.booking_exceptions import BookingNotFoundException
from src.domain.gateway.payment_gateway import PaymentGateway
from src.domain.models.payment import Payment
from src.domain.repositories.booking_repository import BookingRepository
from src.domain.repositories.payment_repository import PaymentRepository


class CreatePaymentUseCase:
    """
    Use case for creating a payment for a booking.
    This creates a payment record and generates a payment URL from the gateway.
    """

    def __init__(
        self,
        payment_repository: PaymentRepository,
        booking_repository: BookingRepository,
        payment_gateway: PaymentGateway,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._payment_repository = payment_repository
        self._booking_repository = booking_repository
        self._payment_gateway = payment_gateway
        self._sessionmaker = sessionmaker

    async def execute(
        self, payment_data: PaymentCreateDTO, idempotency_key: str
    ) -> PaymentResponseDTO:
        """
        Create a payment for a booking and generate payment URL.

        Args:
            payment_data: Payment creation data
            idempotency_key: Idempotency key to store in payment metadata

        Returns:
            PaymentResponseDTO with payment_url generated from gateway

        Raises:
            BookingNotFoundException: If booking doesn't exist
            ValueError: If booking is not in a payable state
        """
        logger.info(
            f"Creating payment for booking {payment_data.booking_id} with method {payment_data.payment_method_id}"
        )

        async with self._sessionmaker() as session:
            try:
                # 1. Validate booking exists and is payable
                booking = await self._booking_repository.get_by_id(
                    payment_data.booking_id, session
                )
                if not booking:
                    raise BookingNotFoundException(identifier=payment_data.booking_id)

                # Check if booking is in a payable state
                if booking.status not in [BookingStatus.CREATED]:
                    raise ValueError(
                        f"Booking {booking.id} is not in a payable state (current status: {booking.status})"
                    )

                # 2. Create payment record with status=pending and store idempotency_key in metadata
                amount = (
                    payment_data.amount if payment_data.amount else booking.total_price
                )
                new_payment = Payment(
                    booking_id=payment_data.booking_id,
                    payment_method_id=payment_data.payment_method_id,
                    amount=amount,
                    status=PaymentStatus.PENDING,
                    metadata={"idempotency_key": idempotency_key},  # Store for tracking
                )
                payment = await self._payment_repository.create(new_payment, session)
                logger.info(
                    f"Created payment record {payment.id} with idempotency_key: {idempotency_key}"
                )

                # Commit the payment record before calling external gateway
                await session.commit()

            except Exception as e:
                await session.rollback()
                logger.error(
                    f"Error creating payment for booking {payment_data.booking_id}: {e}"
                )
                raise

        # 4. Call payment gateway AFTER commit
        try:
            payment_url = self._payment_gateway.createPayment(
                orderId=payment.id,
                amount=payment.amount,
                metadata={
                    "booking_id": payment.booking_id,
                    "payment_method_id": payment.payment_method_id,
                    "orderDes": f"Payment for booking {payment.booking_id}",
                    "ipAddr": payment_data.client_ip,
                },
            )
            logger.info(f"Generated payment URL for payment {payment.id}")

            # 5. Update payment with external_txn_id if needed (in a new session)
            async with self._sessionmaker() as update_session:
                try:
                    await self._payment_repository.update(
                        payment.id,
                        update_session,
                        external_txn_id=payment.id,  # We use order ID as txn ref
                    )
                    await update_session.commit()
                except Exception as e:
                    logger.warning(
                        f"Failed to update payment with external_txn_id: {e}"
                    )
                    # Don't fail the whole operation if this update fails

            # 6. Return payment response with payment_url
            return PaymentResponseDTO(
                id=payment.id,
                booking_id=payment.booking_id,
                payment_method_id=payment.payment_method_id,
                external_txn_id=payment.id,
                amount=payment.amount,
                currency=payment.currency,
                status=payment.status,
                created_at=payment.created_at,
                confirmed_at=payment.confirmed_at,
                payment_url=payment_url,
            )

        except Exception as e:
            logger.error(f"Error generating payment URL for payment {payment.id}: {e}")
            # Mark payment as failed
            async with self._sessionmaker() as fail_session:
                try:
                    await self._payment_repository.update(
                        payment.id,
                        fail_session,
                        status=PaymentStatus.FAILED.value,
                        metadata={
                            "idempotency_key": idempotency_key,
                            "failure_reason": str(e),
                        },
                    )
                    await fail_session.commit()
                except Exception as update_error:
                    logger.error(f"Failed to mark payment as failed: {update_error}")

            raise ValueError(f"Failed to generate payment URL: {str(e)}")
