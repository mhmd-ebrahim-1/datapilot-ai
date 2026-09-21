from typing import Dict, Any, List

def format_number(val: float, is_currency: bool = False, is_pct: bool = False) -> str:
    """Format numeric values cleanly with currency symbols or percentages."""
    if is_pct:
        return f"{val:+.2f}%" if val != 0 else "0.00%"
    if is_currency:
        if abs(val) >= 1_000_000:
            return f"${val:,.2f}"
        return f"${val:,.2f}"
    if isinstance(val, int) or (isinstance(val, float) and val.is_integer()):
        return f"{int(val):,}"
    return f"{val:,.2f}"

def is_currency_metric(metric_name: str) -> bool:
    name = str(metric_name).lower()
    return any(term in name for term in ["sales", "revenue", "profit", "cost", "income", "price", "spend", "salary", "budget", "amount"])

def is_percentage_metric(metric_name: str) -> bool:
    name = str(metric_name).lower()
    return any(term in name for term in ["discount", "rate", "pct", "percentage", "margin_rate"])

class DeterministicExplainer:
    """Generates crystal-clear, verified analytical explanations directly from deterministic query results."""

    @classmethod
    def explain(cls, result: Dict[str, Any], dataset_name: str = "Dataset") -> str:
        intent = result.get("intent", "summary")
        metric = result.get("metric", "Metric")
        is_curr = is_currency_metric(metric)
        is_pct = is_percentage_metric(metric)
        rows_analyzed = result.get("rows_analyzed", 0)

        # 1. TOP_N
        if intent == "top_n":
            dim = result.get("group_by", "Item")
            limit = result.get("limit", 5)
            items = result.get("results", [])
            top_share = result.get("top_share_pct", 0)
            
            lines = [f"### Top {limit} {dim}s by {metric}\n"]
            for i, item in enumerate(items, 1):
                val_str = format_number(item["value"], is_currency=is_curr, is_pct=is_pct)
                lines.append(f"{i}. **{item['label']}** - {val_str}")
                
            if top_share > 0:
                lines.append(f"\n> **Insight:** The top {limit} {dim.lower()}s account for **{top_share:.1f}%** of total {metric.lower()}.\n")
                
            lines.append("---")
            lines.append(f"**Verification Details:** Analyzed {rows_analyzed:,} records from *{dataset_name}* via deterministic aggregation.")
            return "\n".join(lines)

        # 2. BOTTOM_N
        if intent == "bottom_n":
            dim = result.get("group_by", "Item")
            limit = result.get("limit", 5)
            items = result.get("results", [])
            
            lines = [f"### Lowest {limit} {dim}s by {metric}\n"]
            for i, item in enumerate(items, 1):
                val_str = format_number(item["value"], is_currency=is_curr, is_pct=is_pct)
                lines.append(f"{i}. **{item['label']}** - {val_str}")
                
            lines.append("\n---")
            lines.append(f"**Verification Details:** Analyzed {rows_analyzed:,} records from *{dataset_name}* via deterministic aggregation.")
            return "\n".join(lines)

        # 3. MAX / HIGHEST
        if intent == "max":
            dim = result.get("group_by")
            winner_label = result.get("winner_label")
            winner_val = result.get("winner_value", 0)
            val_str = format_number(winner_val, is_currency=is_curr, is_pct=is_pct)
            share_pct = result.get("share_pct", 0)
            other_items = result.get("results", [])
            
            if dim and winner_label:
                lines = [
                    f"### Highest {metric} by {dim}\n",
                    f"**{winner_label}** generated the highest {metric.lower()} with **{val_str}**" + (f" ({share_pct:.1f}% of total {metric.lower()})." if share_pct else "."),
                    "\n**Complete Ranking:**"
                ]
                for i, it in enumerate(other_items, 1):
                    v_str = format_number(it["value"], is_currency=is_curr, is_pct=is_pct)
                    lines.append(f"{i}. **{it['label']}**: {v_str}")
                lines.append("\n---")
                lines.append(f"**Verification Details:** Analyzed {rows_analyzed:,} records from *{dataset_name}*.")
                return "\n".join(lines)
            else:
                return f"### Maximum {metric}\n\nThe highest single {metric.lower()} recorded is **{val_str}** across {rows_analyzed:,} rows."

        # 4. MIN / LOWEST
        if intent == "min":
            dim = result.get("group_by")
            winner_label = result.get("winner_label")
            winner_val = result.get("winner_value", 0)
            val_str = format_number(winner_val, is_currency=is_curr, is_pct=is_pct)
            other_items = result.get("results", [])
            
            if dim and winner_label:
                lines = [
                    f"### Lowest {metric} by {dim}\n",
                    f"**{winner_label}** recorded the lowest {metric.lower()} at **{val_str}**.",
                    "\n**Breakdown:**"
                ]
                for i, it in enumerate(other_items, 1):
                    v_str = format_number(it["value"], is_currency=is_curr, is_pct=is_pct)
                    lines.append(f"{i}. **{it['label']}**: {v_str}")
                lines.append("\n---")
                lines.append(f"**Verification Details:** Analyzed {rows_analyzed:,} records from *{dataset_name}*.")
                return "\n".join(lines)
            else:
                return f"### Minimum {metric}\n\nThe minimum {metric.lower()} recorded is **{val_str}** across {rows_analyzed:,} rows."

        # 5. SUM / TOTAL
        if intent == "sum":
            val = result.get("value", 0)
            val_str = format_number(val, is_currency=is_curr, is_pct=is_pct)
            avg_val = result.get("average", 0)
            avg_str = format_number(avg_val, is_currency=is_curr, is_pct=is_pct)
            count = result.get("count", rows_analyzed)
            
            lines = [
                f"### Total {metric}\n",
                f"- **Total {metric}:** {val_str}",
                f"- **Average per Record:** {avg_str}",
                f"- **Total Transactions Analyzed:** {count:,}",
                "\n---",
                f"**Verification Details:** Calculated directly via `SUM({metric})` over all {rows_analyzed:,} rows in *{dataset_name}*."
            ]
            return "\n".join(lines)

        # 6. AVERAGE
        if intent == "average":
            avg = result.get("average", 0)
            avg_str = format_number(avg, is_currency=is_curr, is_pct=is_pct)
            med = result.get("median", 0)
            med_str = format_number(med, is_currency=is_curr, is_pct=is_pct)
            
            lines = [
                f"### Average {metric}\n",
                f"- **Mean (Average):** {avg_str}",
                f"- **Median:** {med_str}",
                "\n---",
                f"**Verification Details:** Calculated directly across all {rows_analyzed:,} records in *{dataset_name}*."
            ]
            return "\n".join(lines)

        if intent == "average_grouped":
            dim = result.get("group_by", "Category")
            overall = result.get("overall_average", 0)
            overall_str = format_number(overall, is_currency=is_curr, is_pct=is_pct)
            items = result.get("results", [])
            
            lines = [
                f"### Average {metric} by {dim}\n",
                f"Overall dataset average is **{overall_str}**.\n"
            ]
            for i, item in enumerate(items, 1):
                v_str = format_number(item["value"], is_currency=is_curr, is_pct=is_pct)
                lines.append(f"{i}. **{item['label']}** - {v_str}")
            lines.append("\n---")
            lines.append(f"**Verification Details:** Grouped mean across {rows_analyzed:,} rows in *{dataset_name}*.")
            return "\n".join(lines)

        # 7. COUNT / COUNT DISTINCT
        if intent in ["count", "count_distinct"]:
            target = result.get("target_column", "records")
            if intent == "count_distinct":
                distinct_count = result.get("distinct_count", 0)
                return (
                    f"### Unique {target} Count\n\n"
                    f"There are **{distinct_count:,}** unique {target.lower()} entries recorded across {rows_analyzed:,} dataset transactions."
                )
            else:
                total_count = result.get("count", rows_analyzed)
                return (
                    f"### Total Record Count\n\n"
                    f"There are **{total_count:,}** total rows/records in the dataset."
                )

        # 8. GROUP_BY
        if intent == "group_by":
            dim = result.get("group_by", "Dimension")
            agg = result.get("aggregation", "SUM")
            items = result.get("results", [])
            lines = [f"### {metric} Breakdown by {dim} ({agg})\n"]
            for i, it in enumerate(items, 1):
                v_str = format_number(it["value"], is_currency=is_curr, is_pct=is_pct)
                lines.append(f"{i}. **{it['label']}** - {v_str}")
            lines.append("\n---")
            lines.append(f"**Verification Details:** Aggregated across {rows_analyzed:,} rows in *{dataset_name}*.")
            return "\n".join(lines)

        # 9. TREND
        if intent == "trend":
            total = result.get("total", 0)
            total_str = format_number(total, is_currency=is_curr, is_pct=is_pct)
            monthly_avg = result.get("monthly_average", 0)
            monthly_avg_str = format_number(monthly_avg, is_currency=is_curr, is_pct=is_pct)
            
            high = result.get("highest_period", {})
            low = result.get("lowest_period", {})
            first = result.get("first_period", {})
            last = result.get("last_period", {})
            growth = result.get("growth_pct", 0)
            dir_str = result.get("trend_direction", "Stable")
            periods = result.get("periods_count", 0)
            
            high_val_str = format_number(high.get("value", 0), is_currency=is_curr, is_pct=is_pct)
            low_val_str = format_number(low.get("value", 0), is_currency=is_curr, is_pct=is_pct)
            first_val_str = format_number(first.get("value", 0), is_currency=is_curr, is_pct=is_pct)
            last_val_str = format_number(last.get("value", 0), is_currency=is_curr, is_pct=is_pct)
            
            lines = [
                f"### {metric} Monthly Trend & Performance\n",
                f"- **Total {metric}:** {total_str}",
                f"- **Average Monthly {metric}:** {monthly_avg_str}",
                f"- **Highest Month:** {high.get('period', 'N/A')} ({high_val_str})",
                f"- **Lowest Month:** {low.get('period', 'N/A')} ({low_val_str})",
                f"- **Initial vs Final Period:** {first.get('period')} ({first_val_str}) -> {last.get('period')} ({last_val_str})",
                f"- **Overall Growth:** **{growth:+.1f}%** ({dir_str} trajectory across {periods} months).",
                "\n---",
                f"**Verification Details:** Monthly resampled time-series on {rows_analyzed:,} records in *{dataset_name}*."
            ]
            return "\n".join(lines)

        # 10. ANOMALY
        if intent == "anomaly":
            cnt = result.get("outliers_count", 0)
            lower = format_number(result.get("lower_bound", 0), is_currency=is_curr)
            upper = format_number(result.get("upper_bound", 0), is_currency=is_curr)
            outliers = result.get("top_outliers", [])
            
            lines = [
                f"### {metric} Anomaly Detection\n",
                f"Detected **{cnt} statistical outliers** outside the expected normal range ({lower} to {upper}).\n",
                "**Top Unusual Transactions:**"
            ]
            for i, o in enumerate(outliers, 1):
                v_str = format_number(o["value"], is_currency=is_curr)
                lines.append(f"{i}. **{o['item']}** - {v_str} (*{o['type']}*)")
            lines.append("\n---")
            lines.append(f"**Verification Details:** Interquartile Range (IQR 1.5x) statistical audit on {rows_analyzed:,} records.")
            return "\n".join(lines)

        # 11. SUMMARY
        rows = result.get("total_rows", 0)
        cols = result.get("total_columns", 0)
        totals = result.get("metrics_totals", {})
        
        lines = [
            f"### Dataset Summary Overview\n",
            f"- **Total Volume:** {rows:,} rows across {cols} columns",
        ]
        for m, v in totals.items():
            is_c = is_currency_metric(m)
            lines.append(f"- **Total {m}:** {format_number(v, is_currency=is_c)}")
        lines.append("\n---")
        lines.append(f"**Verification Details:** Verified schema and record distribution.")
        return "\n".join(lines)
