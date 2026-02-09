"""
CRUD operations for tasks.
All endpoints require authentication.
Free accounts have a limit of 25 tasks.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database.db import get_db
from core.models import Task, User
from ..schemas import TaskCreate, TaskUpdate, TaskResponse
from ..dependencies import get_current_user, check_subscription_limits

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskResponse])
def get_all_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve all tasks for the authenticated user.
    """
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific task by ID.
    The task must belong to the authenticated user.
    """
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new task for the authenticated user.

    Checks subscription limits:
    - Free accounts: max 25 tasks
    - Paid accounts: unlimited
    """
    # Check subscription limits
    if not check_subscription_limits(current_user, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Task limit reached. Free accounts are limited to 25 tasks. Please upgrade to a paid subscription for unlimited tasks."
        )

    # Create new task with unique title for this user
    existing_task = db.query(Task).filter(
        Task.title == task_data.title,
        Task.user_id == current_user.id
    ).first()

    if existing_task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A task with this title already exists"
        )

    new_task = Task(
        **task_data.model_dump(),
        user_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing task.

    Only the title, details, and priority can be updated.
    The task must belong to the authenticated user.
    """
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Check if we're updating title and if it conflicts with existing title
    if task_update.title is not None:
        existing_task = db.query(Task).filter(
            Task.title == task_update.title,
            Task.user_id == current_user.id,
            Task.id != task_id
        ).first()

        if existing_task:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A task with this title already exists"
            )

    # Update only provided fields
    update_data = task_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No update data provided"
        )

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a task.
    The task must belong to the authenticated user.
    """
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return None
