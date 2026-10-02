from fastapi import APIRouter
from datetime import datetime
from backend.app.core.config import settings
from backend.app.services.data_service import data_service
from backend.app.services.prediction_service import prediction_service
from sqlalchemy.orm import Session
from fastapi import Depends
from backend.app.db.database import get_db
from backend.app.services.storage_service import storage_service
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.migration import MigrationContext
import sqlalchemy


router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    db_status = "ok"
    migration_version = None
    try:
        db.execute(sqlalchemy.text("SELECT 1"))
        context = MigrationContext.configure(db.connection())
        migration_version = context.get_current_revision()
    except Exception:
        db_status = "error"

    storage_reachable = True
    try:
        if storage_service.backend == "s3":
            storage_service.s3.head_bucket(Bucket=storage_service.bucket)
    except Exception:
        storage_reachable = False

    return {
        "status": "ok",
        "version": settings.VERSION,
        "timestamp": datetime.now().isoformat(),
        "database": {
            "status": db_status,
            "migration_version": migration_version
        },
        "storage": {
            "backend": storage_service.backend,
            "reachable": storage_reachable
        },
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
