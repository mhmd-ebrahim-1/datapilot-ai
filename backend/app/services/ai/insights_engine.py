from typing import Dict, Any, List
from app.services.ai.mock_provider import MockAIProvider
from app.config.settings import settings

def get_ai_provider():
    # Factory based on settings
    return MockAIProvider()

async def orchestrate_insights(profile: Dict[str, Any], kpis: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    provider = get_ai_provider()
    
    context_metrics = {
        "kpis": kpis,
        "quality": profile.get("quality_metrics", {})
    }
    dataset_info = {
        "columns": list(profile.get("columns", {}).keys()),
        "row_count": profile.get("overall", {}).get("row_count", 0)
    }
    
    raw_insights = await provider.generate_insights(context_metrics, dataset_info)
    # Validation logic here (mocked for brevity)
    validated = raw_insights 
    return validated
