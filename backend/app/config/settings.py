import os
from typing import Dict, Any, List, Optional, Union
from pydantic import field_validator
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
    DEBUG: bool = False
    SECRET_KEY: str = "datapilot-ai-production-super-secret-key-at-least-32-chars"
    FRONTEND_URL: str = "http://localhost:3000"
    BACKEND_URL: str = "http://localhost:8000"
    
    # CORS
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3000",
        "https://datapilot-ai.vercel.app",
        "https://datapilot.ai"
    ]
    
    # Database
    DATABASE_URL: str = "sqlite:///./datapilot.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Authentication & JWT
    JWT_SECRET: str = "datapilot-ai-jwt-secret-key-secure-at-least-32-chars"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours in minutes
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # AI Provider
    AI_PROVIDER: str = "mock"
    AI_API_KEY: str = ""
    GEMINI_API_KEY: Optional[str] = None
    AI_MODEL: str = "gemini-2.0-flash"
    
    # Storage
    STORAGE_PROVIDER: str = "local"  # local, s3
    STORAGE_PATH: str = "./uploads"
    STORAGE_BUCKET: Optional[str] = None
    STORAGE_ENDPOINT: Optional[str] = None
    STORAGE_REGION: Optional[str] = "us-east-1"
    STORAGE_ACCESS_KEY: Optional[str] = None
    STORAGE_SECRET_KEY: Optional[str] = None
    MAX_FILE_SIZE_MB: int = 50
    
    # Email
    EMAIL_PROVIDER: str = "console"
    EMAIL_FROM: str = "noreply@datapilot.ai"
    
    # Payment / Billing
    PAYMENT_PROVIDER: str = "mock"
    DEMO_MODE: bool = True

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str]) -> str:
        if not v:
            return "sqlite:///./datapilot.db"
        # Render/Heroku postgres URLs compatibility with SQLAlchemy
        if v.startswith("postgres://"):
            v = v.replace("postgres://", "postgresql://", 1)
        return v

    @field_validator("AI_API_KEY", mode="before")
    @classmethod
    def assemble_ai_key(cls, v: Optional[str], info) -> str:
        if v:
            return v
        # Fallback to GEMINI_API_KEY environment variable if AI_API_KEY is empty
        return os.getenv("GEMINI_API_KEY", "")

    @property
    def cors_origin_list(self) -> List[str]:
        if isinstance(self.CORS_ORIGINS, list):
            origins = list(self.CORS_ORIGINS)
        elif isinstance(self.CORS_ORIGINS, str):
            origins = [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]
        else:
            origins = []
        if self.FRONTEND_URL and self.FRONTEND_URL not in origins:
            origins.append(self.FRONTEND_URL)
        return origins

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

def get_settings() -> Settings:
    return settings
