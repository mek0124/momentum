from qfluentwidgets import (
    MSFluentWindow, 
    FluentIcon as fi,
    Theme,
    setTheme,
    setThemeColor
)

from .pages.dashboard import Dashboard
from .pages.change_log import ChangeLog


class Updater(MSFluentWindow):
    def __init__(self, root_dir, color_theme, local_version, latest_version):
        super().__init__()

        self.root_dir = root_dir
        self.color_theme = color_theme
        self.local_version = local_version
        self.latest_version = latest_version

        self.dashboard = Dashboard(self)
        self.change_log = ChangeLog(self)

        self.apply_app_styles()
        self.init_navigation()

    def apply_app_styles(self):
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
        self.addSubInterface(
            self.dashboard,
            fi.APPLICATION,
            "Dashboard"
        )

        self.addSubInterface(
            self.change_log,
            fi.CALENDAR,
            "Changelog"
        )