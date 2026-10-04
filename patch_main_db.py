import re
file_path = "backend/app/main.py"
with open(file_path, "r") as f:
    content = f.read()

replacement = """
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up SalesBrain Navigator backend")
    try:
        from backend.app.db.database import engine, Base
        Base.metadata.create_all(bind=engine)
        logger.info("Database schema initialized (create_all applied)")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        
    try:
        data_service.load()
"""

content = re.sub(r'\nfrom contextlib import asynccontextmanager.*?\n    try:\n        data_service\.load\(\)', replacement, content, flags=re.DOTALL)

with open(file_path, "w") as f:
    f.write(content)
