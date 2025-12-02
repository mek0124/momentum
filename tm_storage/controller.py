from typing import Tuple, Union, List
from tm_storage.controllers.offline import OfflineStorageController
from tm_storage.controllers.online import OnlineStorageController
from tm_core.models import Task

import time


class StorageController:
    def __init__(self) -> None:
        self.offline_storage = OfflineStorageController()
        self.online_storage = OnlineStorageController()

    def get_storage_controller(self, online: bool) -> Tuple[bool, Union[OfflineStorageController, OnlineStorageController, str]]:
        if online:
            return self.get_online_storage_controller()
        else:
            return self.get_offline_storage_controller()

    def get_offline_storage_controller(self) -> Tuple[bool, Union[OfflineStorageController, str]]:
        return True, self.offline_storage

    def get_online_storage_controller(self) -> Tuple[bool, Union[OnlineStorageController, OfflineStorageController, str]]:
        tries = 5

        while tries > 0:
            controller_connected, response = self.online_storage.check_controller_connection()

            if controller_connected:
                return True, self.online_storage

            tries -= 1

            if tries == 0:
                break

            time.sleep(0.2)

        return True, self.offline_storage
    
    def get_all_tasks(self) -> Tuple[bool, Union[List[dict], str]]:
        controller_found, controller = self.get_storage_controller(False)

        if not controller_found:
            return False, controller

        return controller.get_all_tasks()
    
    def get_task_by_id(self, task_id: str) -> Tuple[bool, Union[dict, str]]:
        controller_found, controller = self.get_storage_controller(False)

        if not controller_found:
            return False, controller

        return controller.get_task_by_id(task_id)
        
    def create_task(self, task: Task) -> Tuple[bool, str]:
        controller_found, controller = self.get_storage_controller(False)

        if not controller_found:
            return False, controller

        return controller.create_task(task)  # Pass Task model
    
    def update_task(self, task: Task) -> Tuple[bool, str]:
        controller_found, controller = self.get_storage_controller(False)

        if not controller_found:
            return False, controller

        return controller.update_task(task)
    
    def delete_task(self, task_id: str) -> Tuple[bool, str]:
        controller_found, controller = self.get_storage_controller(False)

        if not controller_found:
            return False, controller

        return controller.delete_task(task_id)