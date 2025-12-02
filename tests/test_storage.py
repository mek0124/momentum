import sys
from pathlib import Path
import pytest
import tempfile
import shutil
from datetime import datetime
from uuid import uuid4
import os

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class TestOfflineStorageController:
    """Test suite for offline storage controller"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test database before each test"""
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test_tasks.db"
        
        # Mock config
        import config.config as config_module
        original_path = config_module.config.config_path
        
        class MockConfig:
            def get_database_config(self):
                return {"type": "sqlite", "path": str(self.db_path)}
            
            def get_database_path(self):
                return str(self.db_path)
            
            def get_database_type(self):
                return "sqlite"
        
        config_module.config = MockConfig()
        
        # Reinitialize database with test config
        from storage.database import Database
        self.db = Database()
        
        yield
        
        # Cleanup
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        config_module.config.config_path = original_path
    
    def test_create_task(self):
        """Test creating a task"""
        from storage.controllers.offline import OfflineStorageController
        
        controller = OfflineStorageController()
        new_task = {
            "id": str(uuid4()),
            "title": "Test Task",
            "details": "Test Details",
            "priority": 1,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "is_completed": 0
        }
        
        success, message = controller.create_task(new_task)
        
        assert success is True
        assert message == "Task Saved Successfully"
    
    def test_get_all_tasks(self):
        """Test retrieving all tasks"""
        from storage.controllers.offline import OfflineStorageController
        
        controller = OfflineStorageController()
        
        # Create a task
        new_task = {
            "id": str(uuid4()),
            "title": "Test Task",
            "details": "Test Details",
            "priority": 1,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "is_completed": 0
        }
        controller.create_task(new_task)
        
        # Retrieve all tasks
        success, tasks = controller.get_all_tasks()
        
        assert success is True
        assert isinstance(tasks, list)
        assert len(tasks) > 0
    
    def test_get_task_by_id(self):
        """Test retrieving a task by ID"""
        from storage.controllers.offline import OfflineStorageController
        
        controller = OfflineStorageController()
        task_id = str(uuid4())
        
        # Create a task
        new_task = {
            "id": task_id,
            "title": "Test Task",
            "details": "Test Details",
            "priority": 2,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "is_completed": 0
        }
        controller.create_task(new_task)
        
        # Retrieve the task
        success, task = controller.list_task_by_id(task_id)
        
        assert success is True
        assert task["id"] == task_id
        assert task["title"] == "Test Task"
    
    def test_update_task(self):
        """Test updating a task"""
        from storage.controllers.offline import OfflineStorageController
        
        controller = OfflineStorageController()
        task_id = str(uuid4())
        
        # Create a task
        new_task = {
            "id": task_id,
            "title": "Original Title",
            "details": "Original Details",
            "priority": 1,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "is_completed": 0
        }
        controller.create_task(new_task)
        
        # Update the task
        updated_task = {
            "id": task_id,
            "title": "Updated Title",
            "details": "Updated Details",
            "priority": 3,
            "updated_at": datetime.now(),
            "is_completed": 1
        }
        success, message = controller.update_task(updated_task)
        
        assert success is True
        assert message == "Task Updated Successfully"
        
        # Verify the update
        _, task = controller.list_task_by_id(task_id)
        assert task["title"] == "Updated Title"
    
    def test_delete_task(self):
        """Test deleting a task"""
        from storage.controllers.offline import OfflineStorageController
        
        controller = OfflineStorageController()
        task_id = str(uuid4())
        
        # Create a task
        new_task = {
            "id": task_id,
            "title": "Test Task",
            "details": "Test Details",
            "priority": 1,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "is_completed": 0
        }
        controller.create_task(new_task)
        
        # Delete the task
        success, message = controller.delete_task(task_id)
        
        assert success is True
        assert message == "Task Deleted Successfully"
        
        # Verify deletion
        success, _ = controller.list_task_by_id(task_id)
        assert success is False
    
    def test_create_task_with_missing_id(self):
        """Test creating a task fails with missing required field"""
        from storage.controllers.offline import OfflineStorageController
        
        controller = OfflineStorageController()
        new_task = {
            "title": "Test Task",
            "priority": 1,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        
        success, message = controller.create_task(new_task)
        
        assert success is False

class TestStorageController:
    """Test suite for main storage controller"""
    
    def test_storage_controller_initialization(self):
        """Test StorageController initializes"""
        from storage.controller import StorageController
        
        controller = StorageController()
        assert controller is not None
        assert controller.offline_storage is not None
        assert controller.online_storage is not None
    
    def test_get_offline_controller(self):
        """Test getting offline storage controller"""
        from storage.controller import StorageController
        
        controller = StorageController()
        success, offline = controller.get_offline_storage_controller()
        
        assert success is True
        assert offline is not None
    
    def test_get_online_controller_fallback(self):
        """Test that online storage fails and falls back"""
        from storage.controller import StorageController
        
        controller = StorageController()
        success, storage = controller.get_online_storage_controller()
        
        # Should fallback to offline
        assert success is True
