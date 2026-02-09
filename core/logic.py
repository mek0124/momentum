from typing import Tuple, Optional, Union, List

from .models.task import Task


class MomentumLogic:
    def __init__(self, db):
        self.db = db

    def save_task(self, new_task: dict) -> Tuple[bool, str]:
        if not new_task:
            return True, "Task Object Cannot Be Empty"
        
        found_title = self.db.query(Task).filter(Task.title == new_task["title"]).first()

        if found_title:
            return True, "Title Already Exists"
        
        task_to_save = Task(
            title = new_task["title"],
            details = new_task["details"],
            priority = new_task["priority"]
        )
        
        try:
            self.db.add(task_to_save)
            self.db.commit()
            return False, "Task Saved Successfully"
        
        except Exception as e:
            print(f"Unknown Exception Saving Task: {e}")
            self.db.rollback()
            return True, "Failed to Save Task"
        
    def update_task(self, task_id: int, updated_task: dict) -> Tuple[bool, str]:
        if not task_id or not updated_task:
            return True, "Invalid Operation: Task ID and Task Info Cannot Be Empty"
        
        if not task_id:
            return True, "Task Id Cannot Be Empty"
        
        if not updated_task:
            return True, "Task Object Cannot Be Empty"
        
        found_task = self.db.query(Task).filter(Task.id == task_id).first()

        if not found_task:
            return True, f"No Task Found By Id: {task_id}"
        
        if found_task.title == updated_task["title"] and \
            found_task.details == updated_task["details"]:
            return False, "No Changes Made"
        
        try:
            self.db.query(Task).filter(Task.id == task_id).update(updated_task)
            self.db.commit()
            return True, "Task Updated Successfully"
        
        except Exception as e:
            print(f"Unknown Exception Updating Task: {e}")
            self.db.rollback()
            return False, "Failed to Update Task"
        
    def delete_task(self, task_id: int) -> Tuple[bool, str]:
        try:
            self.db.query(Task).filter(Task.id == task_id).delete()
            self.db.commit()
            return False, "Task Deleted Successfully"
        
        except Exception as e:
            print(f"Unknown Exception Deleting Task: {e}")
            self.db.rollback()
            return True, "Failed to Delete Task"
        
    def get_all_tasks(self) -> Union[List, None]:
        try:
            return self.db.query(Task).all()
        
        except Exception as e:
            print(f"Unknown Exception Retrieving All Tasks: {e}")
            self.db.rollback()
            return None
        
    def get_task_by_id(self, task_id) -> Union[Task, None]:
        try:
            return self.db.query(Task).filter(Task.id == task_id).first()
        
        except Exception as e:
            print(f"Unknown Exception Retrieving Task: {e}")
            self.db.rollback()
            return None