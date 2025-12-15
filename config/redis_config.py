from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    """Configuration for Redis."""

    url: str

    model_config = SettingsConfigDict(
        env_prefix="REDIS_",  # will read REDIS_URL
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
