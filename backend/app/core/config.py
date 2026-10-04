from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    @property
    def DATASET_PATH(self) -> str:
        # Check both local path (with backend/ root) and vercel path (without backend/)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # In local (repo root): base_dir is backend/app -> we want ../dataset/...
        # On Vercel (root="backend"): base_dir is /var/task/app -> we want ../dataset/...
        
        # Actually, let's just use absolute path relative to this file
        # __file__ = backend/app/core/config.py
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # app_dir = backend/app
        backend_dir = os.path.dirname(app_dir)
        # backend_dir = backend
        
        path1 = os.path.join(backend_dir, "dataset", "Cleaned_SuperStore.csv")
        path2 = os.path.join(os.path.dirname(backend_dir), "dataset", "Cleaned_SuperStore.csv")
        
        if os.path.exists(path1):
            return path1
        if os.path.exists(path2):
            return path2
        return path1

    API_HOST: str = os.getenv('API_HOST', '127.0.0.1')
    API_PORT: int = int(os.getenv('API_PORT', 8000))
    
    _cors = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000')
    CORS_ORIGINS: List[str] = _cors.split(',') if _cors else []
    
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    ML_ARTIFACTS_DIR: str = os.getenv('ML_ARTIFACTS_DIR', 'backend/app/ml/artifacts')
    PROJECT_NAME: str = 'SalesBrain Navigator'
    VERSION: str = '1.0.0'

settings = Settings()
