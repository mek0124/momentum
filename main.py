from PySide6.QtWidgets import QApplication, QMessageBox
from pathlib import Path

from app.app import Momentum
from app.database.db import get_base, get_engine, get_db
from app.models.task import Task
from app.utils.color_theme import COLOR_THEME

from updater.app import Updater

import tomllib
import requests
import json
import sys


def update_config_file(ua_file: Path) -> bool:
    storage_folder = ua_file.parent
    storage_folder.mkdir(parents=True, exist_ok=True)

    get_base().metadata.create_all(bind=get_engine())
    
    try:
        if not ua_file.exists():
            data = {"read_write_perm": 1, "use_browser": 1}
        else:
            with open(ua_file, 'r', encoding="utf-8-sig") as curr_agree:
                data = json.load(curr_agree)
            data["read_write_perm"] = 1
            data["use_browser"] = 1
        
        with open(ua_file, 'w', encoding="utf-8-sig") as updated_agree:
            json.dump(data, updated_agree, indent=2)
        
        return True
    
    except Exception as e:
        print(f"Unknown Exception: {e}")
        return False


def get_read_write_perms() -> bool:
    try:
        rw_agreement = QMessageBox.question(
            None,
            "Read/Write Permissions",
            "This application requires read/write permissions to maintain " \
            "its own database. Do you agree to allow this application to " \
            "have read/write permissions?\n\n**NOTE: This application does " \
            "not read/write to any files outside of its own codebase!**",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )

        if rw_agreement == QMessageBox.No or rw_agreement == QMessageBox.Rejected:
            QMessageBox.warning(
                None,
                "Read/Write Permissions - Denied",
                "You denied read/write permissions for this application. This " \
                "application cannot run without these permissions. If you change " \
                "your mind, run the application again."
            )
            return False
                
        return True
    
    except Exception as e:
        print(f"Unknown Exception: {e}")
        return False
    

def get_browser_usage_agreement() -> bool:
    try:
        browser_agree = QMessageBox.question(
            None,
            "Browser Usage Permissions",
            "This application requires permission to use your browser to open and " \
            "display pages like 'About The App' and 'About The Developer' and 'Support'. " \
            "Do you agree to allow this application to use your browser only when you " \
            "click to open these pages?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )

        if browser_agree == QMessageBox.No or browser_agree == QMessageBox.Rejected:
            QMessageBox.warning(
                None,
                "Browser Usage Permissions - Denied",
                "You denied browser usage permissions for this application. " \
                "This application requires browser usage permissions in order " \
                "to properly run and allow you to obtain support when needed. " \
                "If you change your mind, run the application again."
            )
            return False
        
        return True
    
    except Exception as e:
        print(f"Unknown Exception: {e}")
        return False


def get_user_agreement(root_dir: Path) -> bool:
    ua_file = root_dir / "app" / "storage" / "config.json"
    
    rw_agree = get_read_write_perms()
    if not rw_agree:
        return False
    
    browser_agree = get_browser_usage_agreement()
    if not browser_agree:
        return False
    
    did_update = update_config_file(ua_file)
    return did_update


def check_perms(root_dir: Path) -> bool:
    ua_file = root_dir / "app" / "storage" / "config.json"
    
    try:
        if not ua_file.exists():
            return get_user_agreement(root_dir)
        
        with open(ua_file, 'r', encoding="utf-8-sig") as f:
            data = json.load(f)
        
        rw_perm = data.get("read_write_perm", 0)
        browser_perm = data.get("use_browser", 0)
        
        if rw_perm == 0 or browser_perm == 0:
            return get_user_agreement(root_dir)
        
        return True
        
    except json.JSONDecodeError:
        return get_user_agreement(root_dir)
    except Exception as e:
        print(f"Unknown Exception: {e}")
        return False
    

def run_main():
    db = next(get_db())

    window = Momentum(COLOR_THEME, db)
    window.setMinimumWidth(800)
    window.setMinimumHeight(600)
    window.show()

    sys.exit(app.exec())


def get_latest_version_from_repo():
    repo_api = "https://api.github.com/repos/mek0124/momentum/releases/latest"

    try:
        response = requests.get(repo_api)
        response.raise_for_status()

        data = response.json()
        latest_version = data.get("tag_name", "").lstrip("v")
        return latest_version
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching version from GitHub: {e}")
        return None
    
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing GitHub response: {e}")
        return None


def check_for_update(root_dir: Path) -> bool:
    pyproject_toml_path = root_dir / "pyproject.toml"

    with open(pyproject_toml_path, 'rb') as file:
        data = tomllib.load(file)

    if "project" in data and "version" in data["project"]:
        local_version = data["project"]["version"]

    latest_version = get_latest_version_from_repo()

    return True, local_version, latest_version \
        if \
        latest_version != local_version \
        else \
        False


def run_updater(root_dir, local_version, latest_version):
    window = Updater(root_dir, COLOR_THEME, local_version, latest_version)
    window.setMinimumWidth(800)
    window.setMinimumHeight(600)
    window.show()

    sys.exit(app.exec())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    root_dir = Path(__file__).parent
    did_agree = check_perms(root_dir)
    
    if not did_agree:
        sys.exit(0)

    update_ready, local_version, latest_version = check_for_update(root_dir)

    if update_ready:
        run_updater(root_dir, local_version, latest_version)
    
    else:
        run_main()