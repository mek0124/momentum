import sys
from pathlib import Path
import pytest
import tempfile
import shutil
from datetime import datetime
from uuid import uuid4
import os
import storage.database as sdb
from storage.database import Database

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class TestOfflineStorageController:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test_tasks.db"
        import storage.database as sdb
        from storage.database import Database
        sdb.db = Database(db_path=str(self.db_path))

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        sdb.db = Database()

    def test_create_task(self):
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
        controller.create_task(new_task)
        success, tasks = controller.get_all_tasks()
        assert success is True
        assert isinstance(tasks, list)
        assert len(tasks) > 0

    def test_get_task_by_id(self):
        from storage.controllers.offline import OfflineStorageController
        controller = OfflineStorageController()
        task_id = str(uuid4())
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
        success, task = controller.list_task_by_id(task_id)
        assert success is True
        assert task["id"] == task_id
        assert task["title"] == "Test Task"

    def test_update_task(self):
        from storage.controllers.offline import OfflineStorageController
        controller = OfflineStorageController()
        task_id = str(uuid4())
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
        _, task = controller.list_task_by_id(task_id)
        assert task["title"] == "Updated Title"

    def test_delete_task(self):
        from storage.controllers.offline import OfflineStorageController
        controller = OfflineStorageController()
        task_id = str(uuid4())
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
        success, message = controller.delete_task(task_id)
        assert success is True
        assert message == "Task Deleted Successfully"
        success, _ = controller.list_task_by_id(task_id)
        assert success is False

    def test_create_task_with_missing_id(self):
        from storage.controllers.offline import OfflineStorageController
        controller = OfflineStorageController()
        new_task = {
            "title": "Test Task",
            "details": "",
            "priority": 1,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        success, message = controller.create_task(new_task)
        assert success is False

class TestStorageController:
    def test_storage_controller_initialization(self):
        from storage.controller import StorageController
        controller = StorageController()
        assert controller is not None
        assert controller.offline_storage is not None
        assert controller.online_storage is not None

    def test_get_offline_controller(self):
        from storage.controller import StorageController
        controller = StorageController()
        success, offline = controller.get_offline_storage_controller()
        assert success is True
        assert offline is not None

    def test_get_online_controller_fallback(self):
        from storage.controller import StorageController
        controller = StorageController()
        success, storage = controller.get_online_storage_controller()
        assert success is True
