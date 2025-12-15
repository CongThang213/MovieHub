from dataclasses import dataclass, field
from typing import List

from src.domain.models.film import Film


@dataclass
class FilmBrief:
    film: Film
    genres: List[str] = field(default_factory=list)
