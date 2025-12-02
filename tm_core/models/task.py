from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    details = Column(Text, nullable=True, default="")
    priority = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    is_completed = Column(Integer, nullable=False, default=0)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "details": self.details,
            "priority": self.priority,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_completed": self.is_completed,
        }
