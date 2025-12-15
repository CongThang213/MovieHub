from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class FilmReview:
    """
    Represents a user review for a film, including rating and content.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    film_id: Optional[str] = None
    author_id: Optional[str] = None
    rating: int = 0
    content: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def is_valid_rating(self) -> bool:
        """
        Check if the rating is within valid range (1-5).

        Returns:
            bool: True if rating is valid, False otherwise
        """
        return 1 <= self.rating <= 5
