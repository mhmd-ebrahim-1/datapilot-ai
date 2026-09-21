import pytest
import pandas as pd
import numpy as np
from app.services.cleaning.cleaner import clean_dataset

def test_clean_dataset_pipeline():
    df = pd.DataFrame({
        " Product Name ": ["  Laptop ", "Phone", "Phone", "Tablet  "],
        "Revenue ": ["100.5", "200.0", "200.0", "N/A"],
        "Quantity": [1, 2, 2, 3]
    })
    
    result = clean_dataset(df)
    cleaned = result["cleaned_df"]
    changes = result["changes_log"]
    
    # 1. Check normalized column names
    assert "product_name" in cleaned.columns
    assert "revenue" in cleaned.columns
    
    # 2. Check whitespace trimmed
    assert cleaned["product_name"].iloc[0] == "Laptop"
    
    # 3. Check duplicate removal (Phone row was exact duplicate)
    assert len(cleaned) == 3
    assert result["rows_before"] == 4
    assert result["rows_after"] == 3
    
    # 4. Check changes log
    assert len(changes) > 0

