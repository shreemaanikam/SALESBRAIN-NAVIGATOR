from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    _DATASET_PATH_RAW: str = os.getenv('DATASET_PATH', 'backend/dataset/Cleaned_SuperStore.csv')

    @property
    def DATASET_PATH(self) -> str:
        if os.path.isabs(self._DATASET_PATH_RAW): return self._DATASET_PATH_RAW
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        return os.path.join(base_dir, self._DATASET_PATH_RAW)

    API_HOST: str = os.getenv('API_HOST', '127.0.0.1')
    API_PORT: int = int(os.getenv('API_PORT', 8000))
    
    _cors = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000')
    CORS_ORIGINS: List[str] = _cors.split(',') if _cors else []
    
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    ML_ARTIFACTS_DIR: str = os.getenv('ML_ARTIFACTS_DIR', 'backend/app/ml/artifacts')
    PROJECT_NAME: str = 'SalesBrain Navigator'
    VERSION: str = '1.0.0'

settings = Settings()
