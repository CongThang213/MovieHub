from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4


@dataclass
class Hall:
    """
    Represents a cinema hall/auditorium where films are shown.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    cinema_id: Optional[str] = None
    name: str = ""
    capacity: int = 0
    description: Optional[str] = None

    def is_valid(self) -> bool:
        """
        Check if the hall has all required fields filled.

        Returns:
            bool: True if valid, False otherwise
        """
        return bool(self.cinema_id and self.name and self.capacity > 0)
