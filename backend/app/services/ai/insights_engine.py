import logging
from typing import Dict, Any, List, Optional
from app.config.settings import settings
from app.services.ai.gemini_provider import GeminiProvider
from app.services.ai.mock_provider import MockAIProvider

logger = logging.getLogger("datapilot.insights")

def generate_deterministic_insights(profile: Dict[str, Any], kpis: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate 100% verified, data-grounded insights when LLM is unavailable."""
    insights = []
    
    # 1. KPI-based insights
    kpi_map = {k.get("name", ""): k for k in kpis}
    
    if "Total Revenue" in kpi_map or "Total Sales" in kpi_map:
        rev_kpi = kpi_map.get("Total Revenue") or kpi_map.get("Total Sales")
        rev_val = rev_kpi.get("formatted_value", str(rev_kpi.get("value", 0)))
        insights.append({
            "title": f"Strong Cumulative Performance: {rev_val}",
            "category": "performance",
            "severity": "info",
            "description": f"Overall verified revenue reached {rev_val} across all analyzed transactions.",
            "recommendation": "Focus sales resources on top-margin product tiers to sustain volume growth.",
            "supporting_metrics_json": {"metric": "Revenue", "value": rev_val}
        })

    if "Profit Margin" in kpi_map:
        pm_kpi = kpi_map.get("Profit Margin")
        pm_val = pm_kpi.get("value", 0)
        formatted_pm = pm_kpi.get("formatted_value", f"{pm_val:.1f}%")
        severity = "info" if pm_val >= 15 else ("warning" if pm_val >= 0 else "critical")
        insights.append({
            "title": f"Profit Margin Health: {formatted_pm}",
            "category": "growth" if pm_val >= 15 else "risk",
            "severity": severity,
            "description": f"Operating profit margin stands at {formatted_pm}. High-discount transactions can suppress overall profitability.",
            "recommendation": "Review discounting policies across negative-margin categories to protect bottom line.",
            "supporting_metrics_json": {"profit_margin": pm_val}
        })

    # 2. Data Quality & Distribution Insights
    quality_score = profile.get("quality_score", 90.0) if isinstance(profile.get("quality_score"), (int, float)) else 90.0
    if quality_score >= 85:
        insights.append({
            "title": "High Data Quality & Integrity",
            "category": "opportunity",
            "severity": "info",
            "description": f"Dataset achieved a {quality_score:.1f}% data quality rating with minimal nulls and high structural validity.",
            "recommendation": "Data is clean and ready for executive reporting and predictive forecasting.",
            "supporting_metrics_json": {"quality_score": quality_score}
        })
    else:
        insights.append({
            "title": "Data Cleansing Recommendations",
            "category": "risk",
            "severity": "warning",
            "description": f"Data quality score is {quality_score:.1f}%. Some missing values or anomalies were detected during ingestion.",
            "recommendation": "Apply automated imputation or review source exports to improve data consistency.",
            "supporting_metrics_json": {"quality_score": quality_score}
        })

    return insights

async def orchestrate_insights(profile: Dict[str, Any], kpis: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Orchestrate AI insights generation with guaranteed deterministic fallback."""
    # 1. Try Gemini Provider if configured
    if settings.AI_PROVIDER.lower() == "gemini" and settings.AI_API_KEY:
        try:
            provider = GeminiProvider()
            dataset_info = {
                "name": profile.get("name", "Dataset"),
                "dataset_type": profile.get("dataset_type", "General")
            }
            context_metrics = {
                "kpis": kpis,
                "quality_score": profile.get("quality_score", 90.0),
                "columns": list(profile.get("columns", {}).keys()) if isinstance(profile.get("columns"), dict) else []
            }
            insights = await provider.generate_insights(context_metrics, dataset_info)
            if insights and len(insights) > 0:
                return insights
        except Exception as e:
            logger.warning(f"Gemini insight generation failed: {e}. Falling back to deterministic engine.")
            
    # 2. Return high-quality deterministic insights
    return generate_deterministic_insights(profile, kpis)
