from qfluentwidgets import (
    MSFluentWindow, setTheme, setThemeColor,
    Theme, FluentIcon
)
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPixmap
from pathlib import Path

from .pages.dashboard import Dashboard

from core.logic import Logic
from core.utils.color_theme import COLOR_THEME

import sys


class Momentum(MSFluentWindow):
    def __init__(self, color_theme, logic):
        super().__init__()

        self.color_theme = color_theme
        self.logic = logic
        self.dashboard = Dashboard(self)

        self.set_app_theme()
        self.init_navigation()

    def set_app_theme(self):
        setTheme(Theme.DARK)
        setThemeColor(self.color_theme['primary'])

        self.setStyleSheet(
            f"background-color: {self.color_theme['background']};"
        )

    def init_navigation(self):
        self.addSubInterface(self.dashboard, FluentIcon.HOME, "Dashboard")

    def closeEvent(self, event):
        event.accept()


def main():
    app = QApplication(sys.argv)
    app_dir = Path.home() / ".momentum"

    logic = Logic(app_dir)

    window = Momentum(COLOR_THEME, logic)
    window.setWindowTitle("Momentum")
    window.setWindowIcon(QPixmap("./core/assets/icon.png"))
    window.setMinimumWidth(800)
    window.setMinimumHeight(600)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()