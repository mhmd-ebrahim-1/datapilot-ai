from typing import Dict, Any, List
from pydantic_settings import BaseSettings, SettingsConfigDict

PLAN_LIMITS: Dict[str, Dict[str, Any]] = {
    "free": {
        "max_datasets": 5,
        "max_analyses_per_month": 10,
        "max_ai_requests_per_month": 20,
        "max_file_size_mb": 10,
        "max_storage_mb": 500,
        "max_chat_messages_per_month": 50,
        "max_reports_per_month": 5,
        "max_forecast_requests_per_month": 5,
        "features": ["basic_analytics", "basic_reports", "data_cleaning"]
    },
    "pro": {
        "max_datasets": 50,
        "max_analyses_per_month": 100,
        "max_ai_requests_per_month": 500,
        "max_file_size_mb": 50,
        "max_storage_mb": 5000,
        "max_chat_messages_per_month": 500,
        "max_reports_per_month": 50,
        "max_forecast_requests_per_month": 50,
        "features": ["basic_analytics", "basic_reports", "data_cleaning", "ai_chat", "forecasting", "anomaly_detection", "advanced_reports", "pdf_export"]
    },
    "business": {
        "max_datasets": 500,
        "max_analyses_per_month": 1000,
        "max_ai_requests_per_month": 5000,
        "max_file_size_mb": 200,
        "max_storage_mb": 50000,
        "max_chat_messages_per_month": 5000,
        "max_reports_per_month": 500,
        "max_forecast_requests_per_month": 500,
        "features": ["basic_analytics", "basic_reports", "data_cleaning", "ai_chat", "forecasting", "anomaly_detection", "advanced_reports", "pdf_export", "scheduled_reports", "white_label", "multi_user", "api_access"]
    }
}

class Settings(BaseSettings):
    APP_NAME: str = "DataPilot AI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "supersecretkey"
    SECRET_KEY: str = "datapilot-ai-production-super-secret-key-at-least-32-chars"
    FRONTEND_URL: str = "http://localhost:3000"
    BACKEND_URL: str = "http://localhost:8000"
    
    DATABASE_URL: str = "postgresql://user:password@localhost/datapilot"
    DATABASE_URL: str = "sqlite:///./datapilot.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    JWT_SECRET: str = "jwtsecretkey"
    JWT_SECRET: str = "datapilot-ai-jwt-secret-key-secure-at-least-32-chars"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    AI_PROVIDER: str = "mock"
    AI_API_KEY: str = ""
    AI_MODEL: str = ""
    
    STORAGE_PROVIDER: str = "local"
    STORAGE_PATH: str = "./uploads"
    MAX_FILE_SIZE_MB: int = 50
    
    EMAIL_PROVIDER: str = "console"
    EMAIL_FROM: str = "noreply@datapilot.ai"
    
    PAYMENT_PROVIDER: str = "mock"
    DEMO_MODE: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

def get_settings() -> Settings:
    return settings
