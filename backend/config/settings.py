"""
Phoenix SRE: Settings Configuration
Environment variables and application settings
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Phoenix SRE API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    PORT: int = 8080
    
    # GCP
    GCP_PROJECT_ID: str
    GCP_REGION: str = "europe-west1"
    
    # Services
    OLLAMA_URL: Optional[str] = None
    REDIS_URL: str = "redis://localhost:6379"
    FIRESTORE_PROJECT: Optional[str] = None
    
    # AI
    GEMINI_API_KEY: str
    GEMINI_PRIMARY_MODEL: str = "gemini-2.5-pro"
    GEMINI_FALLBACK_MODEL: str = "gemini-1.5-flash"
    
    # Budget
    BUDGET_LIMIT_USD: float = 10.00
    COST_ALERT_THRESHOLD_PERCENT: float = 80.0
    
    # WebSocket
    WEBSOCKET_PING_INTERVAL: int = 25
    WEBSOCKET_PING_TIMEOUT: int = 60
    
    # Metrics
    METRICS_INTERVAL_MS: int = 200
    METRICS_RETENTION_HOURS: int = 24
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()
