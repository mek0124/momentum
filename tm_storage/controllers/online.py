from typing import Tuple, Union, List
from tm_core.models import Task  # Add this import


class OnlineStorageController:
    def __init__(self) -> None:
        pass

    def check_controller_connection(self) -> Tuple[bool, Union[object, str]]:
        return False, "Online Storage Controller Not Setup At This Time"

    def create_task(self, task: Task) -> Tuple[bool, str]:  # Changed parameter type
        return False, "Online storage not implemented"

    def get_all_tasks(self) -> Tuple[bool, Union[List[dict], str]]:  # Added return type
        return False, "Online storage not implemented"

    def list_task_by_id(self, task_id: str) -> Tuple[bool, Union[dict, str]]:  # Added return type
        return False, "Online storage not implemented"

    def update_task(self, task: Task) -> Tuple[bool, str]:  # Changed parameter type
        return False, "Online storage not implemented"

    def delete_task(self, task_id: str) -> Tuple[bool, str]:  # Added return type
        return False, "Online storage not implemented"