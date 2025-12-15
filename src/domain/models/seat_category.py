from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4


@dataclass
class SeatCategory:
    """
    Represents a category of seats with specific pricing and attributes.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    base_price: float = 0.0
    attributes: Optional[str] = None

    def calculate_price_with_surcharge(
        self, surcharge_percentage: float = 0.0
    ) -> float:
        """
        Calculate the total price including a surcharge.

        Args:
            surcharge_percentage: The surcharge percentage to apply

        Returns:
            float: The total price with surcharge
        """
        surcharge = self.base_price * (surcharge_percentage / 100)
        return self.base_price + surcharge
