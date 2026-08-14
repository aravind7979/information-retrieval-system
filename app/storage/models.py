from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime

class DocumentMetadata(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    filepath = Column(String)
    extension = Column(String)
    size_bytes = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    query_text = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
