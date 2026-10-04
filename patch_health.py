with open('backend/app/api/v1/routes/health.py', 'r') as f:
    content = f.read()

import re

new_imports = """
from sqlalchemy.orm import Session
from fastapi import Depends
from backend.app.db.database import get_db
from backend.app.services.storage_service import storage_service
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.migration import MigrationContext
import sqlalchemy
"""

content = content.replace("from backend.app.services.prediction_service import prediction_service", 
"from backend.app.services.prediction_service import prediction_service" + new_imports)

new_health = """@router.get("/health")
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
    }"""

content = re.sub(r"@router\.get\(\"/health\"\)\ndef health_check\(\):.*?\"model_ready\": prediction_service\.is_ready\(\)\n    \}", new_health, content, flags=re.DOTALL)

with open('backend/app/api/v1/routes/health.py', 'w') as f:
    f.write(content)
