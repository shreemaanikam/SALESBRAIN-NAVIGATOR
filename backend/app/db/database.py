import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./backend/app/data/salesbrain.db")
IS_PRODUCTION = os.getenv("RENDER", "false") == "true" or os.getenv("ENVIRONMENT") == "production"

if IS_PRODUCTION and DATABASE_URL.startswith("sqlite"):
    error_msg = (
        "CRITICAL STARTUP ERROR: The application is running in a production environment "
        "but DATABASE_URL is configured to use SQLite. "
        "SQLite is not supported for production deployments due to concurrency limits on persistent disks. "
        "Please provision a PostgreSQL database and configure the DATABASE_URL environment variable."
    )
    logger.error(error_msg)
    raise RuntimeError(error_msg)

# Setup engine with PostgreSQL optimizations if applicable
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL production configurations
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
