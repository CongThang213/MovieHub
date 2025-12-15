from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from src.domain.models.seat_category import SeatCategory


@dataclass
class Seat:
    """
    Represents a seat within a cinema hall row.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    row_id: Optional[str] = None
    category_id: Optional[str] = None
    seat_number: int = 0
    pos_x: float = 0.0
    pos_y: float = 0.0
    is_accessible: bool = False
    external_label: Optional[str] = None
    category: Optional["SeatCategory"] = None

    def get_display_label(self) -> str:
        """
        Get a display label for this seat, either using the external label or generating one.

        Returns:
            str: The display label for this seat
        """
        if self.external_label:
            return self.external_label
        return str(self.seat_number)

    def is_valid(self) -> bool:
        """
        Check if the seat has all required fields filled.

        Returns:
            bool: True if valid, False otherwise
        """
        return bool(self.row_id and self.category_id and self.seat_number > 0)
