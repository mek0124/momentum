from qfluentwidgets import (
    MSFluentWindow, setTheme, setThemeColor,
    Theme, FluentIcon
)

from .pages.dashboard import Dashboard
from .utils.color_theme import COLOR_THEME


class Momentum(MSFluentWindow):
    def __init__(self, color_theme, db):
        super().__init__()

        self.color_theme = color_theme
        self.db = db
        self.dashboard = Dashboard(self)

        self.set_app_theme()
        self.init_navigation()

    def set_app_theme(self):
        setTheme(Theme.DARK)
        setThemeColor(COLOR_THEME['primary'])

        self.setStyleSheet(
            f"background-color: {COLOR_THEME['background']};"
        )

    def init_navigation(self):
        self.addSubInterface(self.dashboard, FluentIcon.HOME, "Dashboard")

    def closeEvent(self, event):
        self.db.close()
        event.accept()
