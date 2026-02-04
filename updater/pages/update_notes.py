from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)

from PySide6.QtCore import Qt


class UpdateNotes(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Update Notes")

        self.color_theme = parent.color_theme

        self.setStyleSheet(
            f"""
                QWidget {{
                    border: none;
                }}
            """
        )

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignCenter)

        layout.addStretch()