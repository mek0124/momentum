from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid as uuid_module

from ..database.db import get_base

Base = get_base()


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid_module.uuid4()))
    title = Column(String, nullable=False, index=True)
    details = Column(String)
    priority = Column(Integer, index=True, default=3)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationship to user
    owner = relationship("User", back_populates="tasks")