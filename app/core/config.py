from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Ecommerce API"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/ecommerce_db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
