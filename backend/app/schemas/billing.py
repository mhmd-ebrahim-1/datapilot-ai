from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class SubscriptionResponse(BaseModel):
    plan: str
    status: str
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None

class UsageMetric(BaseModel):
    used: int
    limit: int

class UsageResponse(BaseModel):
    plan: str
    analyses: UsageMetric
    ai_requests: UsageMetric
    uploads: UsageMetric
    storage_mb: UsageMetric

class CheckoutRequest(BaseModel):
    plan: str
