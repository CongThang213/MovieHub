from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class MailerSendSettings(BaseSettings):
    """Configuration for MailerSend email service."""

    api_key: str
    email: EmailStr

    model_config = SettingsConfigDict(
        env_prefix="MAILERSEND_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
