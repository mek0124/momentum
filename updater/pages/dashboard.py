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
        self.new_version = parent.new_version
        self.curr_version = parent.curr_version

        self.setStyleSheet(
            f"""
                QWidget {{
                    border: none;
                }}

                QWidget#container {{
                    border: none;
                }}

                QLabel#title {{
                    font-weight: bold;
                    font-style: italic;
                    font-size: 16px;
                    color: {self.color_theme["primary"]};
                }}

                QLabel#info {{
                    font-size: 12px;
                    color: {self.color_theme['text_primary']};
                }}

                QPushButton#form-btn {{
                    border: 2px solid {self.color_theme['primary']};
                    border-radius: {self.color_theme['border_radius_medium']};
                    background-color: transparent;
                    color: {self.color_theme['text_primary']};
                    font-size: 12px;
                    outline: none;
                }}

                QPushButton#form-btn:hover {{
                    background-color: {self.color_theme['surface_glass_hover']};
                    font-weight: bold;
                    font-style: italic;
                    color: {self.color_theme['primary']};
                    outline: none;
                }}
            """
        )

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignCenter)

        update_label = QLabel(
            "An Update Is Available!"
        )
        update_label.setObjectName("title")
        update_label.setAlignment(Qt.AlignCenter)

        update_info = QLabel(
            f"""
An update from version {self.curr_version} to
{self.new_version} is available. Would you like
to update?
            """
        )
        update_info.setObjectName("info")
        update_info.setAlignment(Qt.AlignCenter)

        btn_row = QWidget()
        btn_row.setObjectName("container")

        btn_row_layout = QHBoxLayout(btn_row)
        btn_row_layout.setContentsMargins(0, 0, 0, 0)
        btn_row_layout.setSpacing(20)
        btn_row_layout.setAlignment(Qt.AlignCenter)

        notes_btn = QPushButton("Update Notes")
        notes_btn.setFixedSize(150, 40)
        notes_btn.setObjectName("form-btn")
        notes_btn.clicked.connect(self.navigate_to_notes_page)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedSize(150, 40)
        cancel_btn.setObjectName("form-btn")
        cancel_btn.clicked.connect(self.exit_app)

        update_btn = QPushButton("Update")
        update_btn.setFixedSize(150, 40)
        update_btn.setObjectName("form-btn")
        update_btn.clicked.connect(self.launch_update)

        btn_row_layout.addWidget(notes_btn)
        btn_row_layout.addWidget(cancel_btn)
        btn_row_layout.addWidget(update_btn)

        layout.addWidget(update_label, 1)
        layout.addWidget(update_info, 1)
        layout.addWidget(btn_row, 1)

        layout.addStretch()

    def navigate_to_notes_page(self):
        return self.parent.switchTo("Update Notes")
    
    def exit_app(self):
        sys.exit(0)

    def launch_update(self):
        pass