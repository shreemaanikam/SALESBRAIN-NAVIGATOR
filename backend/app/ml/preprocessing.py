"""
SalesBrain Navigator — ML Preprocessing Pipeline

Builds scikit-learn Pipeline + ColumnTransformer for the profit prediction task.
"""

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

from backend.app.ml.features import CATEGORICAL_FEATURES, NUMERIC_FEATURES


def build_preprocessor() -> ColumnTransformer:
    """
    Build a ColumnTransformer that handles numeric and categorical features.

    Numeric: impute with median, then standard scale
    Categorical: impute with 'missing', then one-hot encode
    """
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, NUMERIC_FEATURES),
            ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )

    return preprocessor


def build_pipeline(estimator) -> Pipeline:
    """
    Build a complete pipeline: preprocessing + estimator.
    The estimator is NOT fit here — call pipeline.fit(X_train, y_train).
    """
    preprocessor = build_preprocessor()
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", estimator),
    ])
    return pipeline


def get_feature_names(fitted_preprocessor: ColumnTransformer):
    """Extract feature names from a fitted ColumnTransformer."""
    feature_names = []

    # Numeric features keep their names
    feature_names.extend(NUMERIC_FEATURES)

    # Categorical features get one-hot encoded names
    try:
        cat_encoder = fitted_preprocessor.named_transformers_["cat"]["encoder"]
        cat_features = cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES)
        feature_names.extend(cat_features.tolist())
    except Exception:
        pass

    return feature_names
