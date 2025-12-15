from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import uuid4


@dataclass
class Cast:
    """
    Represents a cast member (actor, director, etc.) in a film.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    avatar_image_url: Optional[str] = None
    date_of_birth: Optional[date] = None
    biography: Optional[str] = None

    @property
    def calculate_age(self) -> Optional[int]:
        """
        Calculate actor's age based on date of birth.

        Returns:
            Optional[int]: The actor's age or None if date of birth is not set
        """
        if not self.date_of_birth:
            return None

        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )
