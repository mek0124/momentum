from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)

from PySide6.QtCore import Qt


class Dashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Dashboard")

        self.parent_window = parent
        self.color_theme = parent.color_theme
        self.local_version = parent.local_version
        self.latest_version = parent.latest_version

        self.setStyleSheet(
            f"""
                QWidget {{
                    border: none;
                }}

                QLabel#title {{
                    font-weight: bold;
                    font-style: italic;
                    font-size: 18px;
                    color: {self.color_theme['primary']};
                }}

                QLabel#version-label {{
                    font-style: italic;
                    font-size: 14px;
                    color: {self.color_theme['text_primary']};
                }}

                QPushButton#cancel-button {{
                    border: 2px solid {self.color_theme['error']};
                    border-radius: {self.color_theme['border_radius_medium']};
                    color: {self.color_theme['error']};
                    outline: none;
                }}

                QPushButton#cancel-button:hover {{
                    background-color: {self.color_theme['error']};
                    color: black;
                    outline: none;
                    font-weight: bold;
                }}

                QPushButton#update-button {{
                    border: 2px solid {self.color_theme['success']};
                    border-radius: {self.color_theme['border_radius_medium']};
                    color: {self.color_theme['success']};
                    outline: none;
                }}

                QPushButton#update-button:hover {{
                    background-color: {self.color_theme['success']};
                    color: black;
                    outline: none;
                    font-weight: bold;
                }}
            """
        )

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(50)
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

        update_box = QWidget()
        
        update_box_layout = QVBoxLayout(update_box)
        update_box_layout.setContentsMargins(0, 0, 0, 0)
        update_box_layout.setSpacing(50)
        update_box_layout.setAlignment(Qt.AlignCenter)

        update_label = QLabel("Would You Like To Update?")
        update_label.setObjectName("title")
        update_label.setAlignment(Qt.AlignCenter)

        button_row = QWidget()

        button_row_layout = QHBoxLayout(button_row)
        button_row_layout.setContentsMargins(0, 0, 0, 0)
        button_row_layout.setSpacing(50)
        button_row_layout.setAlignment(Qt.AlignCenter)

        cancel_btn = QPushButton("No")
        cancel_btn.setFixedSize(150, 40)
        cancel_btn.setObjectName("cancel-button")
        cancel_btn.clicked.connect(self.exit_app)
        
        update_btn = QPushButton("Yes")
        update_btn.setFixedSize(150, 40)
        update_btn.setObjectName("update-button")
        update_btn.clicked.connect(self.update_app)

        button_row_layout.addWidget(cancel_btn)
        button_row_layout.addWidget(update_btn)

        update_box_layout.addWidget(update_label)
        update_box_layout.addWidget(button_row)

        layout.addWidget(title_label)
        layout.addWidget(current_label)
        layout.addWidget(latest_label)
        layout.addWidget(update_box, 1)

        layout.addStretch()

    def exit_app(self):
        from PySide6.QtWidgets import QApplication
        QApplication.quit()

    def update_app(self):
        self.parent_window.show_splash_screen()