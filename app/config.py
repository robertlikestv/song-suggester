"""Application Config Module.

Loads and validates environment variables needed for Spotify and Last.fm
API wrappers using Pydantic Settings.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized application settings and credential validation."""

    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_REDIRECT_URI: str

    LASTFM_API_KEY: str
    LASTFM_API_SECRET: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Creates and caches the application settings instance.

    Returns:
        An initialized Settings object populated with validated environment variables.
    """
    return Settings()

# Global instance for direct imports across services
settings = get_settings()