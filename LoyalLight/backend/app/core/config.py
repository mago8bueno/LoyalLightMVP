"""
Application configuration settings.
"""
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    mongo_url: str = "mongodb://localhost:27017"
    db_name: str = "loyallight_mvp"
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # OpenAI
    openai_api_key: str = ""
    
    # Rate Limiting
    rate_limit_requests_per_minute: int = 60
    rate_limit_burst: int = 10
    
    # Cache
    cache_ttl_seconds: int = 300
    redis_url: str = "redis://localhost:6379"
    
    # Application
    debug: bool = False
    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # AI Configuration
    ai_max_tokens: int = 500
    ai_temperature: float = 0.7
    ai_cache_enabled: bool = True
    
    class Config:
        env_file = ".env"


settings = Settings()

