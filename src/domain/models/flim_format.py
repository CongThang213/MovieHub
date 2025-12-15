from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class FilmFormat:
    """
    Represents a format in which films can be shown (e.g., IMAX, 3D, 4DX).
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""  # e.g., "IMAX", "3D", "4DX"
    description: str = ""
    surcharge: float = 0.0  # Additional cost for this format

    def has_surcharge(self) -> bool:
        """
        Check if this format has an additional surcharge.

        Returns:
            bool: True if surcharge exists, False otherwise
        """
        return self.surcharge > 0
