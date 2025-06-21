from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Evolve"
    
    # Authentication settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "evolve_secret_key_change_in_production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./evolve.db")
    
    # LLM settings
    DEFAULT_MODEL: str = "gpt-3.5-turbo"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # CORS settings
    CORS_ORIGINS: list = ["*"]  # In production, replace with specific origins
    
    class Config:
        env_file = ".env"

settings = Settings()
