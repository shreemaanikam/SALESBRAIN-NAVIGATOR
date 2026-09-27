from fastapi import APIRouter
from datetime import datetime
from backend.app.core.config import settings
from backend.app.services.data_service import data_service
from backend.app.services.prediction_service import prediction_service

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "version": settings.VERSION,
        "timestamp": datetime.now().isoformat(),
        "dataset_ready": data_service.is_loaded(),
        "model_ready": prediction_service.is_ready()
    }

@router.get("/metadata")
def metadata():
    ds_info = data_service.get_quality_info() if data_service.is_loaded() else {}
    return {
        "dataset": {
            "schema": "Cleaned_SuperStore",
            "row_count": ds_info.get("row_count", 0),
            "date_range": ds_info.get("date_range", {}),
            "columns": ds_info.get("column_count", 0)
        },
        "model": {
            "available": prediction_service.is_ready(),
            "metrics": prediction_service.get_model_info().get("metrics") if prediction_service.is_ready() else None
        }
    }
