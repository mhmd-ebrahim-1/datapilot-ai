import pandas as pd
from typing import Dict, Any, List, Optional

def compute_kpis(df: pd.DataFrame, dataset_type: str = "General") -> List[Dict[str, Any]]:
    kpis = []
    if df.empty:
        return kpis
        
    cols = [str(c).lower() for c in df.columns]

    def get_col(keywords):
        for kw in keywords:
            for i, c in enumerate(cols):
                if kw in c:
                    return df.columns[i]
        return None

    dtype_lower = (dataset_type or "General").lower()

    if 'sale' in dtype_lower:
        rev_col = get_col(['revenue', 'sales', 'total_amount', 'amount'])
        cost_col = get_col(['cost', 'expense'])
        qty_col = get_col(['quantity', 'qty', 'units_sold'])
        
        if rev_col:
            total_rev = float(pd.to_numeric(df[rev_col], errors='coerce').sum())
            kpis.append({"name": "Total Revenue", "value": round(total_rev, 2), "formatted_value": f"${total_rev:,.2f}", "description": "Total gross sales revenue", "icon": "trending-up"})
            
            if cost_col:
                total_cost = float(pd.to_numeric(df[cost_col], errors='coerce').sum())
                profit = total_rev - total_cost
                margin = (profit / total_rev * 100) if total_rev else 0
                kpis.append({"name": "Total Profit", "value": round(profit, 2), "formatted_value": f"${profit:,.2f}", "description": "Gross profit generated", "icon": "dollar-sign"})
                kpis.append({"name": "Profit Margin", "value": round(margin, 1), "formatted_value": f"{margin:.1f}%", "description": "Overall profit margin", "icon": "percent"})
                
            avg_order = total_rev / max(len(df), 1)
            kpis.append({"name": "Avg Order Value", "value": round(avg_order, 2), "formatted_value": f"${avg_order:,.2f}", "description": "Average transaction value", "icon": "credit-card"})
            
        if qty_col:
            total_qty = int(pd.to_numeric(df[qty_col], errors='coerce').sum())
            kpis.append({"name": "Units Sold", "value": total_qty, "formatted_value": f"{total_qty:,}", "description": "Total volume of items sold", "icon": "package"})

        kpis.append({"name": "Total Orders", "value": len(df), "formatted_value": f"{len(df):,}", "description": "Number of customer transactions", "icon": "shopping-cart"})
    
    elif 'market' in dtype_lower:
        spend_col = get_col(['spend', 'cost', 'budget'])
        conv_col = get_col(['conversion', 'leads', 'signups'])
        click_col = get_col(['clicks'])
        imp_col = get_col(['impressions', 'views'])
        
        if spend_col:
            total_spend = float(pd.to_numeric(df[spend_col], errors='coerce').sum())
            kpis.append({"name": "Total Ad Spend", "value": round(total_spend, 2), "formatted_value": f"${total_spend:,.2f}", "description": "Total media expenditure", "icon": "dollar-sign"})
        if conv_col:
            total_conv = float(pd.to_numeric(df[conv_col], errors='coerce').sum())
            kpis.append({"name": "Total Conversions", "value": round(total_conv, 0), "formatted_value": f"{total_conv:,.0f}", "description": "Total qualified actions", "icon": "target"})
        if click_col and imp_col:
            total_clicks = float(pd.to_numeric(df[click_col], errors='coerce').sum())
            total_imps = float(pd.to_numeric(df[imp_col], errors='coerce').sum())
            ctr = (total_clicks / max(total_imps, 1)) * 100
            kpis.append({"name": "Click-Through Rate", "value": round(ctr, 2), "formatted_value": f"{ctr:.2f}%", "description": "Engagement rate (CTR)", "icon": "mouse-pointer"})

    elif 'finan' in dtype_lower:
        amt_col = get_col(['amount', 'value', 'balance'])
        type_col = get_col(['type', 'transaction_type'])
        if amt_col:
            num_amt = pd.to_numeric(df[amt_col], errors='coerce').fillna(0)
            if type_col:
                rev_mask = df[type_col].astype(str).str.lower().str.contains('rev|income|credit')
                exp_mask = df[type_col].astype(str).str.lower().str.contains('exp|debit|cost')
                inc = float(num_amt[rev_mask].sum()) if rev_mask.any() else float(num_amt.sum())
                exp = float(num_amt[exp_mask].sum()) if exp_mask.any() else 0.0
                kpis.append({"name": "Total Income", "value": round(inc, 2), "formatted_value": f"${inc:,.2f}", "description": "Inflow receipts", "icon": "trending-up"})
                kpis.append({"name": "Total Expenses", "value": round(exp, 2), "formatted_value": f"${exp:,.2f}", "description": "Outflow costs", "icon": "trending-down"})
                net = inc - exp
                kpis.append({"name": "Net Income", "value": round(net, 2), "formatted_value": f"${net:,.2f}", "description": "Bottom-line net balance", "icon": "dollar-sign"})
            else:
                total_val = float(num_amt.sum())
                kpis.append({"name": "Total Cash Flow", "value": round(total_val, 2), "formatted_value": f"${total_val:,.2f}", "description": "Sum of monetary values", "icon": "dollar-sign"})

    elif 'hr' in dtype_lower:
        sal_col = get_col(['salary', 'compensation', 'wage'])
        dept_col = get_col(['department', 'dept', 'team'])
        perf_col = get_col(['performance', 'rating', 'score'])
        
        kpis.append({"name": "Total Headcount", "value": len(df), "formatted_value": f"{len(df):,}", "description": "Total recorded workforce", "icon": "users"})
        if sal_col:
            avg_sal = float(pd.to_numeric(df[sal_col], errors='coerce').mean())
            kpis.append({"name": "Average Salary", "value": round(avg_sal, 2), "formatted_value": f"${avg_sal:,.2f}", "description": "Mean employee compensation", "icon": "dollar-sign"})
        if dept_col:
            depts = int(df[dept_col].nunique())
            kpis.append({"name": "Departments", "value": depts, "formatted_value": f"{depts}", "description": "Active functional units", "icon": "briefcase"})
        if perf_col:
            avg_perf = float(pd.to_numeric(df[perf_col], errors='coerce').mean())
            kpis.append({"name": "Avg Performance", "value": round(avg_perf, 2), "formatted_value": f"{avg_perf:.1f} / 5.0", "description": "Mean review score", "icon": "award"})

    # Always include Record Count for completeness
    kpis.append({"name": "Total Records", "value": len(df), "formatted_value": f"{len(df):,}", "description": "Total profiled rows", "icon": "database"})
    return kpis

calculate_kpis = compute_kpis
