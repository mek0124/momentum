from typing import Tuple, Union, List
from tm_storage.database import db
from tm_core.models import Task
from sqlalchemy.exc import SQLAlchemyError


class OfflineStorageController:
    def __init__(self) -> None:
        self.db = db
    
    def create_task(self, new_task: dict) -> Tuple[bool, str]:
        try:
            session = self.db.get_session()
            task = Task(
                id=new_task["id"],
                title=new_task["title"],
                details=new_task.get("details", ""),
                priority=new_task["priority"],
                created_at=new_task["created_at"],
                updated_at=new_task["updated_at"],
                is_completed=new_task.get("is_completed", 0),
            )

            session.add(task)
            session.commit()
            session.close()

            return True, "Task Saved Successfully"

        except SQLAlchemyError as e:
            return False, f"Failed to create new task: {e}"

        except Exception as e:
            return False, f"Unknown Exception: {e}"
    
    def get_all_tasks(self) -> Tuple[bool, Union[List[dict], str]]:
        try:
            session = self.db.get_session()
            tasks = session.query(Task).all()
            session.close()

            if not tasks:
                return False, "No tasks found"

            return True, [task.to_dict() for task in tasks]

        except Exception as e:
            return False, f"Failed to get all tasks: {e}"
    
    def list_task_by_id(self, task_id: str) -> Tuple[bool, Union[dict, str]]:
        try:
            session = self.db.get_session()
            task = session.query(Task).filter(Task.id == task_id).first()
            session.close()

            if not task:
                return False, f"Failed to find task by id: {task_id}"

            return True, task.to_dict()

        except Exception as e:
            return False, f"Failed to retrieve task: {e}"
    
    def update_task(self, updated_task: dict) -> Tuple[bool, str]:
        try:
            session = self.db.get_session()
            task = session.query(Task).filter(Task.id == updated_task["id"]).first()

            if not task:
                session.close()
                return False, f"Task not found: {updated_task['id']}"

            task.title = updated_task["title"]
            task.details = updated_task.get("details", "")
            task.priority = updated_task["priority"]
            task.updated_at = updated_task["updated_at"]
            task.is_completed = updated_task.get("is_completed", 0)

            session.commit()
            session.close()

            return True, "Task Updated Successfully"

        except Exception as e:
            return False, f"Failed to update task: {e}"
    
    def delete_task(self, task_id: str) -> Tuple[bool, str]:
        try:
            session = self.db.get_session()
            task = session.query(Task).filter(Task.id == task_id).first()

            if not task:
                session.close()
                return False, f"Task not found: {task_id}"

            session.delete(task)
            session.commit()
            session.close()

            return True, "Task Deleted Successfully"

        except Exception as e:
            return False, f"Failed to delete task: {e}"
