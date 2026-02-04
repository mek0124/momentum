from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QPixmap
from pathlib import Path

from app.app import Momentum
from app.database.db import get_base, get_engine, get_db
from app.models.task import Task

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



def run():
    app = QApplication(sys.argv)

    root_dir = Path(__file__).parent

    did_agree = check_perms(root_dir)

    if not did_agree:
        sys.exit(0)

    color_theme_path = root_dir / "app" / "utils" / "color_theme.json"

    with open(color_theme_path, 'r', encoding="utf-8-sig") as f:
        color_theme = json.load(f)

    db = next(get_db())

    window = Momentum(color_theme, db)
    window.setWindowTitle("Momentum")
    window.setMinimumWidth(800)
    window.setMinimumHeight(600)
    window.setWindowIcon(QPixmap("./app/assets/icon.png"))
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    run()