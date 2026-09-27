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
        self.artifacts_dir = os.environ.get("ML_ARTIFACTS_DIR", "backend/app/ml/artifacts")
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

    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a profit prediction from validated input data."""
        if not self.is_ready():
            raise RuntimeError("Model not loaded")

        # Build a DataFrame from input
        df = pd.DataFrame([input_data])

        # Ensure all required features exist
        for feat in ALL_FEATURES:
            if feat not in df.columns:
                if feat in NUMERIC_FEATURES:
                    df[feat] = 0.0
                else:
                    df[feat] = "unknown"

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
