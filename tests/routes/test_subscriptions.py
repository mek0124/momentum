"""
Tests for subscription routes.
"""
import pytest
from unittest.mock import patch, MagicMock
import stripe


def test_get_subscription_status_free(client, auth_headers):
    """Test getting subscription status for free user."""
    response = client.get("/subscription/status", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert "is_subscribed" in data
    assert data["is_subscribed"] is False
    assert data["plan"] == "free"


def test_get_subscription_status_paid(client, test_user_with_subscription):
    """Test getting subscription status for paid user."""
    headers = test_user_with_subscription["headers"]
    response = client.get("/subscription/status", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["is_subscribed"] is True
    assert data["plan"] == "premium"


@patch('stripe.checkout.Session.create')
def test_create_checkout_session_success(mock_stripe_create, client, auth_headers):
    """Test creating a checkout session successfully."""
    # Mock Stripe response
    mock_session = MagicMock()
    mock_session.url = "https://checkout.stripe.com/test"
    mock_stripe_create.return_value = mock_session

    response = client.post(
        "/subscription/create-checkout-session",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "checkout_created"
    assert "checkout_url" in data
    assert data["checkout_url"] == "https://checkout.stripe.com/test"


@patch('stripe.checkout.Session.create')
def test_create_checkout_session_already_subscribed(mock_stripe_create, client, test_user_with_subscription):
    """Test that paid users cannot create another checkout session."""
    headers = test_user_with_subscription["headers"]

    response = client.post(
        "/subscription/create-checkout-session",
        headers=headers
    )

    assert response.status_code == 400
    assert "already has an active subscription" in response.json()["detail"]
    mock_stripe_create.assert_not_called()


def test_create_checkout_session_not_configured(client, auth_headers):
    """Test checkout session creation fails when Stripe is not configured."""
    # Temporarily remove Stripe config
    with patch.dict('os.environ', {'STRIPE_PRICE_ID': ''}, clear=True):
        # Re-import to clear cached value
        from importlib import reload
        import api.routes.subscriptions as subs_module
        reload(subs_module)

        response = client.post(
            "/subscription/create-checkout-session",
            headers=auth_headers
        )

        assert response.status_code == 500
        assert "not configured" in response.json()["detail"].lower()


@patch('stripe.Webhook.construct_event')
def test_stripe_webhook_checkout_completed(mock_construct_event, client, db_session):
    """Test Stripe webhook handles checkout.session.completed."""
    from core.models import User
    from api.authentication import get_password_hash

    # Create a user
    user = User(
        username="webhookuser",
        password_hash=get_password_hash("password")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Mock Stripe event
    mock_event = {
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "metadata": {
                    "user_id": str(user.id)
                }
            }
        }
    }
    mock_construct_event.return_value = mock_event

    # Call webhook
    response = client.post(
        "/subscription/webhook",
        data={"test": "data"},
        headers={"stripe-signature": "test_signature"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"

    # Verify user is now subscribed
    db_session.refresh(user)
    assert user.is_subscribed is True


@patch('stripe.Webhook.construct_event')
def test_stripe_webhook_subscription_deleted(mock_construct_event, client, db_session, test_user):
    """Test Stripe webhook handles customer.subscription.deleted."""
    from core.models import User

    # Get the test user (already created by test_user fixture)
    user = db_session.query(User).filter(User.username == test_user["username"]).first()
    assert user is not None

    user.is_subscribed = True
    db_session.commit()
    db_session.refresh(user)

    # Mock Stripe event with email
    mock_event = {
        "type": "customer.subscription.deleted",
        "data": {
            "object": {
                "customer_email": user.username
            }
        }
    }
    mock_construct_event.return_value = mock_event

    response = client.post(
        "/subscription/webhook",
        data={"test": "data"},
        headers={"stripe-signature": "test_signature"}
    )

    assert response.status_code == 200

    # Verify user is now unsubscribed
    db_session.refresh(user)
    assert user.is_subscribed is False


def test_stripe_webhook_missing_signature(client):
    """Test webhook fails without signature."""
    response = client.post("/subscription/webhook", data={"test": "data"})
    assert response.status_code == 400
    assert "Missing Stripe signature" in response.json()["detail"]
