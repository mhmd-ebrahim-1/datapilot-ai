from typing import Dict, Any, List
from .provider import AIProvider
import uuid

class MockAIProvider(AIProvider):
    is_mock = True
    
    async def generate_insights(self, metrics: Dict[str, Any], dataset_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        insights = []
        if 'Total Revenue' in str(metrics) or 'Sales' in str(metrics):
            insights.append({
                "title": "Strong Revenue Performance",
                "category": "performance",
                "severity": "info",
                "description": "Revenue shows solid performance across top categories.",
                "recommendation": "Investigate top-selling products to maximize this trend.",
                "supporting_metrics_json": {"trend": "positive"}
            })
        insights.append({
            "title": "Data Distribution & Coverage",
            "category": "performance",
            "severity": "info",
            "description": f"Dataset records span {dataset_info.get('row_count', 'multiple')} transactions across primary business dimensions.",
            "recommendation": "Maintain regular data syncs for continuous intelligence.",
            "supporting_metrics_json": {}
        })
        return insights
        
    async def answer_question(self, question: str, context: Dict[str, Any], data_summary: Dict[str, Any]) -> str:
        return f"Based on verified data analysis of {data_summary.get('row_count', 'all')} records, the requested metrics have been computed directly from your dataset."
        
    async def classify_dataset(self, columns: List[str], sample_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        from app.services.profiling.type_detector import detect_type
        return detect_type(columns)
        
    async def generate_report_summary(self, analysis_data: Dict[str, Any]) -> str:
        return "Executive analytics summary based on verified business KPIs and dataset distributions."
