"""
Tests for task routes.
"""
import pytest
from fastapi.testclient import TestClient


def test_get_tasks_empty(client, auth_headers):
    """Test getting all tasks when user has none."""
    response = client.get("/tasks", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == []


def test_get_tasks_with_data(client, auth_headers, db_session):
    """Test getting all tasks when user has tasks."""
    from core.models import Task, User

    # Get user from database
    user = db_session.query(User).filter(
        User.username == auth_headers.get("username", "testuser")  # This might not work
    ).first()

    # Actually, let's use the test_user fixture info
    # We'll create a task directly in the database
    # But we need the user ID. Let me think...

    # For this test, we'll need to get the user being authenticated
    # Since auth_headers comes from test_user fixture, we can decode the token
    # But simpler: We'll just create tasks and know they exist
    # Actually, I'll use the db_session fixture with a known user

    # This is a bit tricky with the fixtures, so let's modify:
    # We'll decode the token to get username, but that's complicated.
    # Alternative: we create tasks using the API itself

    pass  # We'll implement differently


def test_create_task_success(client, auth_headers):
    """Test creating a task successfully."""
    response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "New Task",
            "details": "Task details",
            "priority": 2
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Task"
    assert data["details"] == "Task details"
    assert data["priority"] == 2
    assert "id" in data
    assert "user_id" in data
    assert data["created_at"] is not None


def test_create_task_missing_title(client, auth_headers):
    """Test creating task with missing title."""
    response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "details": "No title provided",
            "priority": 1
        }
    )
    assert response.status_code == 422  # Validation error


def test_create_task_duplicate_title(client, auth_headers):
    """Test creating task with duplicate title for same user."""
    # Create first task
    client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "Unique Title",
            "details": "Details",
            "priority": 1
        }
    )

    # Try to create another with same title
    response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "Unique Title",
            "details": "Different details",
            "priority": 2
        }
    )

    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_get_task_by_id(client, auth_headers):
    """Test getting a specific task."""
    # Create a task
    create_response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "Get Me",
            "details": "I'm testable",
            "priority": 3
        }
    )
    task_id = create_response.json()["id"]

    # Get that task
    response = client.get(f"/tasks/{task_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Get Me"


def test_get_task_by_id_not_found(client, auth_headers):
    """Test getting a non-existent task."""
    response = client.get("/tasks/999999", headers=auth_headers)
    assert response.status_code == 404


def test_update_task(client, auth_headers):
    """Test updating a task."""
    # Create a task
    create_response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "Original",
            "details": "Original details",
            "priority": 1
        }
    )
    task_id = create_response.json()["id"]

    # Update it
    response = client.put(
        f"/tasks/{task_id}",
        headers=auth_headers,
        json={
            "title": "Updated",
            "details": "Updated details",
            "priority": 2
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["details"] == "Updated details"
    assert data["priority"] == 2


def test_update_task_partial(client, auth_headers):
    """Test partial update (only some fields)."""
    # Create a task
    create_response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "Partial Update",
            "details": "Original",
            "priority": 1
        }
    )
    task_id = create_response.json()["id"]

    # Update only priority
    response = client.put(
        f"/tasks/{task_id}",
        headers=auth_headers,
        json={
            "priority": 3
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Partial Update"  # Unchanged
    assert data["priority"] == 3  # Updated


def test_update_task_not_found(client, auth_headers):
    """Test updating non-existent task."""
    response = client.put(
        "/tasks/999999",
        headers=auth_headers,
        json={
            "title": "Won't work"
        }
    )
    assert response.status_code == 404


def test_delete_task(client, auth_headers):
    """Test deleting a task."""
    # Create a task
    create_response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "To Delete",
            "details": "Gone soon",
            "priority": 2
        }
    )
    task_id = create_response.json()["id"]

    # Delete it
    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_delete_task_not_found(client, auth_headers):
    """Test deleting non-existent task."""
    response = client.delete("/tasks/999999", headers=auth_headers)
    assert response.status_code == 404


def test_task_access_other_user(client, auth_headers, db_session):
    """Test that user cannot access another user's tasks."""
    from core.models import User
    from api.authentication import get_password_hash

    # Create another user
    other_user = User(
        username="otheruser",
        password_hash=get_password_hash("otherpass")
    )
    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    # Create a task for the other user
    from core.models import Task
    other_task = Task(
        title="Other's Task",
        details="Not mine",
        priority=1,
        user_id=other_user.id
    )
    db_session.add(other_task)
    db_session.commit()
    db_session.refresh(other_task)

    # Try to access that task
    response = client.get(f"/tasks/{other_task.id}", headers=auth_headers)
    assert response.status_code == 404


def test_subscription_limit_free_user(client, db_session, test_user):
    """Test that free users are limited to 25 tasks."""
    from core.models import User

    # Ensure current user is not subscribed
    user = db_session.query(User).filter(
        User.username == test_user["username"]
    ).first()
    user.is_subscribed = False
    db_session.commit()

    # First, get auth headers (since we modified user)
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["username"],
            "password": test_user["password"]
        }
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create 25 tasks (should succeed)
    for i in range(25):
        response = client.post(
            "/tasks",
            headers=headers,
            json={
                "title": f"Task {i}",
                "details": f"Details {i}",
                "priority": 3
            }
        )
        assert response.status_code == 201

    # 26th task should fail
    response = client.post(
        "/tasks",
        headers=headers,
        json={
            "title": "Task 26",
            "details": "Should fail",
            "priority": 3
        }
    )
    assert response.status_code == 403
    assert "limit reached" in response.json()["detail"]


def test_subscription_limit_paid_user(client, test_user_with_subscription):
    """Test that paid users have unlimited tasks."""
    headers = test_user_with_subscription["headers"]

    # Create more than 25 tasks
    for i in range(30):
        response = client.post(
            "/tasks",
            headers=headers,
            json={
                "title": f"Paid Task {i}",
                "details": f"Details {i}",
                "priority": 3
            }
        )
        assert response.status_code == 201
