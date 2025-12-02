import sys
from pathlib import Path
import pytest
import tempfile
import shutil

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import storage.database as sdb
from storage.database import Database


@pytest.fixture(scope="session")
def temp_db_dir():
    temp_dir = tempfile.mkdtemp()
    db_file = Path(temp_dir) / "test_tasks.db"
    sdb.db = Database(db_path=str(db_file))
    yield str(db_file)
    shutil.rmtree(temp_dir)
    sdb.db = Database()
