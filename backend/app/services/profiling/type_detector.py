from typing import Union, List, Dict, Any
import pandas as pd

def detect_type(columns: Union[List[str], pd.DataFrame]) -> Dict[str, Any]:
    if isinstance(columns, pd.DataFrame):
        cols = columns.columns.tolist()
    else:
        cols = list(columns)
        
    columns_lower = [str(c).lower() for c in cols]
    
    sales_kw = {'revenue', 'sales', 'price', 'cost', 'order', 'quantity', 'product', 'customer', 'units_sold', 'item'}
    mkt_kw = {'impressions', 'clicks', 'ctr', 'cpc', 'campaign', 'channel', 'spend', 'conversions', 'roas', 'cpa'}
    fin_kw = {'income', 'expense', 'budget', 'profit', 'loss', 'balance', 'transaction', 'amount', 'tax'}
    hr_kw = {'employee', 'salary', 'department', 'hire', 'performance', 'tenure', 'headcount', 'turnover'}
    inv_kw = {'inventory', 'stock', 'warehouse', 'sku', 'reorder', 'supplier'}
    ops_kw = {'duration', 'latency', 'ticket', 'incident', 'sla', 'uptime'}
    
    scores = {'Sales': 0, 'Marketing': 0, 'Finance': 0, 'HR': 0, 'Inventory': 0, 'Operations': 0}
    matches = {k: [] for k in scores}
    
    for c in columns_lower:
        for kw in sales_kw:
            if kw in c: scores['Sales'] += 1; matches['Sales'].append(c)
        for kw in mkt_kw:
            if kw in c: scores['Marketing'] += 1; matches['Marketing'].append(c)
        for kw in fin_kw:
            if kw in c: scores['Finance'] += 1; matches['Finance'].append(c)
        for kw in hr_kw:
            if kw in c: scores['HR'] += 1; matches['HR'].append(c)
        for kw in inv_kw:
            if kw in c: scores['Inventory'] += 1; matches['Inventory'].append(c)
        for kw in ops_kw:
            if kw in c: scores['Operations'] += 1; matches['Operations'].append(c)
            
    best_type = max(scores, key=scores.get)
    if scores[best_type] == 0:
        return {"dataset_type": "General", "confidence": 0.5, "matched_columns": []}
        
    total_matches = scores[best_type]
    confidence = min(0.95, round(0.5 + (total_matches / max(len(cols), 1)) * 0.5, 2))
    
    return {
        "dataset_type": best_type,
        "confidence": confidence,
        "matched_columns": list(set(matches[best_type]))
    }

detect_dataset_type = detect_type
