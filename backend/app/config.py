"""Application configuration."""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""

    # Application
    APP_NAME: str = "Zorvan Bot - Class Audio Organizer"
    DEBUG: bool = True
    API_VERSION: str = "v1"

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 days

    # Database
    DATABASE_URL: str = "sqlite:///./zorvan_bot.db"

    # OpenAI
    OPENAI_API_KEY: str = ""

    # File Upload
    MAX_UPLOAD_SIZE: int = 5368709120  # 5GB
    UPLOAD_DIR: str = "./uploads"
    TRANSCRIPTION_DIR: str = "./transcriptions"
    VECTOR_STORE_DIR: str = "./vector_store"

    # Whisper
    WHISPER_MODEL: str = "base"

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # Admin User
    ADMIN_EMAIL: str = "vfx.soli@gmail.com"
    ADMIN_PASSWORD: str = "Ali011111"

    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
