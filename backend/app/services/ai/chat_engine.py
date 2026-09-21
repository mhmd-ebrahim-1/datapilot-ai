import pandas as pd
import json
from typing import Any
from app.services.ai.provider import AIProvider

class ChatEngine:
    def __init__(self, ai_provider: AIProvider):
        self.provider = ai_provider
    
    async def answer(self, question: str, df: pd.DataFrame, dataset_info: dict) -> dict:
        context = self._build_context(question, df)
        
        summary = {"rows": len(df), "columns": list(df.columns), "dtypes": {col: str(df[col].dtype) for col in df.columns}}
        answer = await self.provider.answer_question(question, context, summary)
        
        return {"answer": answer, "context": context, "methodology": "Deterministic analysis with AI explanation"}
    
    def _build_context(self, question: str, df: pd.DataFrame) -> dict:
        q = question.lower()
        context = {}
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if any(word in q for word in ['total', 'sum', 'revenue', 'sales', 'income']):
            for col in numeric_cols:
                context[f"total_{col}"] = float(df[col].sum())
        
        if any(word in q for word in ['best', 'top', 'most', 'highest', 'largest']):
            cat_cols = df.select_dtypes(include=['object']).columns.tolist()
            for cat_col in cat_cols[:3]:
                for num_col in numeric_cols[:2]:
                    top = df.groupby(cat_col)[num_col].sum().nlargest(5)
                    context[f"top_{cat_col}_by_{num_col}"] = {str(k): float(v) for k, v in top.items()}
        
        if any(word in q for word in ['average', 'avg', 'mean']):
            for col in numeric_cols:
                context[f"average_{col}"] = float(df[col].mean())
        
        if any(word in q for word in ['trend', 'growth', 'change', 'month']):
            date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
            if date_cols and numeric_cols:
                date_col = date_cols[0]
                num_col = numeric_cols[0]
                try:
                    monthly = df.set_index(date_col)[num_col].resample('M').sum()
                    context["monthly_trend"] = {str(k.date()): float(v) for k, v in monthly.items()}
                except Exception:
                    pass
        
        if not context:
            for col in numeric_cols[:5]:
                context[f"{col}_stats"] = {"mean": float(df[col].mean()), "sum": float(df[col].sum()), "min": float(df[col].min()), "max": float(df[col].max())}
        
        return context
