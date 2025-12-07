from typing import List
from datetime import datetime

from .models.task import Task
from .services.db import DBServices


class LogicGate:
    def __init__(self) -> None:
        self.db_service = DBServices()

    def get_current_tasks(self) -> List:
        try:
            all_tasks = self.db_service.get_all_tasks()
            if all_tasks is None:
                return []
            return [task for task in all_tasks if task.is_completed == False]

        except Exception as e:
            print(f"Unknown Exception Retrieving Tasks: {e}")
            return []
        
    def get_all_tasks(self) -> List:
        try:
            all_tasks = self.db_service.get_all_tasks()

            if all_tasks is None:
                return []
            
            return [task for task in all_tasks]
        
        except Exception as e:
            print(f"Unknown Exception Retrieving Tasks: {e}")
            return []

    def create_task(self, new_task: dict) -> str:
        try:
            all_tasks = self.db_service.get_all_tasks()

            if all_tasks is None:
                all_tasks = []

            found_task = [task for task in all_tasks if task.title == new_task["title"]]

            if found_task:
                return "Title Already Exists"
            
            due_by_datetime = None
            
            if new_task["due_by"]:
                try:
                    due_by_datetime = datetime.strptime(new_task["due_by"], "%m/%d/%Y %H:%M")
            
                except ValueError:
                    return "Invalid date format. Use mm/dd/yyyy hh:mm"
            
            save_task = Task(
                title = new_task["title"],
                details = new_task["details"],
                due_by = due_by_datetime,
                priority = new_task["priority"],
            )

            did_save = self.db_service.save_task(save_task)

            if not did_save:
                return "Failed Saving New Task"
            
            return "Saved New Task Successfully"

        except Exception as e:
            return f"Exception Creating Task in Logic Gate: {e}"
        
    def delete_task_by_id(self, task_id: str) -> str:
        try:
            all_tasks = self.db_service.get_all_tasks()

            if not all_tasks:
                return "No Tasks Currently Exist"
            
            found_task = None

            for task in all_tasks:
                if str(task.id) == task_id:
                    found_task = task

            if not found_task:
                return f"No Task Found with ID: {task_id}"
            
            did_delete = self.db_service.delete_task(found_task)

            if not did_delete:
                return "Failed to delete task"
            
            return "Task deleted successfully"
        
        except Exception as e:
            return f"Exception Deleting Task in Logic Gate: {e}"
        
    def update_task(self, task_id: str, updated_task: dict) -> str:
        try:
            all_tasks = self.db_service.get_all_tasks()

            if not all_tasks:
                return "No Tasks Currently Exist"
            
            found_task = None

            for task in all_tasks:
                if str(task.id) == task_id:
                    found_task = task
                    break

            if not found_task:
                return f"No Task Found with ID: {task_id}"
            
            # Check if title is unique (excluding the current task)
            if updated_task["title"] != found_task.title:
                existing_title = [task for task in all_tasks if task.title == updated_task["title"]]
                if existing_title:
                    return "Title Already Exists"
            
            # Update the task
            found_task.title = updated_task["title"]
            found_task.details = updated_task["details"]
            found_task.priority = updated_task["priority"]
            
            # Update due_by if provided
            due_by_datetime = None
            if updated_task["due_by"]:
                try:
                    due_by_datetime = datetime.strptime(updated_task["due_by"], "%m/%d/%Y %H:%M")
                except ValueError:
                    return "Invalid date format. Use mm/dd/yyyy hh:mm"
            found_task.due_by = due_by_datetime
            
            # Save the updated task
            did_save = self.db_service.save_task(found_task)
            if not did_save:
                return "Failed Updating Task"
            
            return "Task Updated Successfully"
            
        except Exception as e:
            return f"Exception Updating Task in Logic Gate: {e}"