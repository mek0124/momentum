"""
Tests for authentication routes.
"""
import pytest
from fastapi.testclient import TestClient


def test_register_success(client, db_session):
    """Test successful user registration."""
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "password": "securepass123"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert "id" in data
    assert "created_at" in data
    assert "password_hash" not in data  # Password should not be returned

    # Verify user was created in database
    from core.models import User
    user = db_session.query(User).filter(User.username == "newuser").first()
    assert user is not None


def test_register_duplicate_username(client, test_user):
    """Test registration fails with duplicate username."""
    response = client.post(
        "/auth/register",
        json={
            "username": test_user["username"],  # Already exists
            "password": "anotherpass123"
        }
    )

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_register_invalid_data(client):
    """Test registration with missing data."""
    response = client.post(
        "/auth/register",
        json={
            "username": "incomplete"
            # Missing password
        }
    )
    assert response.status_code == 422  # Validation error


def test_login_success(client, test_user):
    """Test successful login."""
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["username"],
            "password": test_user["password"]
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    """Test login with wrong password."""
    # First create a user
    client.post(
        "/auth/register",
        json={
            "username": "user1",
            "password": "pass123"
        }
    )

    # Try to login with wrong password
    response = client.post(
        "/auth/login",
        data={
            "username": "user1",
            "password": "wrongpass"
        }
    )

    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_nonexistent_user(client):
    """Test login with non-existent user."""
    response = client.post(
        "/auth/login",
        data={
            "username": "nonexistent",
            "password": "somepassword"
        }
    )

    assert response.status_code == 401


def test_get_current_user_authenticated(client, auth_headers):
    """Test getting current user info with valid token."""
    response = client.get("/auth/me", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "username" in data
    assert "is_subscribed" in data


def test_get_current_user_unauthenticated(client):
    """Test getting current user info without token."""
    response = client.get("/auth/me")
    assert response.status_code == 401
