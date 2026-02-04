from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPixmap
from pathlib import Path

from app.app import Momentum
from app.database.db import get_base, get_engine, get_db
from app.models.task import Task

import sys


def run():
    app = QApplication(sys.argv)

    root_dir = Path(__file__).parent
    storage_dir = root_dir / "app" / "storage"
    storage_dir.mkdir(parents=True, exist_ok=True)

    get_base().metadata.create_all(bind=get_engine())

    db = next(get_db())

    window = Momentum(db)
    window.setWindowTitle("Momentum")
    window.setMinimumWidth(800)
    window.setMinimumHeight(600)
    window.setWindowIcon(QPixmap("./app/assets/icon.png"))
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    run()