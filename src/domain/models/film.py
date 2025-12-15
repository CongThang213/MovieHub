from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class Film:
    """
    Represents a film that can be shown in cinemas.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    votes: int = 0
    rating: float = 0.0
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    thumbnail_image_url: Optional[str] = None
    background_image_url: Optional[str] = None
    poster_image_url: Optional[str] = None
    movie_begin_date: Optional[datetime] = None
    movie_end_date: Optional[datetime] = None

    def is_currently_showing(self) -> bool:
        """
        Check if the film is currently showing in cinemas.

        Returns:
            bool: True if the film is currently showing, False otherwise
        """
        now = datetime.now()

        if not self.movie_begin_date:
            return False

        if now < self.movie_begin_date:
            return False

        if self.movie_end_date and now > self.movie_end_date:
            return False

        return True

    def update_rating(self, new_rating: float, new_vote: bool = False) -> None:
        """
        Update the film's rating with a new rating value.

        Args:
            new_rating: The new rating to incorporate
            new_vote: Whether this is a new vote or updating an existing one
        """
        if new_vote:
            # If it's a new vote, add it to the average
            total_rating = (self.rating * self.votes) + new_rating
            self.votes += 1
            self.rating = total_rating / self.votes
        else:
            # If it's not a new vote, just update the rating
            self.rating = new_rating

        # Ensure rating is between 0 and 10
        self.rating = max(0.0, min(10.0, self.rating))
