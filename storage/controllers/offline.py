from typing import Tuple, Union, List
from pathlib import Path

import sqlite3 as sql
import os


class OfflineStorageController:
    def __init__(self) -> None:
        self.curr_dir = Path(__file__).parent

    def check_controller_connection(self) -> Tuple[bool, str]:
        try:
            storage_dir = self.curr_dir.parent
            data_dir = storage_dir / "data"

            if not data_dir.exists():
                os.makedirs(data_dir, exist_ok=True)

            db_file_path = data_dir / "tasks.db"

            if not db_file_path.exists():
                did_create, response = self.create_db(db_file_path)
                return did_create, response

            else:
                return True, "db file exists"

        except Exception as e:
            return False, f"Error Creating database file: {e}"

    def create_db(self, file_path: Path) -> Tuple[bool, str]:
        try:
            with sql.connect(file_path) as mdb:
                cur = mdb.cursor()

                cur.execute(
                    '''CREATE TABLE IF NOT EXISTS tasks(
                        id TEXT PRIMARY KEY NOT NULL,
                        title TEXT,
                        details TEXT,
                        priority INTEGER,
                        created_at TEXT,
                        updated_at TEXT,
                        is_completed INTEGER,
                        UNIQUE(id, title)
                    )'''
                )

            return True, "Database Created Successfully"

        except Exception as e:
            return False, f"Failed to create database: {e}"
        
    def create_task(self, new_task: dict) -> Tuple[bool, str]:
        db_file_path = self.curr_dir.parent / "data" / "tasks.db"

        try:
            with sql.connect(db_file_path) as mdb:
                cur = mdb.cursor()

                cur.execute(
                    '''INSERT INTO tasks(
                        id, 
                        title, 
                        details, 
                        priority, 
                        created_at, 
                        updated_at, 
                        is_completed
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (
                        new_task["id"],
                        new_task["title"],
                        new_task["details"],
                        new_task["priority"],
                        new_task["created_at"],
                        new_task["updated_at"],
                        new_task["is_completed"],
                    )
                )

                mdb.commit()

            return True, "Task Saved Successfully"
        
        except sql.Error as e:
            return False, f"Failed to create new task: {e}"

        except Exception as e:
            return False, f"Unknown Exception: {e}"
        
    def get_all_tasks(self) -> Tuple[bool, Union[List[tuple], str]]:
        db_file_path = self.curr_dir.parent / "data" / "tasks.db"

        try:
            with sql.connect(db_file_path) as mdb:
                cur = mdb.cursor()

            all_tasks = cur.execute('SELECT * FROM tasks').fetchall()

            if not all_tasks:
                return False, "Failed to load all tasks"

            return True, all_tasks
        
        except Exception as e:
            return False, f"Unknown Exception: {e}"
        
    def list_task_by_id(self, task_id) -> Tuple[bool, Union[dict, str]]:
        db_file_path = self.curr_dir.parent / "data" / "tasks.db"

        try:
            with sql.connect(db_file_path) as mdb:
                cur = mdb.cursor()

            results = cur.execute('SELECT * FROM tasks WHERE id=?', (task_id,)).fetchone()

            if not results:
                return False, f"Failed to find task by id: {task_id}"
            
            return True, results
        
        except Exception as e:
            return False, f"Unknown Exception: {e}"
        
    def update_task(self, updated_task: dict) -> Tuple[bool, str]:
        db_file_path = self.curr_dir.parent / "data" / "tasks.db"

        try:
            with sql.connect(db_file_path) as mdb:
                cur = mdb.cursor()

                cur.execute(
                    'UPDATE tasks SET title=?, details=?, priority=?, updated_at=?, is_completed=? WHERE id=?',
                    (
                        updated_task["title"],
                        updated_task["details"],
                        updated_task["priority"],
                        updated_task["updated_at"],
                        updated_task["is_completed"],
                        updated_task["id"],
                    )
                )

            return True, "Task Updated Successfully"
        
        except Exception as e:
            return False, f"Failed to update task: {e}"
        
    def delete_task(self, task_id) -> Tuple[bool, str]:
        db_file_path = self.curr_dir.parent / "data" / "tasks.db"

        try:
            with sql.connect(db_file_path) as mdb:
                cur = mdb.cursor()

                cur.execute(
                    'DELETE FROM tasks WHERE id=?',
                    (task_id,)
                )

            return True, "Task Deleted Successfully"
        
        except Exception as e:
            return False, f"Failed to delete task: {e}"
