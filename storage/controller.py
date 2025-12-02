import sys
from pathlib import Path
from typing import Tuple, Union, List

# add project root so imports work
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from controllers.offline import OfflineStorageController
from controllers.online import OnlineStorageController

import time


class StorageController:
    def __init__(self) -> None:
        self.offline_storage = OfflineStorageController()
        self.online_storage = OnlineStorageController()

    def get_storage_controller(self, online: bool = False) -> Tuple[bool, Union[OfflineStorageController, OnlineStorageController, str]]:
        if online:
            return self.get_online_storage_controller()
        else:
            return self.get_offline_storage_controller()

    def get_offline_storage_controller(self) -> Tuple[bool, Union[OfflineStorageController, str]]:
        try:
            return True, self.offline_storage
        
        except Exception as e:
            return False, f"Failed to get storage controller: {e}"
        
    def get_online_storage_controller(self) -> Tuple[bool, Union[OnlineStorageController, OfflineStorageController, str]]:
        tries = 5

        try:
            while tries > 0:
                controller_connected, response = self.online_storage.check_controller_connection()

                if controller_connected:
                    return True, self.online_storage

                print(f"Failed to Connect Online Controller: {response}")
                print(f"Tries remaining: {tries}: Trying Again...")
                tries -= 1

                if tries == 0:
                    break

                time.sleep(0.2)

            # If we get here, online connection failed after all tries
            print("Online storage failed after 5 attempts. Switching to offline storage.")
            return self.get_offline_storage_controller()

        except Exception as e:
            return False, f"Failed to get storage controller: {e}"
    
    def get_all_tasks(self, use_online_storage: bool = False) -> Tuple[bool, Union[List[dict], str]]:
        controller_found, controller_response = self.get_storage_controller(use_online_storage)

        if not controller_found:
            return False, controller_response
        
        return controller_response.get_all_tasks()
    
    def list_task_by_id(self, task_id: str, use_online_storage: bool = False) -> Tuple[bool, Union[dict, str]]:
        controller_found, controller_response = self.get_storage_controller(use_online_storage)

        if not controller_found:
            return False, controller_response
        
        return controller_response.list_task_by_id(task_id)
        
    def create_task(self, new_task: dict, use_online_storage: bool = False) -> Tuple[bool, str]:
        controller_found, controller_response = self.get_storage_controller(use_online_storage)

        if not controller_found:
            return False, f"Storage Controller Not Found: {controller_response}"
        
        return controller_response.create_task(new_task)
    
    def update_task(self, task_id: str, updated_task: dict, use_online_storage: bool = False) -> Tuple[bool, str]:
        controller_found, controller_response = self.get_storage_controller(use_online_storage)

        if not controller_found:
            return False, controller_response
        
        # Ensure task_id is in the updated_task dict
        updated_task["id"] = task_id
        return controller_response.update_task(updated_task)
    
    def delete_task(self, task_id: str, use_online_storage: bool = False) -> Tuple[bool, str]:
        controller_found, controller_response = self.get_storage_controller(use_online_storage)

        if not controller_found:
            return False, controller_response
        
        return controller_response.delete_task(task_id)

