from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

# Prefer explicit env var; fall back to local SQLite in user's home directory
SQL_DB_URL = os.getenv("SQLALCHEMY_DB_URL") or os.getenv("SQLALCHEMY_DATABASE_URL")
if not SQL_DB_URL:
    home = Path.home()
    data_dir = home / ".momentum"
    data_dir.mkdir(parents=True, exist_ok=True)
    SQL_DB_URL = f"sqlite:///{data_dir}/main.db"


Base = declarative_base()

engine = create_engine(
    url=SQL_DB_URL, echo=False, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_base():
    return Base


def get_engine():
    return engine


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
