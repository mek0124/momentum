import sys
from pathlib import Path
import pytest
import tempfile
import shutil

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture(scope="session")
def temp_db_dir():
    """Create temporary directory for test databases"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_config(temp_db_dir, monkeypatch):
    """Mock config for testing with temporary database"""
    from config.config import Config
    
    # Create a mock config object
    class MockConfig:
        def get_database_config(self):
            return {"type": "sqlite", "path": f"{temp_db_dir}/test_tasks.db"}
        
        def get_database_path(self):
            return f"{temp_db_dir}/test_tasks.db"
        
        def get_database_type(self):
            return "sqlite"
    
    return MockConfig()
