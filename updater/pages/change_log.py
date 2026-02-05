from PySide6.QtWidgets import (
    QWidget
)


class ChangeLog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Changelog")