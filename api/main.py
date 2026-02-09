"""
FastAPI application entry point.
Provides REST APIs for authentication, tasks, and subscription management.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from core.database.db import get_engine, Base
# Import models to ensure they are registered with Base.metadata
from core.models import User, Task  # noqa
from .routes import auth, tasks, subscriptions

# Note: Database tables are created by the application startup or migrations.
# For testing, tables are created in the fixtures.

app = FastAPI(
    title="Momentum API",
    description="REST API for Momentum task management application",
    version="1.0.0"
)

# Configure CORS
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(subscriptions.router)


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "momentum-api"}


@app.get("/", tags=["root"])
def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Momentum API",
        "docs": "/docs",
        "version": "1.0.0"
    }
