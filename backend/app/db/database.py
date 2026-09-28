import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./backend/app/data/salesbrain.db")

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
