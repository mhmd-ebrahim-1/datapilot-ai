from typing import Dict, Any, List
from .provider import AIProvider
import uuid

class MockAIProvider(AIProvider):
    async def generate_insights(self, metrics: Dict[str, Any], dataset_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        insights = []
        if 'Total Revenue' in str(metrics):
            insights.append({
                "title": "Strong Revenue Trend",
                "category": "performance",
                "severity": "info",
                "description": "Revenue shows a stable trend across the dataset period.",
                "recommendation": "Investigate top selling products to maximize this trend.",
                "supporting_metrics_json": {"trend": "stable"}
            })
        insights.append({
            "title": "Data Completeness Alert",
            "category": "risk",
            "severity": "warning",
            "description": "There are some missing values that might affect deep analysis.",
            "recommendation": "Use the data cleaning tool to impute missing fields.",
            "supporting_metrics_json": {}
        })
        return insights
        
    async def answer_question(self, question: str, context: Dict[str, Any], data_summary: Dict[str, Any]) -> str:
        return f"[Mock Generated] Based on the context provided, here is the answer to: '{question}'. The data contains {data_summary.get('row_count', 'many')} records."
        
    async def classify_dataset(self, columns: List[str], sample_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        from app.services.profiling.type_detector import detect_type
        return detect_type(columns)
        
    async def generate_report_summary(self, analysis_data: Dict[str, Any]) -> str:
        return "This is a mock executive summary for the generated report. The dataset shows typical distributions."
