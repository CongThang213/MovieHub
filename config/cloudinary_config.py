from pydantic_settings import BaseSettings


class CloudinarySettings(BaseSettings):
    """Cloudinary configuration settings."""

    cloud_name: str
    api_key: str
    api_secret: str
    secure: bool = True

    # Folder structure for organized storage
    AVATARS_FOLDER: str = "seatsync/users/avatars"
    FILM_THUMBNAILS_FOLDER: str = "seatsync/films/thumbnails"
    FILM_BACKGROUNDS_FOLDER: str = "seatsync/films/backgrounds"
    FILM_POSTERS_FOLDER: str = "seatsync/films/posters"

    # Temporary uploads folder (for client-side uploads)
    TEMP_FOLDER: str = "seatsync/temp"

    # Temporary image settings
    TEMP_IMAGE_EXPIRY_HOURS: int = 12  # How long temp images live
    CLEANUP_INTERVAL_HOURS: int = 6  # How often cleanup runs

    # Image transformation presets
    AVATAR_SIZE: tuple = (200, 200)
    THUMBNAIL_SIZE: tuple = (400, 600)
    BACKGROUND_SIZE: tuple = (1920, 1080)
    POSTER_SIZE: tuple = (600, 900)

    # Temporary image preview sizes (smaller for faster upload)
    TEMP_PREVIEW_SIZE: tuple = (800, 600)

    class Config:
        env_prefix = "CLOUDINARY_"
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
