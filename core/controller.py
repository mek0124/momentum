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
        
        return found_controller
    
    



if __name__ == '__main__':
    core_controller = CoreController()