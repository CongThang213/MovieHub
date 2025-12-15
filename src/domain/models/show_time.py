from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4


@dataclass
class ShowTime:
    """
    Represents a scheduled showing of a film in a specific hall.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    hall_id: Optional[str] = None
    film_id: Optional[str] = None
    film_format_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    available_seats: int = 0

    def is_happening_now(self) -> bool:
        """
        Check if this showtime is currently happening.

        Returns:
            bool: True if the showtime is currently happening, False otherwise
        """
        if not self.start_time or not self.end_time:
            return False

        now = datetime.now()
        return self.start_time <= now <= self.end_time

    def is_in_future(self) -> bool:
        """
        Check if this showtime is in the future.

        Returns:
            bool: True if the showtime is in the future, False otherwise
        """
        if not self.start_time:
            return False

        return datetime.now() < self.start_time

    def calculate_end_time(self, duration_minutes: int) -> None:
        """
        Calculate and set the end time based on start time and film duration.

        Args:
            duration_minutes: The duration of the film in minutes
        """
        if self.start_time:
            self.end_time = self.start_time + timedelta(minutes=duration_minutes)
