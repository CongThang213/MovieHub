from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4


@dataclass
class Service:
    """
    Represents an additional service that can be offered to cinema customers.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    detail: str = ""
    image_url: Optional[str] = None
    price: float = 0.0
    is_available: bool = True

    def calculate_total_price(self, quantity: int = 1) -> float:
        """
        Calculate the total price for multiple quantities of this service.

        Args:
            quantity: The number of service items

        Returns:
            float: The total price
        """
        return self.price * max(1, quantity)

    def has_details(self) -> bool:
        """
        Check if this service has detailed information.

        Returns:
            bool: True if service has details, False otherwise
        """
        return bool(self.detail and len(self.detail) > 10)
