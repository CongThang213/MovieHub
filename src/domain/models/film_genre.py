from dataclasses import dataclass
from typing import Optional


@dataclass
class FilmGenre:
    """
    Represents the relationship between a film and a genre.
    """

    film_id: Optional[str] = None
    genre_id: Optional[str] = None
