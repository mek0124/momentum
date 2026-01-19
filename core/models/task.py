from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, Time, SmallInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.db import get_base

Base = get_base()

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, unique=True, index=True)
    content = Column(String)
    completed = Column(Boolean, index=True, default=False)
    created_at = Column(DateTime, index=True, default=lambda: datetime.now())
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    priority = Column(SmallInteger, index=True, default=2)
    due_date = Column(Date, index=True, nullable=True)
    due_time = Column(Time, nullable=True)
    user = relationship("User", back_populates="tasks")