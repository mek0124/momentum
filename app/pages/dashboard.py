from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QLineEdit, QPushButton,
    QRadioButton
)

from PySide6.QtCore import Qt

from ..models.task import Task

from ..utils.color_theme import COLOR_THEME


class Dashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("Dashboard")

        self.db = parent.db

        self.all_tasks = self.db.query(Task).all()
        self.editing_id = ""

        self.setup_ui()
        self.load_tasks()

    def setup_ui(self):
        layout = QHBoxLayout(self)

        self.add_task_panel(layout)
        self.add_form_panel(layout)

        layout.addStretch()

    def add_task_panel(self, layout):
        panel = QWidget()
        panel.setStyleSheet(
            f"""
                QWidget {{
                    border: 2px solid {COLOR_THEME['primary']};
                    border-radius: {COLOR_THEME['border_radius_small']};
                }}
            """
        )

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout.setSpacing(0)
        panel_layout.setAlignment(Qt.AlignCenter)

        if not self.all_tasks or len(self.all_tasks) == 0:
            label = QLabel("No Tasks Currently Exists!")
            label.setStyleSheet(
                f"""
                    QLabel {{
                        border: none; 
                        color: {COLOR_THEME['primary']}; 
                        font-weight: bold; 
                        font-style: italic; 
                        font-size: 16px;
                    }}
                """
            )
            label.setAlignment(Qt.AlignCenter)
            
            label2 = QLabel("Use the form on the right to get started :)")
            label2.setStyleSheet(
                f"""
                    QLabel {{
                        font-style: italic; 
                        font-size: 12px;
                        border: none; 
                        color: {COLOR_THEME['text_primary']};
                    }}
                """
            )
            label2.setWordWrap(True)
            label2.setAlignment(Qt.AlignCenter)
            
            panel_layout.addWidget(label)
            panel_layout.addWidget(label2)

            layout.addWidget(panel, 3)
            return layout
        
        else:
            layout.addWidget(panel, 3)
            return layout

    def add_form_panel(self, layout):
        panel = QWidget()

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout.setSpacing(10)
        panel_layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel("Title")
        title_label.setStyleSheet(
            f"""
                QLabel {{
                    border: none; 
                    font-style: italic; 
                    color: {COLOR_THEME['primary']};
                    font-size: 12px;
                }}
            """
        )
        title_label.setAlignment(Qt.AlignCenter)

        self.title_input = QLineEdit()
        self.title_input.setStyleSheet(
            f"""
                QLineEdit {{
                    background-color: transparent; 
                    border: 2px solid {COLOR_THEME['primary']}; 
                    border-radius: {COLOR_THEME['border_radius_small']};
                    height: 30px;
                    font-size: 12px;
                }}

                QLineEdit::hover {{
                    background-color: {COLOR_THEME['surface_light']};
                }}

                QLineEdit::cursor {{
                    color: {COLOR_THEME['primary']};
                }}
            """
        )
        self.title_input.setAlignment(Qt.AlignCenter)

        content_label = QLabel("Content")
        content_label.setStyleSheet(
            f"""
                QLabel {{
                    border: none; 
                    font-style: italic; 
                    color: {COLOR_THEME['primary']};
                    font-size: 12px;
                }}
            """
        )
        content_label.setAlignment(Qt.AlignCenter)

        self.content_input = QTextEdit()
        self.content_input.setStyleSheet(
            f"""
                QTextEdit {{
                    background-color: transparent; 
                    border: 2px solid {COLOR_THEME['primary']}; 
                    border-radius: {COLOR_THEME['border_radius_small']};
                    font-size: 12px;
                }}

                QTextEdit::hover {{
                    background-color: {COLOR_THEME['surface_light']};
                }}
            """
        )

        priority_label = QLabel("Priority")
        priority_label.setStyleSheet(
            f"""
                QLabel {{
                    border: none; 
                    font-style: italic; 
                    color: {COLOR_THEME['primary']};
                    font-size: 12px;
                }}
            """
        )
        priority_label.setAlignment(Qt.AlignCenter)

        priority_row = QWidget()
        priority_row.setStyleSheet("border: none; height: 30px;")

        priority_row_layout = QHBoxLayout(priority_row)
        priority_row_layout.setContentsMargins(0, 0, 0, 0)
        priority_row_layout.setSpacing(10)

        self.radio_low = QRadioButton("Low")
        self.radio_low.setStyleSheet(
            f"""
                QRadioButton {{
                    color: {COLOR_THEME['primary']};
                    font-size: 12px;
                }}

                QRadioButton::indicator {{
                    width: 20px;
                    height: 20px;
                    border-radius: {COLOR_THEME["border_radius_medium"]};
                }}

                QRadioButton::indicator::unchecked {{
                    background-color: transparent;
                    border: 2px solid {COLOR_THEME['primary']};
                }}

                QRadioButton::indicator::checked {{
                    background-color: {COLOR_THEME['primary']};
                    border: transparent;
                    border-radius: {COLOR_THEME['border_radius_medium']};
                }}
            """
        )

        self.radio_medium = QRadioButton("Medium")
        self.radio_medium.setStyleSheet(
            f"""
                QRadioButton {{
                    color: {COLOR_THEME['primary']};
                    font-size: 12px;
                }}

                QRadioButton::indicator {{
                    width: 20px;
                    height: 20px;
                    border-radius: {COLOR_THEME["border_radius_medium"]};
                }}

                QRadioButton::indicator::unchecked {{
                    background-color: transparent;
                    border: 2px solid {COLOR_THEME['primary']};
                }}

                QRadioButton::indicator::checked {{
                    background-color: {COLOR_THEME['primary']};
                    border: transparent;
                    border-radius: {COLOR_THEME['border_radius_medium']};
                }}
            """
        )

        self.radio_high = QRadioButton("High")
        self.radio_high.setStyleSheet(
            f"""
                QRadioButton {{
                    color: {COLOR_THEME['primary']};
                    font-size: 12px;
                }}

                QRadioButton::indicator {{
                    width: 20px;
                    height: 20px;
                    border-radius: {COLOR_THEME["border_radius_medium"]};
                }}

                QRadioButton::indicator::unchecked {{
                    background-color: transparent;
                    border: 2px solid {COLOR_THEME['primary']};
                }}

                QRadioButton::indicator::checked {{
                    background-color: {COLOR_THEME['primary']};
                    border: transparent;
                    border-radius: {COLOR_THEME['border_radius_medium']};
                }}
            """
        )

        button_row = QWidget()
        button_row.setStyleSheet("border: none; height: 50px;")

        button_row_layout = QHBoxLayout(button_row)
        button_row_layout.setContentsMargins(0, 0, 0, 0)
        button_row_layout.setSpacing(10)

        clear_btn = QPushButton("Clear")
        clear_btn.setStyleSheet(
            f"""
                QPushButton {{
                    border: 2px solid {COLOR_THEME['primary']};
                    border-radius: {COLOR_THEME['border_radius_small']};
                    background-color: transparent;
                    width: 50px;
                    height: 30px;
                }}

                QPushButton::hover {{
                    background-color: {COLOR_THEME['surface_light']};
                }}
            """
        )

        submit_btn = QPushButton("Update" if self.editing_id else "Create")
        submit_btn.setStyleSheet(
            f"""
                QPushButton {{
                    border: 2px solid {COLOR_THEME['primary']};
                    border-radius: {COLOR_THEME['border_radius_small']};
                    background-color: transparent;
                    width: 50px;
                    height: 30px;
                }}

                QPushButton::hover {{
                    background-color: {COLOR_THEME['surface_light']};
                }}
            """
        )

        priority_row_layout.addWidget(self.radio_low)
        priority_row_layout.addWidget(self.radio_medium)
        priority_row_layout.addWidget(self.radio_high)

        button_row_layout.addWidget(clear_btn)
        button_row_layout.addWidget(submit_btn)

        panel_layout.addWidget(title_label)
        panel_layout.addWidget(self.title_input)
        panel_layout.addWidget(content_label)
        panel_layout.addWidget(self.content_input, 2)
        panel_layout.addWidget(priority_label)
        panel_layout.addWidget(priority_row)
        panel_layout.addWidget(button_row)

        layout.addWidget(panel, 1)
        return layout
    
    def load_tasks(self):
        self.title_input.setFocus()
        self.radio_low.setChecked(True)