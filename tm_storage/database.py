from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from tm_config.config import config
from tm_core.models import Task
from typing import Tuple, Union, Optional


class Database:
    def __init__(self, db_path: Optional[str] = None) -> None:
        self.engine = None
        self.SessionLocal = None
        self._db_path_override = db_path
        self._initialize_db()
    
    def _initialize_db(self) -> Tuple[bool, str]:
        try:
            if self._db_path_override:
                db_path = self._db_path_override

            else:
                base_dir = Path(__file__).parent
                data_dir = base_dir / "data"
                data_dir.mkdir(parents=True, exist_ok=True)
                db_path = str(data_dir / "tasks.db")

            db_type = "sqlite"
            data_parent = Path(db_path).parent
            data_parent.mkdir(parents=True, exist_ok=True)

            if db_type == "sqlite":
                connection_string = f"sqlite:///{db_path}"

            else:
                raise ValueError(f"Unsupported database type: {db_type}")

            self.engine = create_engine(connection_string, echo=False)
            self.SessionLocal = sessionmaker(bind=self.engine)

            Task.metadata.create_all(self.engine)

            return True, "Database initialized successfully"

        except Exception as e:
            return False, f"Failed to initialize database: {e}"
    
    def get_session(self) -> Session:
        return self.SessionLocal()
    
    def close(self) -> None:
        if self.engine:
            self.engine.dispose()


db = Database()
