from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QLineEdit, QPushButton,
    QRadioButton, QScrollArea, QStatusBar
)

from PySide6.QtCore import Qt, QTimer

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

        self.radio_low.setChecked(True)

    def setup_ui(self):
        if self.layout() is None:
            layout = QVBoxLayout(self)

        else:
            layout = self.layout()

            while layout.count():
                item = layout.takeAt(0)

                if item.widget():
                    item.widget().deleteLater()

        inner_container = QWidget()
        inner_container_layout = QHBoxLayout(inner_container)

        self.add_task_panel(inner_container_layout)
        self.add_form_panel(inner_container_layout)

        inner_container_layout.addStretch()

        status_bar_container = QWidget()
        status_bar_container.setStyleSheet("border: none;")

        status_bar_container_layout = QHBoxLayout(status_bar_container)
        status_bar_container_layout.setContentsMargins(0, 0, 0, 0)
        status_bar_container_layout.setSpacing(0)
        status_bar_container_layout.setAlignment(Qt.AlignCenter)

        self.status_bar = QStatusBar()

        status_bar_container_layout.addWidget(self.status_bar)

        layout.addWidget(inner_container, 3)
        layout.addWidget(status_bar_container)
        layout.addStretch()

    def add_task_panel(self, layout):
        panel = QWidget()
        panel.setStyleSheet(
            f"""
                QWidget {{
                    border-right: 2px solid {COLOR_THEME['primary']};
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
            task_scroll_area = QScrollArea()

            task_scroll_area_layout = QHBoxLayout(task_scroll_area)
            task_scroll_area_layout.setContentsMargins(10, 0, 0, 0)
            task_scroll_area_layout.setSpacing(10)
            task_scroll_area_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

            for task in self.all_tasks:
                task_card = QWidget()
                task_card.setProperty("task_id", str(task.id))
                task_card.setStyleSheet(
                    f"""
                        QWidget {{
                            background-color: {COLOR_THEME['surface']};
                            border: 1px solid {COLOR_THEME['primary']};
                            border-radius: {COLOR_THEME['border_radius_medium']};
                        }}
                    """
                )
                task_card.setFixedSize(180, 180)

                task_card_layout = QVBoxLayout(task_card)
                task_card_layout.setContentsMargins(5, 5, 5, 5)
                task_card_layout.setSpacing(0)
                task_card_layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)

                task_title = QLabel(task.title)
                task_title.setStyleSheet(
                    f"""
                        QLabel {{
                            font-weight: bold;
                            font-style: italic;
                            font-size: 12px;
                            color: {COLOR_THEME['primary']};
                            border: none;
                        }}
                    """
                )
                task_title.setAlignment(Qt.AlignCenter)

                details_label = QLabel(task.details)
                details_label.setStyleSheet(
                    f"""
                        QLabel {{
                            font-size: 10px;
                            color: {COLOR_THEME['text_primary']};
                            border: none;
                        }}
                    """
                )
                details_label.setAlignment(Qt.AlignCenter)

                task_card_row = QWidget()
                task_card_row.setStyleSheet("border: none;")

                task_card_row_layout = QHBoxLayout(task_card_row)
                task_card_row_layout.setContentsMargins(0, 0, 0, 0)
                task_card_row_layout.setSpacing(10)
                task_card_row_layout.setAlignment(Qt.AlignCenter)

                priority_label = QLabel(f"Priority\n{task.priority}")
                priority_label.setStyleSheet(
                    f"""
                        QLabel {{
                            font-size: 10px;
                            color: {COLOR_THEME['text_primary']};
                        }}
                    """
                )
                priority_label.setAlignment(Qt.AlignCenter)

                created_at_label = QLabel(
                    f"Created On\n{task.created_at.__format__('%m/%d/%Y\n%H:%M')}")
                created_at_label.setStyleSheet(
                    f"""
                        QLabel {{
                            font-size: 10px;
                            color: {COLOR_THEME['text_primary']};
                        }}
                    """
                )
                created_at_label.setAlignment(Qt.AlignCenter)

                task_card_row_layout.addWidget(priority_label)
                task_card_row_layout.addWidget(created_at_label)

                if task.created_at != task.updated_at:
                    updated_at_label = QLabel(
                        f"Last Updated\n{task.updated_at.__format__('%m/%d/%Y\n%H:%M')}")
                    updated_at_label.setStyleSheet(
                        f"""
                            QLabel {{
                                font-size: 10px;
                                color: {COLOR_THEME['text_primary']};
                            }}
                        """
                    )
                    updated_at_label.setAlignment(Qt.AlignCenter)

                    task_card_row_layout.addWidget(updated_at_label)

                btn_container = QWidget()
                btn_container.setStyleSheet("border: none;")

                btn_container_layout = QHBoxLayout(btn_container)
                btn_container_layout.setContentsMargins(0, 0, 0, 0)
                btn_container_layout.setSpacing(10)
                btn_container_layout.setAlignment(Qt.AlignCenter)

                edit_btn = QPushButton("Edit")
                edit_btn.setProperty("task_id", str(task.id))
                edit_btn.setStyleSheet(
                    f"""
                        QPushButton {{
                            border: 2px solid {COLOR_THEME['primary']};
                            border-radius: {COLOR_THEME['border_radius_small']};
                            background-color: transparent;
                            width: 40px;
                            height: 20px;
                            font-size: 12px;
                        }}

                        QPushButton::hover {{
                            background-color: {COLOR_THEME['surface_light']};
                        }}
                    """
                )
                edit_btn.clicked.connect(self.populate_form)

                del_btn = QPushButton("Delete")
                del_btn.setStyleSheet(
                    f"""
                        QPushButton {{
                            border: 2px solid {COLOR_THEME['primary']};
                            border-radius: {COLOR_THEME['border_radius_small']};
                            background-color: transparent;
                            width: 40px;
                            height: 20px;
                            font-size: 12px;
                        }}

                        QPushButton::hover {{
                            background-color: {COLOR_THEME['surface_light']};
                        }}
                    """
                )
                del_btn.clicked.connect(self.delete_task)
                del_btn.setProperty("task_id", str(task.id))

                btn_container_layout.addWidget(edit_btn)
                btn_container_layout.addWidget(del_btn)

                task_card_layout.addWidget(task_title)
                task_card_layout.addWidget(details_label, 2)
                task_card_layout.addWidget(task_card_row)
                task_card_layout.addWidget(btn_container)

                task_scroll_area_layout.addWidget(task_card)

            panel_layout.addWidget(task_scroll_area)

            layout.addWidget(panel, 3)
            return layout

    def add_form_panel(self, layout):
        panel = QWidget()

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout.setSpacing(15)
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

        self.details_input = QTextEdit()
        self.details_input.setStyleSheet(
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
                    width: 40px;
                    height: 20px;
                    font-size: 12px;
                }}

                QPushButton::hover {{
                    background-color: {COLOR_THEME['surface_light']};
                }}
            """
        )
        clear_btn.clicked.connect(self.reset_form)

        submit_btn = QPushButton("Update" if self.editing_id else "Create")
        self.submit_btn = submit_btn
        submit_btn.setStyleSheet(
            f"""
                QPushButton {{
                    border: 2px solid {COLOR_THEME['primary']};
                    border-radius: {COLOR_THEME['border_radius_small']};
                    background-color: transparent;
                    width: 40px;
                    height: 20px;
                    font-size: 12px;
                }}

                QPushButton::hover {{
                    background-color: {COLOR_THEME['surface_light']};
                }}
            """
        )
        submit_btn.clicked.connect(self.handle_task_submit)

        priority_row_layout.addWidget(self.radio_low)
        priority_row_layout.addWidget(self.radio_medium)
        priority_row_layout.addWidget(self.radio_high)

        button_row_layout.addWidget(clear_btn)
        button_row_layout.addWidget(submit_btn)

        panel_layout.addWidget(title_label)
        panel_layout.addWidget(self.title_input)
        panel_layout.addWidget(content_label)
        panel_layout.addWidget(self.details_input, 2)
        panel_layout.addWidget(priority_label)
        panel_layout.addWidget(priority_row)
        panel_layout.addWidget(button_row)

        layout.addWidget(panel, 1)
        return layout

    def reset_form(self):
        self.title_input.clear()
        self.details_input.clear()
        self.radio_low.setChecked(True)
        self.radio_medium.setChecked(False)
        self.radio_high.setChecked(False)
        self.editing_id = ""
        self.setup_ui()

    def handle_error_success(self, is_error: bool, msg: str, duration: int = 3000):
        if is_error:
            self.status_bar.setStyleSheet(
                f"background-color: {COLOR_THEME['error']}; color: black;")
        else:
            self.status_bar.setStyleSheet(
                f"background-color: {COLOR_THEME['success']}; color: black;")

        self.status_bar.showMessage(msg, duration)

        self.timer = QTimer()
        self.timer.setInterval(duration)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.reset_status_bar)
        self.timer.start()

    def reset_status_bar(self):
        self.status_bar.setStyleSheet("")
        return self.timer.stop()

    def handle_task_submit(self):
        if self.editing_id:
            self.update_task()
            self.editing_id = ""
            self.load_tasks()
        else:
            self.save_task()

    def save_task(self):
        new_title = self.title_input.text().strip()
        new_details = self.details_input.toPlainText().strip()
        
        if not new_title:
            self.handle_error_success(True, "Title Error: title cannot be empty", 3000)
            return
        
        if not new_details:
            self.handle_error_success(True, "Details Error: details cannot be empty", 3000)
            return
        
        title_exists = self.db.query(Task).filter(Task.title == new_title).first()

        if title_exists:
            self.handle_error_success(True, "Title Error: title already exists", 3000)
            return
        
        if self.radio_low.isChecked():
            priority = 3
        elif self.radio_medium.isChecked():
            priority = 2
        elif self.radio_high.isChecked():
            priority = 1
        else:
            priority = 3

        new_task = Task(
            title = new_title,
            details = new_details,
            priority = priority
        )

        try:
            self.db.add(new_task)
            self.db.commit()
            self.load_tasks()
            self.handle_error_success(False, "Task created successfully!", 3000)

        except Exception as e:
            self.handle_error_success(True, f"Unknown Error Saving Task: {e}", 3000)
            self.db.rollback()
            return

    def update_task(self):
        new_title = self.title_input.text().strip()
        new_details = self.details_input.toPlainText().strip()

        if not new_title:
            self.handle_error_success(
                True, "Title Error: title cannot be empty", 3000)
            return

        if not new_details:
            self.handle_error_success(
                True, "Details Error: details cannot be empty", 3000)
            return

        title_exists = self.db.query(Task).filter(
            Task.title == new_title, Task.id != int(self.editing_id)).first()

        if title_exists:
            self.handle_error_success(
                True, "Title Error: title already exists", 3000)
            return

        if self.radio_low.isChecked():
            priority = 3
        elif self.radio_medium.isChecked():
            priority = 2
        elif self.radio_high.isChecked():
            priority = 1
        else:
            priority = 3

        try:
            task = self.db.query(Task).filter(
                Task.id == int(self.editing_id)).first()
            task.title = new_title
            task.details = new_details
            task.priority = priority
            self.db.commit()
            self.handle_error_success(
                False, "Task updated successfully!", 3000)

        except Exception as e:
            self.handle_error_success(
                True, f"Unknown Error Saving Task: {e}", 3000)
            self.db.rollback()
            return

    def populate_form(self):
        sender = self.sender()
        task_id = sender.property("task_id")

        for task in self.all_tasks:
            if str(task.id) == task_id:
                self.editing_id = task_id
                self.title_input.setText(task.title)
                self.details_input.setText(task.details)

                if task.priority == 1:
                    self.radio_high.setChecked(True)
                elif task.priority == 2:
                    self.radio_medium.setChecked(True)
                else:
                    self.radio_low.setChecked(True)

                self.submit_btn.setText("Update")
                break

    def delete_task(self):
        sender = self.sender()
        task_id = sender.property("task_id")
        
        try:
            self.db.query(Task).filter(Task.id == int(task_id)).delete()
            self.db.commit()
            self.handle_error_success(False, "Task Deleted Successfully", 3000)
            self.load_tasks()
        
        except Exception as e:
            self.handle_error_success(True, str(e), 3000)
            self.db.rollback()
            self.load_tasks()

    def load_tasks(self):
        self.title_input.clear()
        self.details_input.clear()
        self.title_input.setFocus()
        self.radio_low.setChecked(True)
        self.all_tasks = self.db.query(Task).all()
        self.editing_id = ""
        self.setup_ui()