from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    API_VERSION: str
    DEBUG: bool

    FRONTEND_URL: str
    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "finpilot_ai"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()