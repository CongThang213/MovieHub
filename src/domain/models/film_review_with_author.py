from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class FilmReviewWithAuthor:
    """
    Represents a film review with author details for display purposes.
    """

    id: str
    film_id: str
    author_id: str
    author_name: str  # Author name
    avatar_url: Optional[str]  # Author avatar URL
    rating: int
    content: str
    created_at: datetime  # Review creation timestamp
