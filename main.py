from pathlib import Path
from typing import Tuple

from app.app import TaskManager
from app.database.db import Base, engine

import json
import sys
import os
import shutil
import time


def update_config_read_write(file_path: Path) -> Tuple[bool, str]:
    try:
        with open(file_path, 'r', encoding="utf-8-sig") as cf:
            data = json.load(cf)

        data["rw_agree"] = 1

        with open(file_path, 'w+', encoding="utf-8-sig") as ucf:
            json.dump(data, ucf, indent=2)

        Base.metadata.create_all(bind=engine)

        return True
    
    except FileNotFoundError:
        with open(file_path, 'w+', encoding="utf-8-sig") as nf:
            json.dump({"rw_agree": 0}, nf, indent=2)

        return update_config_read_write(file_path)

    except Exception as e:
        print(f"\nUnknown Exception: Creating UA File: {e}")
        return False
    
def display_file(file_path: Path):
    os.system('cls' if os.name == 'nt' else 'clear')
    time.sleep(0.1)
    
    with open(file_path, 'r') as agreement_file:
        text = agreement_file.read()
    
    try:
        terminal_size = shutil.get_terminal_size()
        terminal_height = terminal_size.lines
    except:
        terminal_height = 24
    
    lines = text.split("\n")
    line_index = 0
    total_lines = len(lines)
    
    lines_per_page = max(1, terminal_height - 4)
    total_pages = (total_lines + lines_per_page - 1) // lines_per_page
    
    current_page = 1
    
    while line_index < total_lines:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        for i in range(lines_per_page):
            if line_index + i < total_lines:
                print(lines[line_index + i])
            else:
                print()
        
        line_index += lines_per_page
        
        if line_index < total_lines:
            print("\n" + "=" * 50)
            input(f"{current_page}/{total_pages} - Press Enter to continue...")
            current_page += 1
        else:
            print("\n" + "=" * 50)
            input(f"{current_page}/{total_pages} - Press Enter to finish...")

def get_perms(config_json: Path, agreement_text_file: Path) -> bool:
    display_file(agreement_text_file)

    user_agree = input("\nDo You Agree? (Y/N): ").lower().strip()

    while not user_agree in ['y', 'n']:
        print("\nInvalid Input. Options are 'Y' for Yes or 'N' for No\n")
        
        user_agree = input("\nDo You Agree? (Y/N): ").lower().strip()

        if user_agree in ['y', 'n']:
            break

    match user_agree:
        case "y":
            return update_config_read_write(config_json)

        case "n":
            return False

def check_for_perms() -> bool:
    curr_dir = Path(__file__).parent
    data_dir = curr_dir / "app" / "data"

    try:
        config_json = data_dir / "config.json"
        agreement_text_file = data_dir / "agreement_text.txt"

        if not config_json.exists():
            return get_perms(config_json, agreement_text_file)
        else:
            with open(config_json, 'r', encoding="utf-8-sig") as cf:
                data = json.load(cf)

            if data["rw_agree"] == 0:
                return get_perms(config_json, agreement_text_file)
            
            return True
        
    except Exception as e:
        print(f"\nUnknown Exception: {e}")
        return False


if __name__ == '__main__':
    did_agree = check_for_perms()

    if not did_agree:
        print("\nYou denied the read/write permissions. Exiting application...")
        sys.exit(1)

    app = TaskManager()
    app.run()