import sys
from pathlib import Path
import pytest

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.config import config

class TestConfig:
    """Test suite for config library"""
    
    def test_config_loads(self):
        """Test that config loads successfully"""
        assert config is not None
    
    def test_database_config_exists(self):
        """Test that database config exists"""
        db_config = config.get_database_config()
        assert db_config is not None
        assert isinstance(db_config, dict)
    
    def test_database_type(self):
        """Test that database type is configured"""
        db_type = config.get_database_type()
        assert db_type == "sqlite"
    
    def test_database_path(self):
        """Test that database path is configured"""
        db_path = config.get_database_path()
        assert db_path is not None
        assert "tasks.db" in db_path
    
    def test_app_version(self):
        """Test that app version is set"""
        assert config.config_data.get("app", {}).get("version") == "0.6.0"
    
    def test_app_name(self):
        """Test that app name is set"""
        assert config.config_data.get("app", {}).get("name") == "Task Manager"
