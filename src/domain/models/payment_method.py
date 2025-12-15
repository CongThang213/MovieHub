from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class PaymentMethod:
    """
    Represents a payment method that can be used for transactions.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    active: bool = True
    surcharge: float = 0.0

    def calculate_surcharge(self, base_amount: float) -> float:
        """
        Calculate the surcharge amount for this payment method.

        Args:
            base_amount: The base amount before surcharge

        Returns:
            float: The surcharge amount
        """
        return base_amount * (self.surcharge / 100)

    def is_available(self) -> bool:
        """
        Check if this payment method is currently available for use.

        Returns:
            bool: True if available, False otherwise
        """
        return self.active
