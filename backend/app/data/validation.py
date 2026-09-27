import pandas as pd
import numpy as np
from backend.app.data.schema import EXPECTED_COLUMNS, NUMERIC_COLUMNS, DATE_COLUMNS

def validate_columns(df: pd.DataFrame):
    missing = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

def validate_dtypes(df: pd.DataFrame):
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                df[col] = pd.to_numeric(df[col], errors='coerce')
    for col in DATE_COLUMNS:
        if col in df.columns:
            if not pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = pd.to_datetime(df[col], errors='coerce')

def validate_data_quality(df: pd.DataFrame) -> dict:
    return {
        "row_count": len(df),
        "column_count": len(df.columns),
        "missing_counts": df.isnull().sum().to_dict(),
        "duplicate_count": df.duplicated().sum(),
        "date_range": {
            "start": df['order_date'].min().isoformat() if not df['order_date'].isnull().all() else None,
            "end": df['order_date'].max().isoformat() if not df['order_date'].isnull().all() else None
        },
        "numeric_stats": df[NUMERIC_COLUMNS].describe().to_dict(),
        "inf_count": df.isin([np.inf, -np.inf]).sum().to_dict(),
        "null_count": df.isnull().sum().to_dict()
    }

def clean_for_json(value):
    if pd.isna(value):
        return None
    if isinstance(value, (np.floating, float)) and np.isinf(value):
        return None
    if isinstance(value, (np.integer, int)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        return float(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    return str(value)
