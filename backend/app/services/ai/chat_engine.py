import pandas as pd
import logging
from typing import Dict, Any, Optional
from app.services.ai.semantic_resolver import SemanticResolver
from app.services.ai.intent_engine import IntentEngine, QueryPlan
from app.services.ai.query_engine import QueryExecutionEngine
from app.services.ai.deterministic_explainer import DeterministicExplainer
from app.services.ai.provider import AIProvider

logger = logging.getLogger("datapilot.chat")

# In-memory session query plan cache for follow-up question context
_SESSION_PLANS: Dict[str, QueryPlan] = {}

class ChatEngine:
    """Production-grade deterministic analytics query engine with optional LLM narrative explanation."""

    def __init__(self, ai_provider: Optional[AIProvider] = None):
        self.provider = ai_provider

    async def answer(
        self,
        question: str,
        df: pd.DataFrame,
        dataset_info: Dict[str, Any],
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        dataset_name = dataset_info.get("name", "Dataset")
        
        # 1. Semantic resolution of columns & entities
        resolver = SemanticResolver(df)
        
        # 2. Retrieve previous plan for follow-up questions if available
        prev_plan = _SESSION_PLANS.get(session_id) if session_id else None
        
        # 3. Parse intent into analytical query plan
        intent_engine = IntentEngine(resolver)
        plan = intent_engine.parse_intent(question, previous_plan=prev_plan)
        
        # Cache plan for follow-ups
        if session_id:
            _SESSION_PLANS[session_id] = plan
            
        # 4. Execute deterministic calculation directly on DataFrame
        execution_engine = QueryExecutionEngine(df)
        analysis_result = execution_engine.execute(plan)
        
        # 5. Generate verified deterministic explanation
        deterministic_message = DeterministicExplainer.explain(analysis_result, dataset_name=dataset_name)
        final_message = deterministic_message
        
        # 6. Optional LLM narrative explanation (if valid provider configured)
        if self.provider and not getattr(self.provider, "is_mock", False):
            try:
                llm_response = await self.provider.answer_question(
                    question=question,
                    context=analysis_result,
                    data_summary={
                        "name": dataset_name,
                        "row_count": len(df),
                        "columns": list(df.columns)
                    }
                )
                if llm_response and len(llm_response.strip()) > 10 and "[Mock Generated]" not in llm_response:
                    final_message = llm_response.strip()
            except Exception as e:
                logger.warning(f"LLM provider failed or rate limited, using deterministic explanation: {e}")
                final_message = deterministic_message
                
        return {
            "answer": final_message,
            "analysis": analysis_result,
            "context": analysis_result,
            "methodology": "100% Deterministic Pandas aggregation on verified dataset records"
        }
