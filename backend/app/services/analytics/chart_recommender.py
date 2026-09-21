import pandas as pd
from typing import Dict, Any, List

def recommend_charts(df: pd.DataFrame, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    charts = []
    if df.empty: return charts

    num_cols = [c for c, p in profile.get('columns', {}).items() if p.get('type') == 'numeric']
    cat_cols = [c for c, p in profile.get('columns', {}).items() if p.get('type') == 'categorical']
    dt_cols = [c for c, p in profile.get('columns', {}).items() if p.get('type') == 'datetime']

    if dt_cols and num_cols:
        dt_col, num_col = dt_cols[0], num_cols[0]
        agg = df.groupby(pd.to_datetime(df[dt_col]).dt.to_period('M'))[num_col].sum().reset_index()
        agg[dt_col] = agg[dt_col].astype(str)
        if len(agg) > 1:
            charts.append({
                "chart_type": "line",
                "title": f"{num_col.title()} over Time",
                "x_column": dt_col,
                "y_column": num_col,
                "data": agg.tail(100).to_dict(orient='records'),
                "config": {}
            })

    if cat_cols and num_cols:
        cat_col, num_col = cat_cols[0], num_cols[0]
        agg = df.groupby(cat_col)[num_col].sum().reset_index().sort_values(by=num_col, ascending=False).head(10)
        charts.append({
            "chart_type": "bar",
            "title": f"Top 10 {cat_col.title()} by {num_col.title()}",
            "x_column": cat_col,
            "y_column": num_col,
            "data": agg.to_dict(orient='records'),
            "config": {}
        })

    if num_cols:
        num_col = num_cols[0]
        counts, bins = pd.cut(df[num_col], bins=10, retbins=True)
        hist_df = pd.DataFrame({
            "bin": [f"{bins[i]:.1f}-{bins[i+1]:.1f}" for i in range(len(bins)-1)], 
            "count": counts.value_counts(sort=False).values
        })
        charts.append({
            "chart_type": "histogram",
            "title": f"Distribution of {num_col.title()}",
            "x_column": "bin",
            "y_column": "count",
            "data": hist_df.to_dict(orient='records'),
            "config": {}
        })

    return charts
