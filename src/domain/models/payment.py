from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import uuid4

from src.domain.enums.payment_status import PaymentStatus


@dataclass
class Payment:
    """
    Represents a payment transaction for a booking.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    booking_id: Optional[str] = None
    payment_method_id: Optional[str] = None
    external_txn_id: Optional[str] = None
    amount: float = 0.0
    currency: str = "VND"
    status: PaymentStatus = PaymentStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    confirmed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def confirm_payment(self, external_txn_id: str = None) -> None:
        """
        Confirm a successful payment transaction.

        Args:
            external_txn_id: Optional external transaction ID from payment provider
        """
        self.status = PaymentStatus.COMPLETED
        self.confirmed_at = datetime.now()
        if external_txn_id:
            self.external_txn_id = external_txn_id

    def fail_payment(self, reason: str = None) -> None:
        """
        Mark payment as failed with an optional reason.

        Args:
            reason: The reason for payment failure
        """
        self.status = PaymentStatus.FAILED
        if reason:
            self.metadata["failure_reason"] = reason

    def refund_payment(self, reason: str = None) -> None:
        """
        Mark payment as refunded with an optional reason.

        Args:
            reason: The reason for the refund
        """
        self.status = PaymentStatus.REFUNDED
        if reason:
            self.metadata["refund_reason"] = reason

    def is_completed(self) -> bool:
        """
        Check if the payment has been completed successfully.

        Returns:
            bool: True if completed, False otherwise
        """
        return self.status == PaymentStatus.COMPLETED
