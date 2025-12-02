from typing import Tuple, Union, List
from pathlib import Path
from datetime import datetime

import json


class Config:
    def __init__(self) -> None:
        self.curr_dir = Path(__file__).parent
        self.config_path = self.curr_dir / "config.json"
        self.config_data = self._load_config()

    def _load_config(self) -> dict:
        try:
            with open(self.config_path, 'r', encoding="utf-8-sig") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found at {self.config_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in config file: {self.config_path}")

    def get_config_file_path(self) -> Tuple[bool, Union[Path, str]]:
        try:
            config_file_path = self.curr_dir / "config.json"

            if not config_file_path.exists():
                with open(config_file_path, 'w+', encoding="utf-8-sig") as new:
                    json.dump([], new, indent=2)

                return True, config_file_path
            
            return True, config_file_path
        
        except Exception as e:
            return False, f"Failed to create config.json: {e}"
        
    def get_all_version_items(self, keyword: str) -> Tuple[bool, Union[List[dict], str]]:
        did_find_config, config_file_path = self.get_config_file_path()

        if not did_find_config:
            return False, config_file_path
        
        try:
            with open(config_file_path, 'r', encoding="utf-8-sig") as f:
                data = json.load(f)

            if keyword:
                return True, data[keyword]

            return True, data
        
        except Exception as e:
            return False, f"Failed to load version items from config.json: {e}"
        
    def create_new_version_item(self, new_version: dict) -> Tuple[bool, str]:
        config_found, config_path = self.get_config_file_path()

        if not config_found:
            return False, config_path
        
        if not new_version:
            return False, "New Task cannot be Empty"
        
        try:
            versions_loaded, current_version_list = self.get_all_version_items()

            if not versions_loaded:
                return False, current_version_list
            
            for current_version in current_version_list:
                if current_version["app_name"] == new_version["app_name"]:
                    return False, "App Name already exists"
                
            with open(config_path, 'r', encoding="utf-8-sig") as current:
                data = json.load(current)

            data.append(new_version)

            with open(config_path, 'w+', encoding="utf-8-sig") as updated:
                json.dump(data, updated, indent=2)

            return True, "Version Created Successfully"
        
        except Exception as e:
            return False, f"Failed to create new version: {e}"
        
    def update_version_item(self, version_id: int, updated_version: dict) -> Tuple[bool, str]:
        config_found, config_path = self.get_config_file_path()

        if not config_found:
            return False, config_path

        if not version_id:
            return False, "ID cannot be empty"
        
        if not updated_version:
            return False, "Updated Version cannot be empty"
        
        try:
            with open(config_path, 'r', encoding="utf-8-sig") as f:    
                all_versions = json.load(f)

                updated_name = updated_version.get("app_name")
                updated_version_str = updated_version.get("version")
                
                # Check if updated_at is provided, otherwise use current datetime
                if "updated_at" in updated_version:
                    updated_at = updated_version["updated_at"]
                else:
                    updated_at = datetime.now().__format__("%m/%d/%Y - %H:%M:%S")

                for index, version in enumerate(all_versions):
                    if version["id"] == version_id:
                        if updated_name is not None:
                            all_versions[index]["app_name"] = updated_name
                        if updated_version_str is not None:
                            all_versions[index]["version"] = updated_version_str
                        
                        all_versions[index]["updated_at"] = updated_at

                        with open(config_path, 'w+', encoding="utf-8-sig") as new:
                            json.dump(all_versions, new, indent=2)

                        return True, "Version Updated Successfully"
                    
                return False, f"Could Not Find Version By ID: {version_id}"
            
        except Exception as e:
            return False, f"Failed to update version: {e}"

    def delete_version_item(self, version_id: int) -> Tuple[bool, str]:
        config_found, config_path = self.get_config_file_path()

        if not config_found:
            return False, config_path

        if not version_id:
            return False, "ID cannot be empty"
        
        try:
            with open(config_path, 'r', encoding="utf-8-sig") as f:
                all_versions = json.load(f)

            # Find the index of the version with the given ID
            found_index = -1
            for index, version in enumerate(all_versions):
                if version.get("id") == version_id:
                    found_index = index
                    break

            if found_index == -1:
                return False, f"Could Not Find Version By ID: {version_id}"

            # Remove the item at the found index
            deleted_item = all_versions.pop(found_index)

            # Write the updated list back to the file
            with open(config_path, 'w+', encoding="utf-8-sig") as new:
                json.dump(all_versions, new, indent=2)

            return True, f"Successfully deleted version with ID: {version_id} (App: {deleted_item.get('app_name', 'Unknown')})"
        
        except Exception as e:
            return False, f"Failed to delete version: {e}"
    
    def get_database_config(self) -> dict:
        return self.config_data.get("database", {})
    
    def get_database_path(self) -> str:
        db_config = self.get_database_config()
        return db_config.get("path", "data/tasks.db")
    
    def get_database_type(self) -> str:
        db_config = self.get_database_config()
        return db_config.get("type", "sqlite")
    
    def get_online_storage_preference(self) -> bool:
        # update later
        return False

config = Config()
