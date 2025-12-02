import sys
from pathlib import Path

# add project root so config is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config.config import config
from core.models import Task
from typing import Tuple, Union

class Database:
    def __init__(self) -> None:
        self.engine = None
        self.SessionLocal = None
        self._initialize_db()
    
    def _initialize_db(self) -> Tuple[bool, str]:
        try:
            db_path = config.get_database_path()
            db_type = config.get_database_type()
            
            # Create data directory if it doesn't exist
            data_dir = Path(db_path).parent
            data_dir.mkdir(parents=True, exist_ok=True)
            
            # Create connection string
            if db_type == "sqlite":
                connection_string = f"sqlite:///{db_path}"
            else:
                raise ValueError(f"Unsupported database type: {db_type}")
            
            self.engine = create_engine(connection_string, echo=False)
            self.SessionLocal = sessionmaker(bind=self.engine)
            
            # Create tables
            Task.metadata.create_all(self.engine)
            
            return True, "Database initialized successfully"
        
        except Exception as e:
            return False, f"Failed to initialize database: {e}"
    
    def get_session(self) -> Session:
        return self.SessionLocal()
    
    def close(self) -> None:
        if self.engine:
            self.engine.dispose()

# Global database instance
db = Database()
