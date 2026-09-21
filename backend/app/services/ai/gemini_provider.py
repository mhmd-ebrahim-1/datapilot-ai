import json
from typing import Any, List, Dict
from app.services.ai.provider import AIProvider
from app.config.settings import settings

class GeminiProvider(AIProvider):
    def __init__(self):
        import google.generativeai as genai
        genai.configure(api_key=settings.AI_API_KEY)
        self.model = genai.GenerativeModel(settings.AI_MODEL)
    
    async def generate_insights(self, metrics: dict, dataset_info: dict) -> list[dict]:
        prompt = f"""Analyze these business metrics and generate 5-8 actionable insights.
        
Dataset: {dataset_info.get('name', 'Unknown')}
Type: {dataset_info.get('dataset_type', 'General')}
Metrics: {json.dumps(metrics, default=str)}

Return JSON array of insights. Each insight must have:
- title: concise insight title
- category: one of [performance, growth, risk, anomaly, opportunity, recommendation]
- severity: one of [info, warning, critical]
- description: 2-3 sentence explanation
- recommendation: actionable recommendation
- supporting_metrics: dict of metric_name: value pairs from the provided metrics

IMPORTANT: Only reference numbers from the provided metrics. Do not invent values."""
        
        response = self.model.generate_content(prompt)
        try:
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            insights = json.loads(text.strip())
            return insights if isinstance(insights, list) else []
        except (json.JSONDecodeError, IndexError):
            return []
    
    async def answer_question(self, question: str, context: dict, data_summary: dict) -> str:
        prompt = f"""You are a data analyst assistant. Answer this question about a business dataset.

Question: {question}

Data Context:
{json.dumps(context, default=str)}

Dataset Summary:
{json.dumps(data_summary, default=str)}

Answer based ONLY on the provided data. If the data cannot answer the question, say so clearly.
Be concise and professional. Reference specific numbers from the context."""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    async def classify_dataset(self, columns: list, sample_rows: list) -> dict:
        prompt = f"""Classify this dataset type based on column names and sample data.
Columns: {columns}
Sample rows (first 3): {sample_rows[:3]}

Return JSON: {{"dataset_type": "Sales|Marketing|Finance|HR|Inventory|Operations|Customer|General", "confidence": 0.0-1.0, "reasoning": "brief explanation"}}"""
        response = self.model.generate_content(prompt)
        try:
            text = response.text
            if "```" in text:
                text = text.split("```json")[-1].split("```")[0] if "```json" in text else text.split("```")[1].split("```")[0]
            return json.loads(text.strip())
        except:
            return {"dataset_type": "General", "confidence": 0.5, "reasoning": "Could not classify"}
    
    async def generate_report_summary(self, analysis_data: dict) -> str:
        prompt = f"""Write a professional executive summary for this data analysis report.
Analysis: {json.dumps(analysis_data, default=str)}
Keep it to 3-4 paragraphs. Be specific with numbers. Professional tone."""
        response = self.model.generate_content(prompt)
        return response.text
