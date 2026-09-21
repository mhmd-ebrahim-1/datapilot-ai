import re
from typing import Dict, Any, List, Tuple

class InsightValidator:
    """Validates AI-generated insights against ground-truth structured metrics to prevent hallucinations."""
    
    @staticmethod
    def extract_numeric_tokens(text: str) -> List[float]:
        """Extract float and integer numbers from text, stripping currencies and commas."""
        cleaned = re.sub(r'[\$,%]', '', text)
        matches = re.findall(r'[-+]?(?:\d*\.\d+|\d+)', cleaned)
        results = []
        for m in matches:
            try:
                results.append(float(m))
            except ValueError:
                pass
        return results

    @staticmethod
    def collect_known_metric_values(metrics: Dict[str, Any]) -> List[float]:
        """Extract all valid ground truth numeric values from metrics dict."""
        values = []
        
        def _extract(val):
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                values.append(float(val))
            elif isinstance(val, dict):
                for v in val.values():
                    _extract(v)
            elif isinstance(val, list):
                for item in val:
                    _extract(item)
                    
        _extract(metrics)
        return values

    @classmethod
    def validate_insight(cls, insight: Dict[str, Any], ground_truth_metrics: Dict[str, Any]) -> Tuple[bool, str]:
        """Verify an insight claim against ground truth metrics."""
        title = insight.get("title", "")
        description = insight.get("description", "")
        supporting = insight.get("supporting_metrics", {})
        
        if not title or not description:
            return False, "Insight missing required title or description"
            
        known_values = cls.collect_known_metric_values(ground_truth_metrics)
        claimed_numbers = cls.extract_numeric_tokens(f"{title} {description}")
        
        # If the insight explicitly provides supporting metrics, check if they exist in ground truth
        if supporting and isinstance(supporting, dict):
            for k, v in supporting.items():
                if isinstance(v, (int, float)):
                    # Check tolerance match with known numbers
                    match = any(abs(float(v) - kv) < 0.01 or (kv != 0 and abs((float(v) - kv) / kv) < 0.05) for kv in known_values)
                    if not match and len(known_values) > 0:
                        return False, f"Supporting metric '{k}': {v} does not match computed dataset analytics"

        return True, "Validated"

    @classmethod
    def filter_valid_insights(cls, insights: List[Dict[str, Any]], ground_truth_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        valid = []
        for ins in insights:
            is_valid, reason = cls.validate_insight(ins, ground_truth_metrics)
            if is_valid:
                valid.append(ins)
        return valid

