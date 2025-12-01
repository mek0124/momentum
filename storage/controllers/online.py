from typing import Tuple, Union


class OnlineStorageController:
    def __init__(self) -> None:
        pass

    def check_controller_connection(self) -> Tuple[bool, Union[object, str]]:
        return False, "Online Storage Controller Not Setup At This Time"