from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QPixmap
from pathlib import Path

from app.app import Momentum
from app.core.logic import MomentumLogic
from app.database.db import get_base, get_engine, get_db
from app.models.task import Task

from updater.app import Updater

import tomllib
import json
import sys


def update_config_file(ua_file: Path) -> bool:
    storage_folder = ua_file.parent
    storage_folder.mkdir(parents=True, exist_ok=True)
    
    try:
        if not ua_file.exists():
            data = {"read_write_perm": 1}
        else:
            with open(ua_file, 'r', encoding="utf-8-sig") as curr_agree:
                data = json.load(curr_agree)
            data["read_write_perm"] = 1
        
        with open(ua_file, 'w', encoding="utf-8-sig") as updated_agree:
            json.dump(data, updated_agree, indent=2)

        get_base().metadata.create_all(bind=get_engine())
        
        return True
    
    except Exception as e:
        print(f"Unknown Exception: {e}")
        return False


def get_read_write_perms() -> bool:
    try:
        rw_agreement = QMessageBox.question(
            None,
            "Read/Write Permissions",
            "This application requires read/write permissions to maintain its own database. Do you agree to allow this application to have read/write permissions?\n\n**NOTE: This application does not read/write to any files outside of its own codebase!**",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )

        if rw_agreement == QMessageBox.No or rw_agreement == QMessageBox.Rejected:
            QMessageBox.warning(
                None,
                "Read/Write Permissions - Denied",
                "You denied read/write permissions for this application. This application cannot run without these permissions. If you change your mind, run the application again."
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
        
        if rw_perm == 0:
            return get_user_agreement(root_dir)
        
        return True
        
    except json.JSONDecodeError:
        return get_user_agreement(root_dir)
    except Exception as e:
        print(f"Unknown Exception: {e}")
        return False


def run_main():
    """
    A function that handles displaying the main application
    window to the user for user interaction
    """
    app = QApplication(sys.argv)
    root_dir = Path(__file__).parent
    did_agree = check_perms(root_dir)

    if not did_agree:
        sys.exit(0)

    color_theme_path = root_dir / "app" / "utils" / "color_theme.json"

    with open(color_theme_path, 'r', encoding="utf-8-sig") as f:
        color_theme = json.load(f)

    db = next(get_db())
    logic = MomentumLogic(db)

    window = Momentum(color_theme, logic)
    window.setWindowTitle("Momentum")
    window.setMinimumWidth(800)
    window.setMinimumHeight(600)
    window.setWindowIcon(QPixmap("./app/assets/icon.png"))
    window.show()

    sys.exit(app.exec())


def run_updater():
    """
    A function that handles displaying the Updater
    window to notify the user that update is available.

    - buttons
        - update notes
            - navigates from dashboard to update notes screen
        - cancel
            - exits the updater application so that the main application can run
        - update
            - updates the application to the newest version
    """
    app = QApplication(sys.argv)
    root_dir = Path(__file__).parent
    color_theme_path = root_dir / "updater" / "utils" / "color_theme.json"
    pyproject_toml_path = root_dir / "pyproject.toml"

    with open(color_theme_path, 'r', encoding="utf-8-sig") as f:
        color_theme = json.load(f)

    with open(pyproject_toml_path, 'rb') as file:
        pyproject_data = tomllib.load(file)

        if "project" in pyproject_data and "version" in pyproject_data["project"]:
            curr_version = pyproject_data["project"]["version"]

    new_version = "0.0.0"

    window = Updater(color_theme, new_version, curr_version)
    window.setWindowTitle("Momentum - Updater")
    window.setMinimumWidth(800)
    window.setMinimumHeight(600)
    window.setWindowIcon(QPixmap("./app/assets/icon.png"))
    window.show()

    sys.exit(app.exec())


def check_for_update(self):
    """
    A function that handles querying the lates releases version
    from the github repo, compares that version to the version
    that is in the pyproject.toml file. If the latest version
    does not match the version in the pyproject.toml file, then
    return True for an update to exist. If the two version numbers
    match, then return False for no update available.
    """
    github_repo_route = "https://github.com/mek0124/momentum"
    return True


# def run():
#     """
#     A function to handle checking if an update is available

#     - True
#         - run_updater()
#         - run_main()
#     - False
#         - run_main()

#     if an update exists, run the updater application. when the
#     user clicks Update and the updates finishes, or when the user
#     clicks the cancel button, the updater application should exit
#     and the main application should run.
#     """
#     update_available = check_for_update()

#     if update_available:
#         run_updater()
#         run_main()
    
#     else:
#         run_main()


if __name__ == '__main__':
    # run()

    run_main()