from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class Voucher:
    """
    Represents a discount voucher that can be applied to bookings.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    code: str = ""
    discount_rate: float = 0.0
    valid_from: datetime = field(default_factory=datetime.now)
    valid_until: Optional[datetime] = None
    max_usage: int = 1
    used_count: int = 0

    def is_valid(self) -> bool:
        """
        Check if the voucher is currently valid.

        Returns:
            bool: True if the voucher is valid, False otherwise
        """
        now = datetime.now()

        if now < self.valid_from:
            return False

        if self.valid_until and now > self.valid_until:
            return False

        if self.used_count >= self.max_usage:
            return False

        return True

    def apply_discount(self, amount: float) -> float:
        """
        Calculate the discounted amount after applying this voucher.

        Args:
            amount: The original amount to discount

        Returns:
            float: The discounted amount, or original amount if voucher is invalid
        """
        if not self.is_valid():
            return amount

        discount = amount * (self.discount_rate / 100)

        # Ensure we don't return negative amounts
        return max(0, amount - discount)

    def use(self) -> bool:
        """
        Mark voucher as used once. Increments used_count if not at max usage.

        Returns:
            bool: True if the voucher was successfully used, False otherwise
        """
        if self.used_count < self.max_usage:
            self.used_count += 1
            return True
        return False

    def get_remaining_uses(self) -> int:
        """
        Get the number of remaining uses for this voucher.

        Returns:
            int: Number of remaining uses
        """
        return max(0, self.max_usage - self.used_count)
