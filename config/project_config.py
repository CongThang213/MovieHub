from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectSettings(BaseSettings):
    """Configuration for the project settings."""

    name: str
    version: str

    model_config = SettingsConfigDict(
        env_prefix="PROJECT_",  # will read PROJECT_NAME, PROJECT_VERSION,...
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
