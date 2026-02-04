from qfluentwidgets import (
    MSFluentWindow, setTheme, setThemeColor,
    Theme, FluentIcon
)

from .pages.dashboard import Dashboard


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
