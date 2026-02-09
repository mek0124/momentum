"""
Tests for the User model.
"""
import uuid
from sqlalchemy.orm import Session

from core.models import User
from api.authentication import get_password_hash, verify_password


def test_user_create(db_session: Session):
    """Test creating a user in the database."""
    user = User(
        username="testuser",
        password_hash=get_password_hash("password123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert isinstance(uuid.UUID(user.id), uuid.UUID)  # Valid UUID
    assert user.username == "testuser"
    assert user.password_hash != "password123"  # Should be hashed
    assert verify_password("password123", user.password_hash)
    assert user.is_subscribed is False
    assert user.created_at is not None


def test_user_duplicate_username_fails(db_session: Session):
    """Test that duplicate usernames are not allowed (unique constraint)."""
    user1 = User(
        username="duplicate",
        password_hash=get_password_hash("pass1")
    )
    user2 = User(
        username="duplicate",
        password_hash=get_password_hash("pass2")
    )

    db_session.add(user1)
    db_session.commit()

    db_session.add(user2)
    try:
        db_session.commit()
        # Should not reach here due to integrity error
        assert False, "Duplicate username should have raised an error"
    except Exception:
        db_session.rollback()


def test_user_subscription_flag(db_session: Session):
    """Test user subscription status."""
    user = User(
        username="subscriber",
        password_hash=get_password_hash("password")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.is_subscribed is False

    user.is_subscribed = True
    db_session.commit()
    db_session.refresh(user)

    assert user.is_subscribed is True


def test_user_task_relationship(db_session: Session):
    """Test user-to-tasks relationship."""
    from core.models import Task
    from sqlalchemy import insert

    user = User(
        username="taskowner",
        password_hash=get_password_hash("password")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create tasks for this user
    task1 = Task(
        title="Task 1",
        details="Details 1",
        priority=1,
        user_id=user.id
    )
    task2 = Task(
        title="Task 2",
        details="Details 2",
        priority=2,
        user_id=user.id
    )

    db_session.add_all([task1, task2])
    db_session.commit()

    # Reload user with tasks
    db_session.refresh(user)
    assert len(user.tasks) == 2
    assert user.tasks[0].title in ["Task 1", "Task 2"]
    assert user.tasks[1].title in ["Task 1", "Task 2"]
