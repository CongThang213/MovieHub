from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4


@dataclass
class SeatRow:
    """
    Represents a row of seats in a cinema hall.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    hall_id: Optional[str] = None
    row_label: str = ""  # e.g., "A", "B", "C"
    row_order: int = 0  # For ordering rows from front to back

    def get_display_label(self) -> str:
        """
        Get a formatted display label for this row.

        Returns:
            str: The display label for this row
        """
        return f"Row {self.row_label}"

    def is_valid(self) -> bool:
        """
        Check if the seat row has all required fields filled.

        Returns:
            bool: True if valid, False otherwise
        """
        return bool(self.hall_id and self.row_label)
