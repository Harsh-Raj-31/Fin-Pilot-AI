from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FinPilot AI"
    API_VERSION: str = "v1"
    FRONTEND_URL: str = "http://localhost:3000"
    DEBUG: bool = True

    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "finpilot_ai"

    class Config:
        env_file = ".env"


settings = Settings()