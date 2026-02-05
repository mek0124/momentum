from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)

from PySide6.QtCore import Qt

import sys


class Dashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Dashboard")

        self.color_theme = parent.color_theme
        self.latest_version = parent.latest_version
        self.local_version = parent.local_version

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
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel("An Update Is Available!")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)

        current_label = QLabel(f"Current Version: v{self.local_version}")
        current_label.setObjectName("version-label")
        current_label.setAlignment(Qt.AlignCenter)

        latest_label = QLabel(f"Latest Version: v{self.latest_version}")
        latest_label.setObjectName("version-label")
        latest_label.setAlignment(Qt.AlignCenter)

        button_row = QWidget()

        button_row_layout = QHBoxLayout(button_row)
        button_row_layout.setContentsMargins(0, 0, 0, 0)
        button_row_layout.setSpacing(50)
        button_row_layout.setAlignment(Qt.AlignCenter)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("cancel-button")
        cancel_btn.clicked.connect(self.exit_app)
        
        update_btn = QPushButton("Update")
        update_btn.setObjectName("update-button")
        update_btn.clicked.connect(self.update_app)

        layout.addWidget(title_label)
        layout.addWidget(current_label)
        layout.addWidget(latest_label)

        layout.addStretch()

    def exit_app(self):
        sys.exit(0)

    def update_app(self):
        """
        this function should switch off to a QSplashWindow
        with progress text and a progress bar for updating
        the application. Once the update is finished, the
        Update application should exit and the Momentum
        application should launch
        """
        pass