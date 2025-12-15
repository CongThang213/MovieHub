from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class City:
    """
    Represents a city where cinemas are located.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    country: str = ""

    def get_display_name(self) -> str:
        """
        Get a formatted display name for the city, including country.

        Returns:
            str: Formatted city name with country
        """
        return f"{self.name}, {self.country}"

    def is_valid(self) -> bool:
        """
        Check if the city has all required fields filled.

        Returns:
            bool: True if valid, False otherwise
        """
        return bool(self.name and self.country)
