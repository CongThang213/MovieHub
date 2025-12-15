import re
from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class ValidationConfig:
    """Configuration class for validation limits"""

    # Name validation
    name_max_length: int = 100

    # Password validation
    password_min_length: int = 8
    password_max_length: int = 128
    password_require_uppercase: bool = True
    password_require_lowercase: bool = True
    password_require_digit: bool = True
    password_require_special: bool = True
    password_special_chars: str = '!@#$%^&*(),.?":{}|<>'

    # Date of birth validation
    dob_allow_future: bool = False


# Default configuration instance
DEFAULT_CONFIG = ValidationConfig()


def validate_name(
    value: str,
    max_length: Optional[int] = None,
    config: Optional[ValidationConfig] = None,
) -> str:
    """
    Validate a name string with configurable limits.

    Args:
        value: The name to validate
        max_length: Override for maximum length (optional)
        config: Custom validation configuration (optional)

    Returns:
        The validated and stripped name
    """
    config = config or DEFAULT_CONFIG
    max_len = max_length or config.name_max_length

    stripped_value = value.strip()

    if not stripped_value:
        raise ValueError("Name cannot be empty or blank")

    if len(stripped_value) > max_len:
        raise ValueError(f"Name must be at most {max_len} characters")

    return stripped_value


def validate_password(
    value: str,
    current_password: Optional[str] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    config: Optional[ValidationConfig] = None,
) -> str:
    """
    Validate a password with configurable requirements.

    Args:
        value: The password to validate
        current_password: Current password to check against (optional)
        min_length: Override for minimum length (optional)
        max_length: Override for maximum length (optional)
        config: Custom validation configuration (optional)

    Returns:
        The validated and stripped password
    """
    config = config or DEFAULT_CONFIG
    min_len = min_length or config.password_min_length
    max_len = max_length or config.password_max_length

    stripped_value = value.strip()
    length = len(stripped_value)

    if not stripped_value:
        raise ValueError("Password cannot be empty or blank")

    if current_password and stripped_value == current_password:
        raise ValueError("New password must be different from current password")

    if length < min_len:
        raise ValueError(f"Password must be at least {min_len} characters long")
    if length > max_len:
        raise ValueError(f"Password cannot exceed {max_len} characters")

    # Build patterns based on configuration
    patterns = []
    if config.password_require_uppercase:
        patterns.append((r"[A-Z]", "at least one uppercase letter"))
    if config.password_require_lowercase:
        patterns.append((r"[a-z]", "at least one lowercase letter"))
    if config.password_require_digit:
        patterns.append((r"[0-9]", "at least one digit"))
    if config.password_require_special:
        special_pattern = f"[{re.escape(config.password_special_chars)}]"
        patterns.append((special_pattern, "at least one special character"))

    for pattern, message in patterns:
        if not re.search(pattern, stripped_value):
            raise ValueError(f"Password must contain {message}")

    return stripped_value


def validate_dob(
    value: Optional[date] = None,
    allow_future: Optional[bool] = None,
    config: Optional[ValidationConfig] = None,
) -> date:
    """
    Validate a date of birth with configurable rules.

    Args:
        value: The date of birth to validate
        allow_future: Override for allowing future dates (optional)
        config: Custom validation configuration (optional)

    Returns:
        The validated date
    """
    config = config or DEFAULT_CONFIG
    future_allowed = (
        allow_future if allow_future is not None else config.dob_allow_future
    )

    if value and not future_allowed and value > date.today():
        raise ValueError("Date of birth cannot be in the future")
    return value


def create_custom_config(**kwargs) -> ValidationConfig:
    """
    Create a custom validation configuration.

    Args:
        **kwargs: Configuration parameters to override

    Returns:
        A new ValidationConfig instance with custom settings
    """
    return ValidationConfig(**kwargs)
