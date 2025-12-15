from typing import Optional, Dict, Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class FirebaseSettings(BaseSettings):
    """Configuration for Firebase."""

    credentials: Optional[Dict[str, Any]] = None

    model_config = SettingsConfigDict(
        env_prefix="FIREBASE_",
        case_sensitive=False,
        json_encoders={dict: lambda v: v},
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )
