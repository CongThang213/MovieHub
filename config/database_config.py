from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Configuration for the database connection."""

    url: str
    url_async: str
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10

    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",  # will read DATABASE_URL, DATABASE_ECHO,...
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
