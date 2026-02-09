"""
Tests for the Task model.
"""
import uuid
from sqlalchemy.orm import Session

from core.models import Task, User
from api.authentication import get_password_hash


def test_task_create(db_session: Session, test_user):
    """Test creating a task."""
    # Get user from database
    user = db_session.query(User).filter(User.username == test_user["username"]).first()

    task = Task(
        title="Test Task",
        details="Test details",
        priority=2,
        user_id=user.id
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    assert task.id is not None
    assert isinstance(uuid.UUID(task.id), uuid.UUID)  # Valid UUID
    assert task.title == "Test Task"
    assert task.details == "Test details"
    assert task.priority == 2
    assert task.user_id == user.id
    assert task.created_at is not None
    assert task.owner == user


def test_task_priority_default(db_session: Session, test_user):
    """Test that task priority defaults to 3."""
    user = db_session.query(User).filter(User.username == test_user["username"]).first()

    task = Task(
        title="Default Priority Task",
        details="Details",
        user_id=user.id
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    assert task.priority == 3


def test_task_update_timestamp(db_session: Session, test_user):
    """Test that task updated_at changes on update."""
    from datetime import datetime
    import time

    user = db_session.query(User).filter(User.username == test_user["username"]).first()

    task = Task(
        title="Timestamp Task",
        details="Details",
        user_id=user.id
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    initial_updated_at = task.updated_at
    time.sleep(0.1)  # Small delay to ensure different timestamp

    task.priority = 1
    db_session.commit()
    db_session.refresh(task)

    # updated_at should have changed
    if task.updated_at is not None and initial_updated_at is not None:
        assert task.updated_at > initial_updated_at
    assert task.priority == 1


def test_task_cascade_delete(db_session: Session, test_user):
    """Test that deleting a user cascades to their tasks."""
    user = db_session.query(User).filter(User.username == test_user["username"]).first()

    task = Task(
        title="To be deleted",
        details="Details",
        user_id=user.id
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    task_id = task.id

    # Delete the user
    db_session.delete(user)
    db_session.commit()

    # Task should be deleted as well
    deleted_task = db_session.query(Task).filter(Task.id == task_id).first()
    assert deleted_task is None
