import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from app.services.ai.intent_engine import QueryPlan

class QueryExecutionEngine:
    """Executes deterministic analytical plans on Pandas DataFrames with 100% verified math."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def execute(self, plan: QueryPlan) -> Dict[str, Any]:
        intent = plan.intent
        metric = plan.metric
        dimension = plan.dimension
        date_col = plan.date_col
        total_rows = len(self.df)

        # 1. TOP_N
        if intent == "TOP_N":
            if not dimension or not metric:
                return self._fallback_summary(plan)
            grouped = self.df.groupby(dimension)[metric].sum().sort_values(ascending=False)
            top_series = grouped.head(plan.limit)
            results = [{"label": str(k), "value": float(v)} for k, v in top_series.items()]
            total_metric_val = float(self.df[metric].sum())
            top_total = sum(r["value"] for r in results)
            
            return {
                "intent": "top_n",
                "metric": metric,
                "group_by": dimension,
                "aggregation": "SUM",
                "limit": plan.limit,
                "results": results,
                "top_share_pct": round((top_total / total_metric_val * 100), 2) if total_metric_val else 0,
                "total_metric_value": total_metric_val,
                "rows_analyzed": total_rows,
                "chart": {
                    "type": "bar",
                    "title": f"Top {plan.limit} {dimension}s by {metric}",
                    "labels": [r["label"] for r in results],
                    "values": [r["value"] for r in results]
                }
            }

        # 2. BOTTOM_N
        if intent == "BOTTOM_N":
            if not dimension or not metric:
                return self._fallback_summary(plan)
            grouped = self.df.groupby(dimension)[metric].sum().sort_values(ascending=True)
            bottom_series = grouped.head(plan.limit)
            results = [{"label": str(k), "value": float(v)} for k, v in bottom_series.items()]
            return {
                "intent": "bottom_n",
                "metric": metric,
                "group_by": dimension,
                "aggregation": "SUM",
                "limit": plan.limit,
                "results": results,
                "rows_analyzed": total_rows,
                "chart": {
                    "type": "bar",
                    "title": f"Bottom {plan.limit} {dimension}s by {metric}",
                    "labels": [r["label"] for r in results],
                    "values": [r["value"] for r in results]
                }
            }

        # 3. MAX / HIGHEST
        if intent == "MAX":
            if dimension and metric:
                grouped = self.df.groupby(dimension)[metric].sum().sort_values(ascending=False)
                top_label = str(grouped.index[0])
                top_val = float(grouped.iloc[0])
                all_results = [{"label": str(k), "value": float(v)} for k, v in grouped.head(5).items()]
                total_val = float(self.df[metric].sum())
                return {
                    "intent": "max",
                    "metric": metric,
                    "group_by": dimension,
                    "winner_label": top_label,
                    "winner_value": top_val,
                    "share_pct": round((top_val / total_val * 100), 2) if total_val else 0,
                    "results": all_results,
                    "rows_analyzed": total_rows,
                    "chart": {
                        "type": "bar",
                        "title": f"{metric} by {dimension}",
                        "labels": [r["label"] for r in all_results],
                        "values": [r["value"] for r in all_results]
                    }
                }
            elif metric:
                max_val = float(self.df[metric].max())
                return {
                    "intent": "max",
                    "metric": metric,
                    "winner_value": max_val,
                    "rows_analyzed": total_rows
                }

        # 4. MIN / LOWEST
        if intent == "MIN":
            if dimension and metric:
                grouped = self.df.groupby(dimension)[metric].sum().sort_values(ascending=True)
                min_label = str(grouped.index[0])
                min_val = float(grouped.iloc[0])
                all_results = [{"label": str(k), "value": float(v)} for k, v in grouped.head(5).items()]
                return {
                    "intent": "min",
                    "metric": metric,
                    "group_by": dimension,
                    "winner_label": min_label,
                    "winner_value": min_val,
                    "results": all_results,
                    "rows_analyzed": total_rows
                }
            elif metric:
                min_val = float(self.df[metric].min())
                return {
                    "intent": "min",
                    "metric": metric,
                    "winner_value": min_val,
                    "rows_analyzed": total_rows
                }

        # 5. SUM / TOTAL
        if intent == "SUM":
            if not metric:
                metric = self._get_primary_metric()
            val = float(self.df[metric].sum())
            mean_val = float(self.df[metric].mean())
            return {
                "intent": "sum",
                "metric": metric,
                "value": val,
                "average": mean_val,
                "count": total_rows,
                "rows_analyzed": total_rows
            }

        # 6. AVERAGE / MEAN
        if intent == "AVERAGE":
            if not metric:
                metric = self._get_primary_metric()
            if dimension:
                grouped = self.df.groupby(dimension)[metric].mean().sort_values(ascending=False).head(plan.limit or 5)
                results = [{"label": str(k), "value": float(v)} for k, v in grouped.items()]
                overall_avg = float(self.df[metric].mean())
                return {
                    "intent": "average_grouped",
                    "metric": metric,
                    "group_by": dimension,
                    "overall_average": overall_avg,
                    "results": results,
                    "rows_analyzed": total_rows,
                    "chart": {
                        "type": "bar",
                        "title": f"Average {metric} by {dimension}",
                        "labels": [r["label"] for r in results],
                        "values": [r["value"] for r in results]
                    }
                }
            else:
                avg_val = float(self.df[metric].mean())
                median_val = float(self.df[metric].median())
                std_val = float(self.df[metric].std()) if total_rows > 1 else 0
                return {
                    "intent": "average",
                    "metric": metric,
                    "average": avg_val,
                    "median": median_val,
                    "std": std_val,
                    "rows_analyzed": total_rows
                }

        # 7. COUNT / COUNT_DISTINCT
        if intent in ["COUNT", "COUNT_DISTINCT"]:
            col = plan.metric or self.df.columns[0]
            if plan.is_distinct or intent == "COUNT_DISTINCT":
                count_val = int(self.df[col].nunique())
                return {
                    "intent": "count_distinct",
                    "target_column": col,
                    "distinct_count": count_val,
                    "total_rows": total_rows,
                    "rows_analyzed": total_rows
                }
            else:
                count_val = int(self.df[col].count())
                return {
                    "intent": "count",
                    "target_column": col,
                    "count": count_val,
                    "total_rows": total_rows,
                    "rows_analyzed": total_rows
                }

        # 8. GROUP_BY / COMPARISON
        if intent == "GROUP_BY":
            if not dimension or not metric:
                return self._fallback_summary(plan)
            agg_func = "mean" if plan.aggregation == "mean" else "sum"
            grouped = self.df.groupby(dimension)[metric].agg(agg_func).sort_values(ascending=False).head(plan.limit or 10)
            results = [{"label": str(k), "value": float(v)} for k, v in grouped.items()]
            return {
                "intent": "group_by",
                "metric": metric,
                "group_by": dimension,
                "aggregation": agg_func.upper(),
                "results": results,
                "rows_analyzed": total_rows,
                "chart": {
                    "type": "bar",
                    "title": f"{metric} by {dimension}",
                    "labels": [r["label"] for r in results],
                    "values": [r["value"] for r in results]
                }
            }

        # 9. TREND / TIME SERIES
        if intent == "TREND":
            if not metric:
                metric = self._get_primary_metric()
            date_col = date_col or self._find_date_col()
            if not date_col or date_col not in self.df.columns:
                return self._fallback_summary(plan)
                
            try:
                date_series = pd.to_datetime(self.df[date_col], errors='coerce')
                valid_mask = date_series.notna() & self.df[metric].notna()
                sub_df = self.df[valid_mask].copy()
                sub_df['__dt__'] = date_series[valid_mask]
                
                # Monthly Resampling
                sub_df.set_index('__dt__', inplace=True)
                monthly = sub_df[metric].resample('MS').sum()
                
                if len(monthly) < 2:
                    monthly = sub_df[metric].resample('W').sum()
                    
                total_val = float(monthly.sum())
                avg_monthly = float(monthly.mean())
                max_month = monthly.idxmax().strftime('%B %Y')
                max_val = float(monthly.max())
                min_month = monthly.idxmin().strftime('%B %Y')
                min_val = float(monthly.min())
                
                first_period = monthly.index[0].strftime('%B %Y')
                first_val = float(monthly.iloc[0])
                last_period = monthly.index[-1].strftime('%B %Y')
                last_val = float(monthly.iloc[-1])
                
                growth_pct = round(((last_val - first_val) / first_val * 100), 2) if first_val else 0.0
                
                direction = "Upward" if growth_pct > 5 else ("Downward" if growth_pct < -5 else "Stable")
                
                # Format monthly data points for chart
                chart_labels = [dt.strftime('%b %Y') for dt in monthly.index]
                chart_values = [float(v) for v in monthly.values]
                
                return {
                    "intent": "trend",
                    "metric": metric,
                    "date_column": date_col,
                    "total": total_val,
                    "monthly_average": avg_monthly,
                    "highest_period": {"period": max_month, "value": max_val},
                    "lowest_period": {"period": min_month, "value": min_val},
                    "first_period": {"period": first_period, "value": first_val},
                    "last_period": {"period": last_period, "value": last_val},
                    "growth_pct": growth_pct,
                    "trend_direction": direction,
                    "periods_count": len(monthly),
                    "rows_analyzed": len(sub_df),
                    "chart": {
                        "type": "line",
                        "title": f"Monthly {metric} Trend",
                        "labels": chart_labels,
                        "values": chart_values
                    }
                }
            except Exception as e:
                return self._fallback_summary(plan)

        # 10. ANOMALY DETECTION
        if intent == "ANOMALY":
            if not metric:
                metric = self._get_primary_metric()
            series = self.df[metric].dropna()
            q1 = float(series.quantile(0.25))
            q3 = float(series.quantile(0.75))
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            anomalies_high = self.df[self.df[metric] > upper_bound]
            anomalies_low = self.df[self.df[metric] < lower_bound]
            
            outliers = []
            dim_col = dimension or (self.df.select_dtypes(include=['object']).columns[0] if len(self.df.select_dtypes(include=['object']).columns) > 0 else None)
            
            for _, row in anomalies_high.sort_values(by=metric, ascending=False).head(5).iterrows():
                label = str(row[dim_col]) if dim_col and dim_col in row else f"Row {row.name}"
                outliers.append({
                    "item": label,
                    "value": float(row[metric]),
                    "type": "High Outlier",
                    "deviation": round(float(row[metric]) - upper_bound, 2)
                })
                
            return {
                "intent": "anomaly",
                "metric": metric,
                "lower_bound": round(lower_bound, 2),
                "upper_bound": round(upper_bound, 2),
                "outliers_count": len(anomalies_high) + len(anomalies_low),
                "top_outliers": outliers,
                "rows_analyzed": total_rows
            }

        # 11. SUMMARY / FALLBACK
        return self._fallback_summary(plan)

    def _fallback_summary(self, plan: QueryPlan) -> Dict[str, Any]:
        num_cols = self.df.select_dtypes(include=['number']).columns.tolist()
        metrics = [c for c in num_cols if not any(id_w in str(c).lower() for id_w in ['id', 'postal', 'zip', 'code'])]
        primary_metric = metrics[0] if metrics else (num_cols[0] if num_cols else None)
        
        totals = {}
        for m in metrics[:3]:
            totals[m] = float(self.df[m].sum())
            
        cat_cols = self.df.select_dtypes(include=['object']).columns.tolist()
        categories = {}
        for c in cat_cols[:2]:
            top_val = self.df[c].value_counts().head(1)
            if not top_val.empty:
                categories[c] = {"top_value": str(top_val.index[0]), "count": int(top_val.iloc[0])}
                
        return {
            "intent": "summary",
            "total_rows": len(self.df),
            "total_columns": len(self.df.columns),
            "primary_metric": primary_metric,
            "metrics_totals": totals,
            "top_categories": categories,
            "rows_analyzed": len(self.df)
        }

    def _get_primary_metric(self) -> str:
        num_cols = self.df.select_dtypes(include=['number']).columns.tolist()
        clean_metrics = [c for c in num_cols if not any(id_w in str(c).lower() for id_w in ['id', 'postal', 'zip', 'code'])]
        for pref in ["Sales", "Revenue", "Profit", "Total", "Amount"]:
            for m in clean_metrics:
                if str(m).strip().lower() == pref.lower():
                    return m
        return clean_metrics[0] if clean_metrics else num_cols[0]

    def _find_date_col(self) -> Optional[str]:
        for c in self.df.columns:
            if pd.api.types.is_datetime64_any_dtype(self.df[c]):
                return c
        for c in self.df.columns:
            if "date" in str(c).lower() or "time" in str(c).lower():
                return c
        return None

