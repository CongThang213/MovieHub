from typing import Optional, Dict, Any


class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details
        super().__init__(self.message)


class DuplicateEntryException(AppException):
    def __init__(self, entry_type: str, identifier: dict):
        """
        Exception raised when a duplicate entry is detected.
        :param entry_type: The type of entry that is duplicated (e.g., "User", "Genre").
        :param identifier: The identifier of the duplicate entry (e.g., email, name) as a dict.
        """
        super().__init__(
            status_code=409,  # HTTP 409 Conflict
            error_code="DUPLICATE_ENTRY",
            message=f"{entry_type} with identifier {identifier} already exists.",
            details={"entry_type": entry_type, "identifier": identifier},
        )
