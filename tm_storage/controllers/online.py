from typing import Tuple, Union


class OnlineStorageController:
    def __init__(self) -> None:
        pass

    def check_controller_connection(self) -> Tuple[bool, Union[object, str]]:
        return False, "Online Storage Controller Not Setup At This Time"

    def create_task(self, new_task: dict) -> Tuple[bool, str]:
        return False, "Online storage not implemented"

    def get_all_tasks(self):
        return False, "Online storage not implemented"

    def list_task_by_id(self, task_id: str):
        return False, "Online storage not implemented"

    def update_task(self, updated_task: dict):
        return False, "Online storage not implemented"

    def delete_task(self, task_id: str):
        return False, "Online storage not implemented"
