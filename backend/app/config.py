from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FinPilot AI"
    API_VERSION: str = "v1"
    FRONTEND_URL: str = "http://localhost:3000"
    DEBUG: bool = True

    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "finpilot_ai"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 
   

    class Config:
        env_file = ".env"



settings = Settings()