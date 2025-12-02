import sys
from pathlib import Path

# add project root (parent of core/) so sibling package `storage` is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from storage.controller import StorageController

from typing import Tuple, Union


class CoreController:
    def __init__(self) -> None:
        self.storage_controller = self.set_storage_controller()
        
    def set_storage_controller(self) -> Tuple[bool, Union[StorageController, str]]:
        storage_controller_class = StorageController()

        controller_found, found_controller = storage_controller_class.get_storage_controller()
        
        if not controller_found:
            return False, found_controller
        
        return True, found_controller


if __name__ == '__main__':
    core_controller = CoreController()
    found_controller, response = core_controller.set_storage_controller()

    from datetime import datetime
    from uuid import uuid4

    if not found_controller:
        raise Exception(response)
    
    new_task = {
        "id": str(uuid4()),
        "title": "An example title6546084",
        "details": "some exampe details464565",
        "priority": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "is_completed": False
    }

    did_save, response = response.update_task(new_task)

    if not did_save:
        raise Exception(response)
    
    print(response)