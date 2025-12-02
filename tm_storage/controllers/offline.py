from typing import Tuple, Union, List
from tm_storage.database import db
from tm_core.models import Task
from sqlalchemy.exc import SQLAlchemyError


class OfflineStorageController:
    def __init__(self) -> None:
        self.db = db
    
    def create_task(self, task: Task) -> Tuple[bool, str]:
        try:
            session = self.db.get_session()
            
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
    
    def get_task_by_id(self, task_id: str) -> Tuple[bool, Union[dict, str]]:
        try:
            session = self.db.get_session()
            task = session.query(Task).filter(Task.id == task_id).first()
            session.close()

            if not task:
                return False, f"Failed to find task by id: {task_id}"

            return True, task.to_dict()

        except Exception as e:
            return False, f"Failed to retrieve task: {e}"
    
    def update_task(self, task: Task) -> Tuple[bool, str]:
        try:
            session = self.db.get_session()
            existing_task = session.query(Task).filter(Task.id == task.id).first()

            if not existing_task:
                session.close()
                return False, f"Task not found: {task.id}"

            existing_task.title = task.title
            existing_task.details = task.details
            existing_task.priority = task.priority
            existing_task.updated_at = task.updated_at
            existing_task.is_completed = task.is_completed

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