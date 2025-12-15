import enum


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
