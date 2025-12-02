import sys
from pathlib import Path
import pytest
from datetime import datetime
from uuid import uuid4

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.models import Task

class TestCoreModels:
    """Test suite for core models"""
    
    def test_task_model_creation(self):
        """Test creating a Task model instance"""
        task_id = str(uuid4())
        task = Task(
            id=task_id,
            title="Test Task",
            details="Test Details",
            priority=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_completed=0
        )
        
        assert task.id == task_id
        assert task.title == "Test Task"
        assert task.details == "Test Details"
        assert task.priority == 1
        assert task.is_completed == 0
    
    def test_task_to_dict(self):
        """Test converting Task to dictionary"""
        task_id = str(uuid4())
        now = datetime.now()
        task = Task(
            id=task_id,
            title="Test Task",
            details="Test Details",
            priority=2,
            created_at=now,
            updated_at=now,
            is_completed=0
        )
        
        task_dict = task.to_dict()
        
        assert isinstance(task_dict, dict)
        assert task_dict["id"] == task_id
        assert task_dict["title"] == "Test Task"
        assert task_dict["priority"] == 2
    
    def test_task_default_values(self):
        """Test Task model default values"""
        task = Task(
            id="test-id",
            title="Test",
            details = "",
            priority=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_completed=False
        )
        
        assert task.is_completed == 0
        assert task.details == ""
    
    def test_task_priority_levels(self):
        """Test different priority levels"""
        for priority in [1, 2, 3]:
            task = Task(
                id=str(uuid4()),
                title="Test",
                priority=priority,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                is_completed=False
            )
            assert task.priority == priority
