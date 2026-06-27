import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Vision-Agentic Scraper - Agent Core"
    API_V1_STR: str = "/api/v1"

    DEFAULT_VIEWPORT_WIDTH: int = 1280
    DEFAULT_VIEWPORT_HEIGHT: int = 720

    class config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()