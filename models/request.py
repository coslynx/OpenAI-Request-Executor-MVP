from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    status = Column(String)
    response = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, text: str, status: str = "pending", response: str = None, created_at: DateTime = None):
        if not text or len(text) < 5:
            raise ValueError("Invalid request text: Must be at least 5 characters long")
        if status not in ["pending", "completed", "error"]:
            raise ValueError("Invalid request status: Must be 'pending', 'completed', or 'error'")
        self.text = text
        self.status = status
        self.response = response
        self.created_at = created_at or datetime.utcnow()