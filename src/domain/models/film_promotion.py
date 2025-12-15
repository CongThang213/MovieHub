from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4

from src.domain.enums.promotion_type import PromotionType


@dataclass
class FilmPromotion:
    """
    Represents a promotional offer for a film.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    film_id: Optional[str] = None
    type: str = PromotionType.DISCOUNT
    title: str = ""
    content: str = ""
    valid_from: datetime = field(default_factory=datetime.now)
    valid_until: Optional[datetime] = None

    def is_active(self) -> bool:
        """
        Check if the promotion is currently active.

        Returns:
            bool: True if the promotion is active, False otherwise
        """
        now = datetime.now()

        if now < self.valid_from:
            return False

        if self.valid_until and now > self.valid_until:
            return False

        return True
