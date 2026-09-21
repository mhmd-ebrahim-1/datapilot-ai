import re
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from app.services.ai.semantic_resolver import SemanticResolver

@dataclass
class QueryPlan:
    intent: str
    metric: Optional[str] = None
    dimension: Optional[str] = None
    date_col: Optional[str] = None
    aggregation: str = "sum"
    limit: int = 5
    filter_col: Optional[str] = None
    filter_val: Optional[str] = None
    time_grain: str = "monthly"
    is_distinct: bool = False
    raw_query: str = ""

def contains_word(pattern_list, text):
    for p in pattern_list:
        if re.search(r'\b' + re.escape(p) + r'\b', text):
            return True
    return False

class IntentEngine:
    """Parses natural language business questions into deterministic analytical execution plans."""

    def __init__(self, resolver: SemanticResolver):
        self.resolver = resolver

    def parse_intent(self, question: str, previous_plan: Optional[QueryPlan] = None) -> QueryPlan:
        q = question.strip()
        q_lower = q.lower()
        
        # 1. Contextual Follow-Up
        # e.g. "What about profit?", "And for Central?", "How about top 10?"
        if previous_plan and (
            q_lower.startswith(("what about", "how about", "and for", "and by", "and with", "what is the profit", "what about sales"))
            or len(q_lower.split()) <= 3
        ):
            new_metric = None
            for m in self.resolver.metrics:
                if re.search(r'\b' + re.escape(str(m).lower()) + r'\b', q_lower):
                    new_metric = m
                    break
            if not new_metric:
                for syn_group, syns in [("profit", ["profit", "margin"]), ("sales", ["sales", "revenue"]), ("discount", ["discount"]), ("quantity", ["quantity", "volume"])]:
                    if any(s in q_lower for s in syns):
                        new_metric = self.resolver.resolve_metric(syn_group)
                        break
                        
            new_dim = None
            for d in self.resolver.dimensions:
                if re.search(r'\b' + re.escape(str(d).lower()) + r'\b', q_lower):
                    new_dim = d
                    break
                    
            limit_match = re.search(r'\b(?:top|bottom|first|last)\s+(\d+)\b', q_lower)
            new_limit = int(limit_match.group(1)) if limit_match else previous_plan.limit
            
            if new_metric or new_dim or limit_match:
                return QueryPlan(
                    intent=previous_plan.intent,
                    metric=new_metric or previous_plan.metric,
                    dimension=new_dim or previous_plan.dimension,
                    date_col=previous_plan.date_col,
                    aggregation=previous_plan.aggregation,
                    limit=new_limit,
                    raw_query=q
                )

        # 2. Extract Limit (e.g. "top 5", "top 10", "best 3")
        limit = 5
        limit_match = re.search(r'\b(?:top|bottom|best|worst|first|last|highest|lowest)\s+(\d+)\b', q_lower)
        if limit_match:
            limit = int(limit_match.group(1))

        # 3. SUMMARY
        if contains_word(["summary", "summarize", "overview", "describe", "what is this dataset", "dataset summary"], q_lower):
            return QueryPlan(intent="SUMMARY", raw_query=q)

        # 4. COUNT / HOW MANY / COUNT DISTINCT
        if contains_word(["how many", "count of", "number of", "total count", "unique count", "distinct count"], q_lower) or (
            contains_word(["unique", "distinct"], q_lower) and not contains_word(["average", "sum", "top"], q_lower)
        ):
            target_col, is_distinct = self.resolver.resolve_count_target(q_lower)
            return QueryPlan(
                intent="COUNT_DISTINCT" if is_distinct or contains_word(["unique", "distinct"], q_lower) else "COUNT",
                metric=target_col,
                dimension=target_col,
                is_distinct=is_distinct,
                raw_query=q
            )

        # 5. AVERAGE / MEAN
        if contains_word(["average", "avg", "mean", "typical"], q_lower):
            metric = self.resolver.resolve_metric(q_lower)
            dim = None
            if contains_word(["by", "per", "across", "for each"], q_lower):
                dim = self.resolver.resolve_dimension(q_lower)
            return QueryPlan(
                intent="AVERAGE",
                metric=metric,
                dimension=dim,
                aggregation="mean",
                raw_query=q
            )

        # 6. MONTHLY / TIME / TEMPORAL WINNER (e.g. "what month had the highest sales")
        if contains_word(["month", "year", "quarter", "timeline"], q_lower) and contains_word(["highest", "most", "best", "lowest", "least", "sales", "profit", "trend"], q_lower):
            metric = self.resolver.resolve_metric(q_lower)
            date_col = self.resolver.resolve_date(q_lower)
            return QueryPlan(
                intent="TREND",
                metric=metric,
                date_col=date_col,
                aggregation="sum",
                raw_query=q
            )

        # 7. TREND / TIME SERIES / OVER TIME
        if contains_word(["trend", "trends", "over time", "change over time", "by month", "monthly", "growth", "seasonality", "historical"], q_lower):
            metric = self.resolver.resolve_metric(q_lower)
            date_col = self.resolver.resolve_date(q_lower)
            return QueryPlan(
                intent="TREND",
                metric=metric,
                date_col=date_col,
                aggregation="sum",
                raw_query=q
            )

        # 8. HIGHEST / MAXIMUM / LOWEST / MINIMUM / WINNER
        # "which region generated the highest sales", "which category has the highest sales"
        if contains_word(["highest", "largest", "maximum", "max", "greatest", "most sales", "most profit", "most revenue", "best category", "best region"], q_lower):
            dim = self.resolver.resolve_dimension(q_lower)
            metric = self.resolver.resolve_metric(q_lower)
            if limit_match and limit > 1:
                return QueryPlan(intent="TOP_N", metric=metric, dimension=dim, limit=limit, raw_query=q)
            return QueryPlan(
                intent="MAX",
                metric=metric,
                dimension=dim,
                aggregation="sum",
                limit=1,
                raw_query=q
            )

        if contains_word(["lowest", "least", "smallest", "minimum", "min", "worst"], q_lower):
            dim = self.resolver.resolve_dimension(q_lower)
            metric = self.resolver.resolve_metric(q_lower)
            if limit_match and limit > 1:
                return QueryPlan(intent="BOTTOM_N", metric=metric, dimension=dim, limit=limit, raw_query=q)
            return QueryPlan(
                intent="MIN",
                metric=metric,
                dimension=dim,
                aggregation="sum",
                limit=1,
                raw_query=q
            )

        # 9. TOP_N / BOTTOM_N
        if contains_word(["top", "best", "leading", "most popular", "highest ranking"], q_lower):
            dim = self.resolver.resolve_dimension(q_lower)
            metric = self.resolver.resolve_metric(q_lower)
            return QueryPlan(
                intent="TOP_N",
                metric=metric,
                dimension=dim,
                aggregation="sum",
                limit=limit,
                raw_query=q
            )
            
        if contains_word(["bottom", "worst", "lowest ranking"], q_lower):
            dim = self.resolver.resolve_dimension(q_lower)
            metric = self.resolver.resolve_metric(q_lower)
            return QueryPlan(
                intent="BOTTOM_N",
                metric=metric,
                dimension=dim,
                aggregation="sum",
                limit=limit,
                raw_query=q
            )

        # 10. ANOMALY / OUTLIER DETECTION
        if contains_word(["anomaly", "anomalies", "unusual", "outlier", "outliers", "abnormal", "unexpected", "strange"], q_lower):
            metric = self.resolver.resolve_metric(q_lower)
            dim = self.resolver.resolve_dimension(q_lower)
            return QueryPlan(
                intent="ANOMALY",
                metric=metric,
                dimension=dim,
                raw_query=q
            )

        # 11. TOTAL / SUM
        if contains_word(["total", "sum", "overall", "aggregate"], q_lower):
            metric = self.resolver.resolve_metric(q_lower)
            dim = None
            if contains_word(["by", "per", "across", "for each"], q_lower):
                dim = self.resolver.resolve_dimension(q_lower)
            return QueryPlan(
                intent="SUM" if not dim else "GROUP_BY",
                metric=metric,
                dimension=dim,
                aggregation="sum",
                raw_query=q
            )

        # 12. GROUP_BY / COMPARISON / BREAKDOWN / DISTRIBUTION
        if contains_word(["by", "breakdown", "distribution", "per", "across", "compare", "split"], q_lower):
            dim = self.resolver.resolve_dimension(q_lower)
            metric = self.resolver.resolve_metric(q_lower)
            return QueryPlan(
                intent="GROUP_BY",
                metric=metric,
                dimension=dim,
                aggregation="sum",
                limit=10,
                raw_query=q
            )

        # 13. Default intelligent fallback
        dim = self.resolver.resolve_dimension(q_lower)
        metric = self.resolver.resolve_metric(q_lower)
        if dim and metric:
            return QueryPlan(intent="GROUP_BY", metric=metric, dimension=dim, limit=5, raw_query=q)
        elif metric:
            return QueryPlan(intent="SUM", metric=metric, raw_query=q)
        else:
            return QueryPlan(intent="SUMMARY", raw_query=q)

