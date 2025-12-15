from typing import Optional, List

from pydantic import BaseModel, Field, conlist


class SeatLayoutRequest(BaseModel):
    """Request schema for a single seat in a row."""

    seat_number: int = Field(..., ge=1, description="Seat number within the row")
    category_id: str = Field(
        ..., description="ID of the seat category (regular, VIP, accessible, etc.)"
    )
    pos_x: Optional[float] = Field(
        None, description="X position in the layout for visual representation"
    )
    pos_y: Optional[float] = Field(
        None, description="Y position in the layout for visual representation"
    )
    is_accessible: bool = Field(
        False, description="Whether the seat is wheelchair accessible"
    )
    external_label: Optional[str] = Field(
        None, max_length=50, description="Optional custom label for the seat"
    )


class RowLayoutRequest(BaseModel):
    """Request schema for a single row in the hall layout."""

    row_label: str = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Label for the row (e.g., 'A', 'B', '1', '2')",
    )
    row_order: int = Field(
        ..., ge=1, description="Order of the row from front to back (1 = front)"
    )
    seats: List[SeatLayoutRequest] = Field(
        ..., min_items=1, description="List of seats in this row"
    )


class HallLayoutCreateRequest(BaseModel):
    """Request schema for creating a complete hall layout."""

    rows: conlist(RowLayoutRequest, min_length=1) = Field()

    class Config:
        json_schema_extra = {
            "example": {
                "rows": [
                    {
                        "row_label": "A",
                        "row_order": 1,
                        "seats": [
                            {
                                "seat_number": 1,
                                "category_id": "vip-category-id",
                                "is_accessible": False,
                            },
                            {
                                "seat_number": 2,
                                "category_id": "vip-category-id",
                                "is_accessible": False,
                            },
                            {
                                "seat_number": 3,
                                "category_id": "vip-category-id",
                                "is_accessible": True,
                            },
                        ],
                    },
                    {
                        "row_label": "B",
                        "row_order": 2,
                        "seats": [
                            {
                                "seat_number": 1,
                                "category_id": "regular-category-id",
                                "is_accessible": False,
                            },
                            {
                                "seat_number": 2,
                                "category_id": "regular-category-id",
                                "is_accessible": False,
                            },
                            {
                                "seat_number": 3,
                                "category_id": "regular-category-id",
                                "is_accessible": False,
                            },
                            {
                                "seat_number": 4,
                                "category_id": "regular-category-id",
                                "is_accessible": False,
                            },
                        ],
                    },
                ]
            }
        }


class HallLayoutUpdateRequest(BaseModel):
    """Request schema for updating a complete hall layout."""

    rows: conlist(RowLayoutRequest, min_length=1) = Field(
        ..., description="List of rows in the hall"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "rows": [
                    {
                        "row_label": "A",
                        "row_order": 1,
                        "seats": [
                            {
                                "seat_number": 1,
                                "category_id": "vip-category-id",
                                "is_accessible": False,
                            },
                            {
                                "seat_number": 2,
                                "category_id": "vip-category-id",
                                "is_accessible": False,
                            },
                        ],
                    }
                ]
            }
        }


class SeatLayoutResponse(BaseModel):
    """Response schema for a single seat."""

    id: str
    seat_number: int
    seat_code: str = Field(
        ..., description="Auto-generated seat code (e.g., 'A1', 'B3')"
    )
    category_id: str
    pos_x: float
    pos_y: float
    is_accessible: bool
    external_label: Optional[str] = None

    class Config:
        from_attributes = True


class RowLayoutResponse(BaseModel):
    """Response schema for a single row."""

    id: str
    row_label: str
    row_order: int
    seats: List[SeatLayoutResponse]

    class Config:
        from_attributes = True


class HallLayoutResponse(BaseModel):
    """Response schema for the complete hall layout."""

    hall_id: str
    total_seats: int
    rows: List[RowLayoutResponse]

    class Config:
        from_attributes = True


class HallLayoutSuccessResponse(BaseModel):
    """Success response for layout operations."""

    message: str
    hall_id: str
    total_rows: int
    total_seats: int
    layout: HallLayoutResponse


class HallLayoutErrorResponse(BaseModel):
    """Error response for layout operations."""

    error: str
    details: Optional[dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid layout configuration",
                "details": {
                    "row": "A",
                    "seat_number": 5,
                    "reason": "Seat category does not exist",
                },
            }
        }
