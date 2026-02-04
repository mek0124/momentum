from qfluentwidgets import (
    MSFluentWindow,
    FluentIcon as fi,
    setTheme,
    setThemeColor,
    Theme
)

from .pages.dashboard import Dashboard
from .pages.update_notes import UpdateNotes


class Updater(MSFluentWindow):
    def __init__(self, color_theme, new_version, curr_version):
        super().__init__()

        self.color_theme = color_theme
        self.new_version = new_version
        self.curr_version = curr_version

        self.dashboard = Dashboard(self)
        self.update_notes = UpdateNotes(self)

        self.set_app_theme()
        self.init_navigation()

    def set_app_theme(self):
        setTheme(Theme.DARK)
        setThemeColor(self.color_theme['primary'])

        self.setStyleSheet(
            f"""
                MSFluentWindow {{
                    background-color: {self.color_theme['background']};
                }}
            """
        )

    def init_navigation(self):
        self.addSubInterface(self.dashboard, fi.APPLICATION, "Dashboard")
        self.addSubInterface(self.update_notes, fi.QUICK_NOTE, "Update Notes")

    def closeEvent(self, event):
        event.accept()