from uuid import uuid4
from datetime import datetime
from core.models.task import Task

class TestCoreModels:
    def test_task_default_values(self):
        task = Task(
            id=str(uuid4()),
            title="Test Task",
            details="",
            priority=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_completed=False
        )
        assert task.is_completed == 0
        assert task.details == ""

    def test_task_priority_levels(self):
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
