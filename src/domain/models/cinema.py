from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4


@dataclass
class Cinema:
    """
    Represents a cinema location where films are shown.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    city_id: Optional[str] = None
    name: str = ""
    address: str = ""
    lat: float = 0.0
    long: float = 0.0
    rating: float = 0.0
    thumbnail_image_url: Optional[str] = None

    def update_rating(self, new_rating: float) -> None:
        """
        Update the cinema's rating, ensuring it stays within valid range.

        Args:
            new_rating: The new rating value
        """
        # Ensure rating is between 0 and 5
        self.rating = max(0.0, min(5.0, new_rating))

    def update_coordinates(self, latitude: float, longitude: float) -> None:
        """
        Update the geographical coordinates of the cinema.

        Args:
            latitude: The latitude coordinate
            longitude: The longitude coordinate
        """
        self.lat = latitude
        self.long = longitude

    def is_valid(self) -> bool:
        """
        Check if the cinema has all required fields filled.

        Returns:
            bool: True if valid, False otherwise
        """
        return bool(
            self.city_id
            and self.name
            and self.address
            and -90 <= self.lat <= 90
            and -180 <= self.long <= 180
        )
