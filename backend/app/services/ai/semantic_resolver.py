import re
import pandas as pd
from typing import Dict, List, Optional, Tuple, Set

IDENTIFIER_PATTERNS = [
    r'id$', r'id\b', r'^id', r'_id$', r'code$', r'postal', r'zip', r'key$', r'uuid',
    r'index', r'row\s*id', r'order\s*id', r'customer\s*id', r'product\s*id',
    r'transaction\s*id', r'account\s*id', r'invoice\s*id'
]

METRIC_SYNONYMS = {
    "sales": ["sales", "revenue", "income", "turnover", "gross sales", "total sales"],
    "profit": ["profit", "net profit", "margin", "earnings", "net income", "gain", "operating income"],
    "cost": ["cost", "cogs", "expense", "expenses", "spend", "spending", "total cost"],
    "quantity": ["quantity", "units", "volume", "qty", "items sold", "order quantity"],
    "discount": ["discount", "discount rate", "rebate", "markdown"],
    "price": ["price", "unit price", "unit cost", "rate"],
    "salary": ["salary", "compensation", "wage", "pay"],
    "score": ["score", "rating", "satisfaction", "quality score"]
}

DIMENSION_SYNONYMS = {
    "product": ["product", "product name", "product_name", "item", "item name", "sku", "goods", "article"],
    "category": ["category", "dept", "department", "category name"],
    "sub-category": ["sub-category", "subcategory", "sub_category", "sub category", "sub dept"],
    "region": ["region", "territory", "zone", "area", "district"],
    "state": ["state", "province", "governorate", "county"],
    "city": ["city", "town", "metro", "municipality"],
    "country": ["country", "nation"],
    "segment": ["segment", "customer segment", "market segment", "tier"],
    "customer": ["customer", "customer name", "customer_name", "client", "buyer", "account name"],
    "ship mode": ["ship mode", "shipping mode", "delivery method", "shipping"],
    "department": ["department", "dept", "division", "team"],
    "channel": ["channel", "marketing channel", "source", "medium"]
}

class SemanticResolver:
    """Classifies dataset columns and maps natural language query terms to real dataset columns."""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.columns = list(df.columns)
        self.column_map_lower = {str(col).strip().lower(): col for col in self.columns}
        
        self.identifiers = self._detect_identifiers()
        self.dates = self._detect_dates()
        self.metrics = self._detect_metrics()
        self.dimensions = self._detect_dimensions()

    def _detect_identifiers(self) -> Set[str]:
        identifiers = set()
        for col in self.columns:
            col_lower = str(col).strip().lower()
            # 1. Regex name match
            if any(re.search(pat, col_lower) for pat in IDENTIFIER_PATTERNS):
                identifiers.add(col)
                continue
                
            # 2. Check if integer sequence / high cardinality unique IDs
            if pd.api.types.is_numeric_dtype(self.df[col]):
                # If unique values == total rows or close to total rows and values look like serial integers
                nunique = self.df[col].nunique()
                total = len(self.df)
                if total > 50 and nunique >= total * 0.95 and col_lower.endswith(('num', 'no', '#')):
                    identifiers.add(col)
        return identifiers

    def _detect_dates(self) -> List[str]:
        date_cols = []
        for col in self.columns:
            if pd.api.types.is_datetime64_any_dtype(self.df[col]):
                date_cols.append(col)
            elif any(term in str(col).lower() for term in ['date', 'time', 'year', 'month', 'day', 'timestamp', 'created_at']):
                date_cols.append(col)
        return date_cols

    def _detect_metrics(self) -> List[str]:
        """Numeric columns that are genuine business metrics (excluding identifiers)."""
        metrics = []
        for col in self.columns:
            if col in self.identifiers or col in self.dates:
                continue
            if pd.api.types.is_numeric_dtype(self.df[col]):
                metrics.append(col)
        return metrics

    def _detect_dimensions(self) -> List[str]:
        """Categorical / grouping columns (excluding raw IDs and numeric metrics)."""
        dims = []
        for col in self.columns:
            if col in self.dates or col in self.identifiers or col in self.metrics:
                continue
            if not pd.api.types.is_numeric_dtype(self.df[col]):
                dims.append(col)
        return dims

    def resolve_metric(self, query: str) -> Optional[str]:
        """Resolve query term to the most appropriate business metric column."""
        q = query.lower()
        
        # 1. Exact or synonym match in query
        for canonical, synonyms in METRIC_SYNONYMS.items():
            for syn in synonyms:
                if re.search(rf'\b{re.escape(syn)}\b', q):
                    # Find matching column in dataset
                    for col in self.metrics:
                        col_lower = str(col).lower()
                        if canonical in col_lower or syn in col_lower:
                            return col
                            
        # 2. Match exact metric column name in query
        for col in self.metrics:
            col_clean = str(col).lower()
            if col_clean in q:
                return col
                
        # 3. Default fallback to primary revenue / sales / first numeric metric
        for preferred in ["Sales", "Revenue", "Total Revenue", "Amount", "Profit", "Total"]:
            for col in self.metrics:
                if str(col).strip().lower() == preferred.lower():
                    return col
                    
        return self.metrics[0] if self.metrics else None

    def resolve_dimension(self, query: str) -> Optional[str]:
        """Resolve query term to the most appropriate dimension/categorical column."""
        q = query.lower()
        
        # 1. Look for synonym matches in query
        for canonical, synonyms in DIMENSION_SYNONYMS.items():
            for syn in synonyms:
                if re.search(rf'\b{re.escape(syn)}\b', q):
                    for col in self.dimensions:
                        col_lower = str(col).lower()
                        if canonical == "sub-category" and ("sub" in col_lower and "cat" in col_lower):
                            return col
                        if canonical in col_lower or syn in col_lower:
                            return col
                            
        # 2. Check exact column name occurrence in query
        for col in self.dimensions:
            col_clean = str(col).lower()
            if col_clean in q:
                return col
                
        # 3. If query mentions "highest / top / by / across", inspect word tokens
        for col in self.dimensions:
            words = [w for w in str(col).lower().split() if len(w) > 3]
            if any(w in q for w in words):
                return col
                
        # 4. Default fallback: choose highest cardinality business dimension (e.g. Category, Product Name, Region)
        for preferred in ["Product Name", "Product", "Category", "Sub-Category", "Region", "State", "Segment"]:
            for col in self.dimensions:
                if str(col).strip().lower() == preferred.lower():
                    return col
                    
        return self.dimensions[0] if self.dimensions else None

    def resolve_date(self, query: str = "") -> Optional[str]:
        """Find the primary datetime column for trend / time series."""
        q = query.lower()
        if self.dates:
            # Look for order date / transaction date
            for preferred in ["Order Date", "Date", "Transaction Date", "Ship Date", "created_at"]:
                for col in self.dates:
                    if str(col).strip().lower() == preferred.lower():
                        return col
            for col in self.dates:
                if "order" in str(col).lower() or "trans" in str(col).lower():
                    return col
            return self.dates[0]
            
        # Try finding string column with 'date'
        for col in self.columns:
            if "date" in str(col).lower() or "time" in str(col).lower():
                return col
        return None

    def resolve_count_target(self, query: str) -> Tuple[str, bool]:
        """Returns (column_name, is_distinct) for COUNT operations."""
        q = query.lower()
        # "how many customers" -> Customer ID, distinct
        if any(term in q for term in ["customer", "clients", "buyers"]):
            for col in self.columns:
                if "customer id" in str(col).lower() or "customer_id" in str(col).lower() or "customer name" in str(col).lower():
                    return col, True
        # "how many orders" -> Order ID, distinct
        if any(term in q for term in ["order", "transactions", "invoices"]):
            for col in self.columns:
                if "order id" in str(col).lower() or "order_id" in str(col).lower() or "order" in str(col).lower():
                    return col, True
        # "how many products" -> Product Name / Product ID, distinct
        if any(term in q for term in ["product", "items", "skus"]):
            for col in self.columns:
                if "product name" in str(col).lower() or "product id" in str(col).lower():
                    return col, True
        # "how many rows / records"
        return self.columns[0], False
