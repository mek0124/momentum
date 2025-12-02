import sys
from pathlib import Path

# add project root (parent of core/) so sibling package `storage` is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tm_storage.controller import StorageController
from tm_core.validators import Validators
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

        return controller.get_all_tasks(use_online_storage)
    
    def get_task_by_id(self, task_id: str, use_online_storage: bool) -> Tuple[bool, Union[dict, str]]:
        controller_found, controller = self.set_storage_controller(use_online_storage)

        if not controller_found:
            return False, controller

        if not self.validators.validate_id(task_id):
            return False, f"Invalid ID: {task_id}"

        return controller.get_task_by_id(task_id, use_online_storage)

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
        
        new_task["id"] = str(uuid4())
        new_task["created_at"] = datetime.now()
        new_task["updated_at"] = datetime.now()

        return controller.create_task(new_task, use_online_storage)

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

        return controller.update_task(task_id, updated_task, use_online_storage)

    def delete_task(self, task_id: str, use_online_storage: bool) -> Tuple[bool, str]:
        controller_found, controller = self.set_storage_controller(use_online_storage)

        if not controller_found:
            return False, controller

        if not self.validators.validate_id(task_id):
            return False, f"Invalid ID: {task_id}"

        return controller.delete_task(task_id, use_online_storage)
