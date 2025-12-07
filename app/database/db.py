from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine(
    "sqlite:///./app/data/main.db",
    connect_args = {
        "check_same_thread": False,
    }
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_engine():
    return engine


def get_base():
    return Base


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()