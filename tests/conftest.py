"""
Pytest fixtures for testing the API.
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Set test environment variables BEFORE importing the app
os.environ["SQLALCHEMY_DATABASE_URL"] = "sqlite:///:memory:"
os.environ["JWT_SECRET_KEY"] = "test-secret-key"
os.environ["STRIPE_SECRET_KEY"] = "sk_test_fake"
os.environ["STRIPE_PRICE_ID"] = "price_fake"
os.environ["STRIPE_WEBHOOK_SECRET"] = "whsec_fake"
os.environ["API_BASE_URL"] = "http://localhost:8000"

# Test database URL - use SQLite in-memory for tests
TEST_DATABASE_URL = "sqlite:///:memory:"

from api.main import app
from core.database.db import Base, get_db


@pytest.fixture(scope="function")
def engine():
    """Create test database engine."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def TestingSessionLocal(engine):
    """Create a session factory for tests."""
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session(TestingSessionLocal):
    """Create a fresh database session for each test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    """Create a FastAPI test client with overridden dependencies."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def test_user(client, db_session):
    """Create a test user and return the credentials."""
    from core.models import User
    from api.authentication import get_password_hash

    username = "testuser"
    password = "testpass123"

    # Check if user already exists
    existing = db_session.query(User).filter(User.username == username).first()
    if not existing:
        user = User(
            username=username,
            password_hash=get_password_hash(password)
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

    return {"username": username, "password": password}


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers with a valid JWT token."""
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["username"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_user_with_subscription(client, db_session):
    """Create a test user with an active subscription."""
    from core.models import User
    from api.authentication import get_password_hash

    username = "subscriber"
    password = "subpass123"

    user = User(
        username=username,
        password_hash=get_password_hash(password),
        is_subscribed=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Get auth token
    response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password
        }
    )
    token = response.json()["access_token"]

    return {
        "user": user,
        "headers": {"Authorization": f"Bearer {token}"}
    }
