from sqlalchemy import Column, String, Integer, Boolean, DateTime
from datetime import datetime
from uuid import uuid4

from app.database.db import Base


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(String, primary_key=True, index=True, nullable=False, default=lambda: str(uuid4()))
    title = Column(String, index=True, unique=True, nullable=False)
    details = Column(String, index=True, nullable=False)
    priority = Column(Integer, index=True, nullable=False)
    is_completed = Column(Boolean, index=True, nullable=False, default=lambda: False)
    due_by = Column(DateTime, index=True, nullable=True)
    created_at = Column(DateTime, index=True, nullable=False, default=lambda: datetime.now())
    updated_at = Column(DateTime, index=True, nullable=False, default=lambda: datetime.now(), onupdate=lambda: datetime.now())

    def __repr__(self) -> str:
        return f"ID: {self.id} - Title: {self.title}"