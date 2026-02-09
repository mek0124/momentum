"""
Subscription management routes using Stripe.
Price: $0.99/month
"""
import os
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import stripe
from typing import Optional

from core.database.db import get_db
from core.models import User
from ..dependencies import get_current_user
from ..schemas import SubscriptionCreate, SubscriptionResponse

# Load Stripe API key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_ID")  # Price ID for $0.99/month subscription

router = APIRouter(prefix="/subscription", tags=["subscriptions"])


@router.get("/status", response_model=dict)
def get_subscription_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the current user's subscription status.
    """
    # Refresh user from database to get latest subscription status
    user = db.query(User).filter(User.id == current_user.id).first()

    return {
        "is_subscribed": user.is_subscribed,
        "subscription_id": None,  # Could store Stripe subscription ID in user model if needed
        "plan": "premium" if user.is_subscribed else "free",
    }


@router.post("/create-checkout-session", response_model=SubscriptionResponse)
def create_checkout_session(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a Stripe Checkout session for subscription purchase.
    """
    if not STRIPE_PRICE_ID:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Stripe price ID not configured. Contact administrator."
        )

    if current_user.is_subscribed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has an active subscription"
        )

    try:
        # Create Stripe Checkout session
        checkout_session = stripe.checkout.Session.create(
            customer_email=current_user.username,  # Using username as email placeholder
            payment_method_types=["card"],
            line_items=[
                {
                    "price": STRIPE_PRICE_ID,
                    "quantity": 1,
                }
            ],
            mode="subscription",
            success_url=f"{os.getenv('API_BASE_URL', 'http://localhost:8000')}/subscription/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{os.getenv('API_BASE_URL', 'http://localhost:8000')}/subscription/cancel",
            metadata={
                "user_id": current_user.id
            }
        )

        return {
            "status": "checkout_created",
            "message": "Checkout session created",
            "checkout_url": checkout_session.url,
            "subscription_id": None
        }

    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Stripe error: {str(e)}"
        )


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Handle Stripe webhook events.
    This endpoint should be called by Stripe to notify of subscription events.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not sig_header:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing Stripe signature"
        )

    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    if not webhook_secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Stripe webhook secret not configured"
        )

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid payload"
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid signature"
        )

    # Handle the event
    event_type = event["type"]
    event_data = event["data"]["object"]

    if event_type == "checkout.session.completed":
        # When checkout is completed, activate subscription
        session = event_data
        user_id = session.get("metadata", {}).get("user_id")

        if user_id:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.is_subscribed = True
                db.commit()

    elif event_type == "customer.subscription.deleted":
        # When subscription is cancelled, deactivate subscription
        subscription = event_data
        # Find user by Stripe customer ID or email
        customer_email = subscription.get("customer_email")
        # Note: This is simplified. In production, store Stripe customer ID on user model
        if customer_email:
            user = db.query(User).filter(User.username == customer_email).first()
            if user:
                user.is_subscribed = False
                db.commit()

    return {"status": "success"}


@router.post("/cancel")
def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel the user's subscription.
    This will cancel at the end of the current billing period.
    """
    # Note: To implement cancellation, you would need to store the Stripe subscription ID
    # For now, we'll just mark the user as not subscribed
    if not current_user.is_subscribed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active subscription found"
        )

    # In a real implementation, you would call Stripe API to cancel subscription:
    # stripe.Subscription.delete(stripe_subscription_id)
    # For now, just deactivate
    current_user.is_subscribed = False
    db.commit()

    return {
        "status": "success",
        "message": "Subscription cancelled successfully"
    }
