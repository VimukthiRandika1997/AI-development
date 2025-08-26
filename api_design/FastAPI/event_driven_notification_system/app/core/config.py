# Settings via environment variables
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "development"
    APP_PORT: int = 8000
    REDIS_URL: str
    WEBHOOK_SECRET: str = ""
    WEBHOOK_TARGET_URL: str = os.getenv("WEBHOOK_URL")

class Config:
    env_file = ".env"

settings = Settings()