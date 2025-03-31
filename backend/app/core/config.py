from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "backend"
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    PORT: int = int(os.getenv("PORT", "8000"))
    # Database settings

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

    class Config:
        case_sensitive = True


settings = Settings()
