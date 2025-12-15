from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from src.domain.models.film import Film
from src.domain.models.film_cast import FilmCast


@dataclass
class FilmDetail:
    film: Film
    genres: List[str] = field(default_factory=list)
    casts: List[FilmCast] = field(default_factory=list)
    trailers: List["FilmTrailer"] = field(default_factory=list)
    showtimes: List[datetime] = field(default_factory=list)
    reviews: List[str] = field(default_factory=list)
    promotions: List["FilmPromotion"] = field(default_factory=list)
