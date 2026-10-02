"""
SalesBrain Navigator — Prediction Service

Loads the trained ML model and provides prediction capabilities.
"""

import os
import json
import logging
import joblib
import pandas as pd
from typing import Dict, Any, Optional

from backend.app.ml.features import ALL_FEATURES, CATEGORICAL_FEATURES, NUMERIC_FEATURES

logger = logging.getLogger(__name__)


class PredictionService:
    def __init__(self):
        self.model = None
        self.metadata: Dict[str, Any] = {}
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        default_artifacts = os.path.join(base_dir, "ml", "artifacts")
        self.artifacts_dir = os.environ.get("ML_ARTIFACTS_DIR", default_artifacts)
        self._try_load()

    def _try_load(self):
        """Attempt to load model artifacts. Fail gracefully."""
        model_path = os.path.join(self.artifacts_dir, "profit_model.joblib")
        metadata_path = os.path.join(self.artifacts_dir, "model_metadata.json")

        try:
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                logger.info("Loaded ML model from %s", model_path)
            else:
                logger.warning("Model file not found: %s", model_path)

            if os.path.exists(metadata_path):
                with open(metadata_path, "r") as f:
                    self.metadata = json.load(f)
                logger.info("Loaded model metadata")
            else:
                logger.warning("Metadata file not found: %s", metadata_path)
        except Exception as e:
            logger.error("Error loading model artifacts: %s", e)

    def is_ready(self) -> bool:
        return self.model is not None
    def check_compatibility(self, mapping: Dict[str, str]) -> Dict[str, Any]:
        """Check if the uploaded dataset mapping has all required features for this model."""
        if not self.is_ready():
            return {"compatible": False, "reason": "Model not loaded"}
        
        required_features = self.metadata.get("features", ALL_FEATURES)
        missing_features = []
        
        for feat in required_features:
            if feat not in mapping or not mapping[feat]:
                missing_features.append(feat)
                
        if missing_features:
            return {
                "compatible": False,
                "reason": f"Missing required mapped features: {', '.join(missing_features)}",
                "missing_features": missing_features
            }
            
        return {"compatible": True, "reason": "All required features mapped"}

    def predict_batch(self, df: pd.DataFrame, mapping: Dict[str, str]) -> pd.Series:
        """Predict profit for a batch of rows in a DataFrame using the mapping."""
        if not self.is_ready():
            raise RuntimeError("Model not loaded")
            
        compatibility = self.check_compatibility(mapping)
        if not compatibility["compatible"]:
            raise ValueError(f"Dataset incompatible: {compatibility['reason']}")
            
        # Extract features using mapping
        feature_df = pd.DataFrame()
        for feat in ALL_FEATURES:
            col_name = mapping[feat]
            feature_df[feat] = df[col_name]
            
            # Basic validation
            if feat in NUMERIC_FEATURES:
                feature_df[feat] = pd.to_numeric(feature_df[feat], errors='coerce').fillna(0.0)
            else:
                feature_df[feat] = feature_df[feat].fillna("unknown").astype(str)
                
        return pd.Series(self.model.predict(feature_df[ALL_FEATURES]), index=df.index)



    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a profit prediction from validated input data."""
        if not self.is_ready():
            raise RuntimeError("Model not loaded")

        # Build a DataFrame from input
        df = pd.DataFrame([input_data])

        # Ensure all required features exist
        missing = [f for f in ALL_FEATURES if f not in df.columns]
        if missing:
            raise ValueError(f"Missing required features: {', '.join(missing)}")
            
        for feat in ALL_FEATURES:
            if feat in NUMERIC_FEATURES:
                df[feat] = pd.to_numeric(df[feat], errors='coerce').fillna(0.0)
            else:
                df[feat] = df[feat].fillna("unknown").astype(str)

        # Reorder columns to match training
        df = df[ALL_FEATURES]

        prediction = float(self.model.predict(df)[0])

        return {
            "predicted_profit": round(prediction, 2),
            "model_name": self.metadata.get("selected_model", "profit_model"),
            "model_version": self.metadata.get("version", "1.0.0"),
            "caveat": self.metadata.get(
                "caveat",
                "Predictions are estimates based on historical patterns. Validate before acting."
            ),
        }

    def get_model_info(self) -> Dict[str, Any]:
        """Return model metadata for API responses."""
        return {
            "available": self.is_ready(),
            "model_name": self.metadata.get("selected_model"),
            "metrics": self.metadata.get("metrics"),
            "features": self.metadata.get("features", ALL_FEATURES),
            "created_at": self.metadata.get("created_at"),
            "use_case": self.metadata.get("use_case"),
            "split_info": self.metadata.get("split_info"),
        }


prediction_service = PredictionService()
