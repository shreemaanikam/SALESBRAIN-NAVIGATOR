from sqlalchemy import Column, String, DateTime, JSON
import datetime
from .database import Base

class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False, server_default="legacy_user")
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    status = Column(String, default="uploaded")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Store schema, profiling, mapping, and generated artifacts as JSON
    profile = Column(JSON, nullable=True)
    mapping = Column(JSON, nullable=True)
    dashboard = Column(JSON, nullable=True)
    insights = Column(JSON, nullable=True)
    recommendations = Column(JSON, nullable=True)
