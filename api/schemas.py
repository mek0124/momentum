"""
Pydantic schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
import uuid as uuid_module


# User schemas
class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: str
    username: str
    is_subscribed: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Task schemas
class TaskBase(BaseModel):
    title: str
    details: Optional[str] = None
    priority: int = 3


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    details: Optional[str] = None
    priority: Optional[int] = None


class TaskResponse(TaskBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Subscription schemas
class SubscriptionCreate(BaseModel):
    # For Stripe integration, this might include payment method ID
    payment_method_id: Optional[str] = None
    success_url: Optional[str] = None
    cancel_url: Optional[str] = None


class SubscriptionResponse(BaseModel):
    subscription_id: Optional[str] = None
    status: str
    message: str
    checkout_url: Optional[str] = None
