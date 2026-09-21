from typing import Dict, Any, Optional
from app.config.settings import PLAN_LIMITS

def get_plan_limits(plan_name: str = "free") -> Dict[str, Any]:
    return PLAN_LIMITS.get(plan_name.lower(), PLAN_LIMITS["free"])

def has_feature(plan_name: str, feature: str) -> bool:
    limits = get_plan_limits(plan_name)
    features = limits.get("features", [])
    return feature in features

def is_within_limit(plan_name: str, metric_name: str, current_value: int) -> bool:
    limits = get_plan_limits(plan_name)
    limit_key = f"max_{metric_name}"
    if limit_key in limits:
        return current_value < limits[limit_key]
    return True

