import pandas as pd
import os
from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.core.exceptions import DatasetNotFoundError, DataValidationError
from backend.app.data.validation import validate_columns, validate_dtypes, validate_data_quality

class DataService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataService, cls).__new__(cls)
            cls._instance._df = None
            cls._instance._loaded = False
            cls._instance._quality_info = {}
        return cls._instance

    def load(self):
        if self._loaded:
            return

        dataset_path = settings.DATASET_PATH
        if not os.path.exists(dataset_path):
            logger.error(f"Dataset not found at {dataset_path}")
            raise DatasetNotFoundError(f"Dataset not found at {dataset_path}")

        try:
            logger.info(f"Loading dataset from {dataset_path}")
            self._df = pd.read_csv(dataset_path)
            
            import numpy as np
            # Replace inf/-inf with NaN to prevent Pandas RuntimeWarnings during std() calculations
            self._df.replace([np.inf, -np.inf], np.nan, inplace=True)
            
            # validate
            validate_columns(self._df)
            validate_dtypes(self._df)
            
            self._quality_info = validate_data_quality(self._df)
            self._loaded = True
            logger.info("Dataset loaded and validated successfully")
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            raise DataValidationError(f"Error validating dataset: {str(e)}")

    def get_df(self) -> pd.DataFrame:
        if not self._loaded:
            self.load()
        return self._df.copy()

    def get_quality_info(self) -> dict:
        if not self._loaded:
            self.load()
        return self._quality_info

    def is_loaded(self) -> bool:
        return self._loaded

data_service = DataService()
