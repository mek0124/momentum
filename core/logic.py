from typing import Tuple, Union, List
from pathlib import Path

import json
import sys
import os

from .database.db import get_db, get_engine, get_base
from .models.task import Task


class Logic:
    def __init__(self, app_dir: Path):
        self.app_dir = app_dir
        self.config_file = app_dir / "config.json"
        self.setup_environment()

    def setup_environment(self):
        self.app_dir.mkdir(parents=True, exist_ok=True)

        try:
            with open(self.config_file, 'r', encoding="utf-8-sig") as f:
                data = json.load(f)

            if data.get("agree") != 1:
                self.get_user_agreement()

        except FileNotFoundError:
            self.get_user_agreement()

        except (KeyError, json.JSONDecodeError):
            if self.config_file.exists():
                os.remove(self.config_file)

            self.get_user_agreement()

        self.init_db()

    def init_db(self):
        get_base().metadata.create_all(bind=get_engine())

    def get_user_agreement(self):
        print(
            "Momentum requires read/write permissions to create and "
            "maintain the database that holds your tasks. This "
            "application cannot run without this permission."
        )

        user_agree = input("\nDo you agree? (Y/N): ")

        while user_agree.lower() not in ['y', 'n', 'yes', 'no']:
            print("\nInvalid Input. Input Must Be 'Y' for Yes or 'N' for No")
            user_agree = input("\nDo you agree? (Y/N): ")

        match user_agree.lower():
            case 'y' | 'yes':
                self.update_user_config()

            case 'n' | 'no':
                print(
                    "\nYou declined the user agreement. This application "
                    "cannot run without this permission. If you change "
                    "your mind later, run any command again"
                )
                sys.exit(0)

    def update_user_config(self):
        try:
            with open(self.config_file, 'w', encoding="utf-8-sig") as new:
                json.dump({"agree": 1}, new, indent=2)

        except FileExistsError:
            with open(self.config_file, 'w+', encoding="utf-8-sig") as new:
                json.dump({"agree": 1}, new, indent=2)

        except (KeyError, json.JSONDecodeError):
            if self.config_file.exists():
                os.remove(self.config_file)

            with open(self.config_file, 'w+', encoding="utf-8-sig") as new:
                json.dump({"agree": 1}, new, indent=2)

    def save_task(self, title: str, content: str) -> Tuple[bool, str]:
        db = next(get_db())

        if not title and not content:
            return False, "Title and Content are Requried"
        
        found_title = db.query(Task).filter(Task.title == title).first()

        if found_title:
            return False, "Title Already Exists"
        
        task_to_save = Task(
            title = title,
            content = content
        )
        
        try:
            db.add(task_to_save)
            db.commit()
            return True, "Task Saved Successfully"
        
        except Exception as e:
            print(f"Unknown Exception Saving Task: {e}")
            db.rollback()
            return False, "Failed to Save Task"
        
    def update_task(self, task_id: int, new_title: str = None, new_content: str = None) -> Tuple[bool, str]:
        db = next(get_db())

        if not new_title and not new_content:
            return False, "Title and Content cannot both be empty"
        
        if not task_id:
            return False, "Task Id Cannot Be Empty"
        
        found_task = db.query(Task).filter(Task.id == task_id).first()

        if not found_task:
            return False, f"No Task Found By Id: {task_id}"
        
        if new_title:
            found_task.title = new_title

        if new_content:
            found_task.content = new_content

        try:
            db.commit()
            db.refresh(found_task)
            return True, "Task Updated Successfully"
        
        except Exception as e:
            print(f"Unknown Exception Updating Task: {e}")
            db.rollback()
            return False, "Failed to Update Task"
        
    def delete_task(self, task_id: int) -> Tuple[bool, str]:
        db = next(get_db())

        if not task_id:
            return False, "Task ID cannot be empty"
        
        found_task = db.query(Task).filter(Task.id == task_id).first()

        if not found_task:
            return False, f"No task found by ID: {task_id}"
        
        try:
            db.delete(found_task)
            db.commit()
            return True, "Task Deleted Successfully"
        
        except Exception as e:
            print(f"Unknown Exception Deleting Task: {e}")
            db.rollback()
            return False, "Failed to Delete Task"
        
    def get_all_tasks(self) -> Union[List, None]:
        db = next(get_db())
        return db.query(Task).all()
        
    def get_task_by_id(self, task_id) -> Union[Task, None]:
        db = next(get_db())
        return db.query(Task).filter(Task.id == task_id).first()