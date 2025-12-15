from pydantic_settings import BaseSettings, SettingsConfigDict


class VNPaySettings(BaseSettings):
    """Configuration for VNPay payment gateway."""

    version: str
    tmncode: str
    hash_secret: str
    payment_url: str
    return_url: str

    model_config = SettingsConfigDict(
        env_prefix="VNPAY_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
