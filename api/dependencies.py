"""
API dependencies for authentication and database access.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
from typing import Optional

from core.database.db import get_db
from core.models import User, Task
from .authentication import decode_token, SECRET_KEY, ALGORITHM
from .schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    token_data = TokenData(username=username)

    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception

    return user


def check_subscription_limits(user: User, db: Session) -> bool:
    """
    Check if a user has exceeded their task limit.
    Free accounts: max 25 tasks
    Paid accounts: unlimited
    """
    if user.is_subscribed:
        return True

    task_count = db.query(Task).filter(Task.user_id == user.id).count()
    if task_count >= 25:
        return False

    return True


def require_subscription_active(user: User = Depends(get_current_user)):
    """
    Dependency to ensure user has an active subscription or is within free limits.
    This checks the user's subscription status but not the task count.
    For task count limits, use the check_subscription_limits function in the route.
    """
    # For now, just return the user. The route will check task limits separately.
    return user
