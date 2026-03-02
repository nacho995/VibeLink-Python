from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://postgres:Inventario123!@localhost:5432/vibelink"

    # JWT
    jwt_key: str = "VibelinkSecretKey123456789012345678901234"
    jwt_issuer: str = "Vibelink"
    jwt_audience: str = "VibelinkUsers"
    jwt_expiration_days: int = 1

    # Stripe
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""

    # External APIs
    tmdb_api_key: str = ""
    twitch_client_id: str = ""
    twitch_client_secret: str = ""

    # CORS
    cors_origins: str = "*"

    # App
    environment: str = "development"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


@lru_cache
def get_settings() -> Settings:
    return Settings()
