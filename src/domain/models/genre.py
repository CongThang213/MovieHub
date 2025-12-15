from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Genre:
    """
    Represents a film genre category (e.g., Action, Comedy, Drama).
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""  # e.g., "Action", "Comedy", "Drama"

    def __str__(self) -> str:
        """
        String representation of the genre.

        Returns:
            str: The name of the genre
        """
        return self.name
