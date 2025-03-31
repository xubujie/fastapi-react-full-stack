from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "{{ cookiecutter.project_name }}"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:{{ cookiecutter.frontend_port }}", "http://127.0.0.1:{{ cookiecutter.frontend_port }}"]
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    PORT: int = int(os.getenv("PORT", "{{ cookiecutter.backend_port }}"))
    
    # Database settings
    {% if cookiecutter.use_sqlmodel == "y" %}
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    {% endif %}
    
    # OpenAI settings
    {% if cookiecutter.use_openai == "y" %}
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    {% endif %}
    
    class Config:
        case_sensitive = True
        
settings = Settings() 