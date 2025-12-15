import enum


class BookingStatus(str, enum.Enum):
    CREATED = "created"
    RESERVED = "reserved"
    PAID = "paid"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
