from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/music_manager"
    test_database_url: str = "postgresql://postgres:postgres@localhost:5432/music_manager_test"

    # Auth
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days

    # Spotify
    spotify_client_id: str = ""
    spotify_client_secret: str = ""

    # Anthropic
    anthropic_api_key: str = ""

    # App
    environment: str = "development"
    log_level: str = "INFO"


settings = Settings()
