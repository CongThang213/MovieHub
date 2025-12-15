from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class Banner:
    """
    Represents a banner for the hero section.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    image_url: str = ""
    fallback_image: Optional[str] = None
    alt_text: str = ""
    title: str = ""
    subtitle: str = ""
    cta_label: str = ""
    target_type: str = ""  # e.g., "movie", "promotion", "external"
    target_id: str = ""
    priority: int = 0
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    aspect_ratio: str = "16:9"

    def is_active(self) -> bool:
        """
        Check if the banner is currently active based on start_at and end_at times.

        Returns:
            bool: True if the banner is currently active, False otherwise
        """
        now = datetime.now()

        if self.start_at and now < self.start_at:
            return False

        if self.end_at and now > self.end_at:
            return False

        return True
