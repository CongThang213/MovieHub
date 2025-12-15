from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class FilmTrailer:
    """
    Represents a trailer video for a film.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    film_id: Optional[str] = None
    title: str = ""
    url: str = ""
    order_index: int = 0
    uploaded_at: datetime = field(default_factory=datetime.now)
