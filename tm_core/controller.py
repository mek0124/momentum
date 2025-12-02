import sys
from pathlib import Path

# add project root (parent of core/) so sibling package `storage` is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tm_storage.controller import StorageController
from tm_core.validators import Validators
from tm_core.models import Task
from typing import Tuple, Union, List
from uuid import uuid4
from datetime import datetime


class CoreController:
    def __init__(self) -> None:
        self.validators = Validators()
        self.storage_controller = StorageController()
        
    def set_storage_controller(self, use_online_storage: bool) -> Tuple[bool, Union[StorageController, str]]:
        controller_found, controller = self.storage_controller.get_storage_controller(use_online_storage)

        if not controller_found:
            return False, controller

        return True, controller
    
    def get_all_tasks(self, use_online_storage: bool) -> Tuple[bool, Union[List[dict], str]]:
        controller_found, controller = self.set_storage_controller(use_online_storage)

        if not controller_found:
            return False, controller

        return controller.get_all_tasks()
    
    def get_task_by_id(self, task_id: str, use_online_storage: bool) -> Tuple[bool, Union[dict, str]]:
        controller_found, controller = self.set_storage_controller(use_online_storage)

        if not controller_found:
            return False, controller

        if not self.validators.validate_id(task_id):
            return False, f"Invalid ID: {task_id}"

        return controller.get_task_by_id(task_id)

    def create_task(self, new_task: dict, use_online_storage: bool) -> Tuple[bool, str]:
        controller_found, controller = self.set_storage_controller(use_online_storage)

        if not controller_found:
            return False, controller

        if not new_task:
            return False, "New task cannot be empty"
        
        title_validated, title = self.validators.validate_title(new_task["title"])

        if not title_validated:
            return False, title
        
        details_validated, details = self.validators.validate_details(new_task["details"])

        if not details_validated:
            return False, details
        
        task_model = Task(
            id=str(uuid4()),
            title=new_task["title"],
            details=new_task.get("details", ""),
            priority=new_task["priority"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_completed=new_task.get("is_completed", 0),
        )

        return controller.create_task(task_model)

    def update_task(self, task_id: str, updated_task: dict, use_online_storage: bool) -> Tuple[bool, str]:
        controller_found, controller = self.set_storage_controller(use_online_storage)

        if not controller_found:
            return False, controller

        if not task_id:
            return False, "ID cannot be empty"

        if not updated_task:
            return False, "Updated task cannot be empty"

        if not self.validators.validate_id(task_id):
            return False, f"Invalid ID: {task_id}"

        task_found, task_response = self.get_task_by_id(task_id, use_online_storage)

        if not task_found:
            return False, task_response

        task_model = Task(
            id=task_id,
            title=updated_task.get("title", task_response.get("title")),
            details=updated_task.get("details", task_response.get("details", "")),
            priority=updated_task.get("priority", task_response.get("priority", 3)),
            created_at=task_response.get("created_at", datetime.now()),
            updated_at=datetime.now(),
            is_completed=updated_task.get("is_completed", task_response.get("is_completed", 0)),
        )

        return controller.update_task(task_model)

    def delete_task(self, task_id: str, use_online_storage: bool) -> Tuple[bool, str]:
        controller_found, controller = self.set_storage_controller(use_online_storage)

        if not controller_found:
            return False, controller

        if not self.validators.validate_id(task_id):
            return False, f"Invalid ID: {task_id}"

        return controller.delete_task(task_id)