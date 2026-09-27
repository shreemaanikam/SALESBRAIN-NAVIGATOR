"""
SalesBrain Navigator — Feature Engineering & Target Design

Target: Transaction-level Profit Prediction
Use case: Given transaction attributes (category, segment, region, quantity,
          discount, sales, shipping_cost), estimate the expected profit.

Note: 'sales' is included as a predictor. This means the model estimates
profit for a transaction where the sale amount is already known — it is NOT
a fully prospective pre-order forecast.

Excluded columns and rationale:
- profit: TARGET variable
- Profit_Margin: derived from profit (target leakage)
- order_id: identifier, not a predictor
- product_id: high cardinality identifier
- customer_name: PII, high cardinality
- product_name: high cardinality, captured by category/sub_category
- order_date, ship_date: used for train/test split, not direct features
- year, Month, Month_Name, Quarter, Day, Day_Name: temporal leak for
  chronological evaluation (the model should generalize to future periods
  without knowing the exact date)
- Shipping_Days: post-outcome — not known at order time
- state: high cardinality, captured by region/market/country
- country: high cardinality, captured by market/region
- order_priority: business metadata, not a strong predictor

Included features:
CATEGORICAL: category, sub_category, segment, region, market, ship_mode
NUMERIC: sales, quantity, discount, shipping_cost
"""

import pandas as pd
import numpy as np
from typing import Tuple, List, Dict, Any

# --- Feature Lists ---
TARGET = "profit"

CATEGORICAL_FEATURES = [
    "category",
    "sub_category",
    "segment",
    "region",
    "market",
    "ship_mode",
]

NUMERIC_FEATURES = [
    "sales",
    "quantity",
    "discount",
    "shipping_cost",
]

ALL_FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES

# Columns that must NEVER be used as features (leakage / identifiers)
EXCLUDED_COLUMNS = [
    "profit",           # target
    "Profit_Margin",    # derived from target
    "order_id",         # identifier
    "product_id",       # high-cardinality identifier
    "customer_name",    # PII
    "product_name",     # high cardinality
    "order_date",       # used for split only
    "ship_date",        # used for split only
    "year",             # temporal info — used for split
    "Month",
    "Month_Name",
    "Quarter",
    "Day",
    "Day_Name",
    "Shipping_Days",    # post-outcome
    "state",            # high cardinality
    "country",          # high cardinality
    "order_priority",   # weak predictor
]


def validate_no_leakage(feature_list: List[str]) -> None:
    """Ensure no excluded column appears in the feature list."""
    leaked = set(feature_list) & set(EXCLUDED_COLUMNS)
    if leaked:
        raise ValueError(f"Target leakage detected! These columns must not be features: {leaked}")


def chronological_split(
    df: pd.DataFrame,
    date_col: str = "order_date",
    test_ratio: float = 0.2,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split data chronologically: earlier records for training, later for testing.
    Uses the date_col to sort, then splits by position.
    """
    df_sorted = df.sort_values(date_col).reset_index(drop=True)
    split_idx = int(len(df_sorted) * (1 - test_ratio))
    train = df_sorted.iloc[:split_idx].copy()
    test = df_sorted.iloc[split_idx:].copy()
    return train, test


def prepare_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Extract feature matrix X and target y from a DataFrame.
    Validates no leakage.
    """
    validate_no_leakage(ALL_FEATURES)

    missing_cols = [c for c in ALL_FEATURES + [TARGET] if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    X = df[ALL_FEATURES].copy()
    y = df[TARGET].copy()
    return X, y


def get_feature_report(df: pd.DataFrame) -> Dict[str, Any]:
    """Generate a feature selection report."""
    report = {
        "target": TARGET,
        "use_case": "Transaction-level profit estimation (sales known at prediction time)",
        "total_features": len(ALL_FEATURES),
        "categorical_features": CATEGORICAL_FEATURES,
        "numeric_features": NUMERIC_FEATURES,
        "excluded_columns": EXCLUDED_COLUMNS,
        "feature_stats": {},
    }

    for col in NUMERIC_FEATURES:
        if col in df.columns:
            report["feature_stats"][col] = {
                "mean": float(df[col].mean()),
                "std": float(df[col].std()),
                "min": float(df[col].min()),
                "max": float(df[col].max()),
                "missing": int(df[col].isna().sum()),
            }

    for col in CATEGORICAL_FEATURES:
        if col in df.columns:
            report["feature_stats"][col] = {
                "unique_values": int(df[col].nunique()),
                "top_values": df[col].value_counts().head(5).to_dict(),
                "missing": int(df[col].isna().sum()),
            }

    return report
