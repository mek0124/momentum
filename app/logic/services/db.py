from typing import List

from app.database.db import get_db

from ..models import Task


class DBServices:
    def __init__(self) -> None:
        self.db_gen = get_db()

        try:
            self.db = next(self.db_gen)

        except Exception:
            raise

    def get_all_tasks(self) -> List[Task] | None:
        try:
            tasks = self.db.query(Task).all()
            return tasks
        except:
            return None
    
    def save_task(self, task: Task) -> bool:
        try:
            if task.id:
                self.db.merge(task)
            
            else:
                self.db.add(task)
                
            self.db.commit()
            self.db.refresh(task)
            return True
            
        except Exception as e:
            self.db.rollback()
            print(f"Error saving task: {e}")
            return False
        
    def delete_task(self, task: Task) -> bool:
        try:
            self.db.delete(task)
            self.db.commit()
            return True
        
        except Exception as e:
            self.db.rollback()
            return False