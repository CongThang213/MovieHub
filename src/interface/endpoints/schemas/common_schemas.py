from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Schema for error responses that match the AppException format"""

    error_code: str = Field(..., description="A unique code identifying the error type")
    message: str = Field(..., description="A human-readable error message")
    details: Optional[Dict[str, Any]] = Field(
        None, description="Additional error details"
    )

class MessageResponse(BaseModel):
    """Generic schema for simple success messages"""

    message: str = Field(..., description="A success or information message")
