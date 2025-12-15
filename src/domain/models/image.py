import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

from src.domain.enums.image_type import ImageType


@dataclass
class Image:
    """
    Domain model for image metadata and storage information.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    owner_id: Optional[str] = None  # FK to user, film, etc.
    type: ImageType = ImageType.AVATAR
    public_id: str = ""
    url: str = ""
    is_temp: bool = True
    created_at: datetime = field(default_factory=datetime.now)

    def is_expired(self, hours: int = 24) -> bool:
        """Check if temporary image has expired."""
        if not self.is_temp:
            return False

        # Calculate the expiry time by adding hours to created_at without timezone
        expiry_time = self.created_at.replace(tzinfo=None) + timedelta(hours=hours)
        return datetime.now() > expiry_time
