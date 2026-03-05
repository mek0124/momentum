from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QStatusBar
)
from PySide6.QtCore import Qt, QTimer


class Dashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("Dashboard")

        self.logic = parent.logic
        self.color_theme = parent.color_theme

        self.all_tasks = self.logic.get_all_tasks()
        self.editing_id = ""

        self.setup_ui()
        self.load_tasks()

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
        self.status_bar.setStyleSheet("border: none; height: 30px;")

        status_bar_container_layout.addWidget(self.status_bar)

        layout.addWidget(inner_container, 3)
        layout.addWidget(status_bar_container)
        layout.addStretch()

    def add_task_panel(self, layout):
        panel = QWidget()
        panel.setStyleSheet(
            f"""
                QWidget {{
                    border-left: 2px solid {self.color_theme["primary"]};
                    border-right: 2px solid {self.color_theme["primary"]};
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
                        color: {self.color_theme["primary"]};
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
                        color: {self.color_theme["text_primary"]};
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
            task_scroll_area.setWidgetResizable(True)
            task_scroll_area.setStyleSheet(
                f"""
                    QScrollArea {{
                        border: none;
                        background-color: transparent;
                    }}
                    QScrollArea > QWidget > QWidget {{
                        background-color: transparent;
                    }}
                """
            )

            scroll_content = QWidget()
            scroll_content.setStyleSheet("border: none; background-color: transparent;")

            scroll_content_layout = QGridLayout(scroll_content)
            scroll_content_layout.setContentsMargins(10, 10, 10, 10)
            scroll_content_layout.setSpacing(15)
            scroll_content_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

            for index, task in enumerate(self.all_tasks):
                row = index // 4
                col = index % 4

                task_card = QWidget()
                task_card.setProperty("task_id", str(task.id))
                task_card.setFixedSize(250, 300)
                task_card.setStyleSheet(
                    f"""
                        QWidget {{
                            background-color: {self.color_theme["surface"]};
                            border: 1px solid {self.color_theme["primary"]};
                            border-radius: {self.color_theme["border_radius_medium"]};
                        }}
                    """
                )

                task_card_layout = QVBoxLayout(task_card)
                task_card_layout.setContentsMargins(10, 10, 10, 10)
                task_card_layout.setSpacing(5)
                task_card_layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)

                task_title = QLabel(task.title)
                task_title.setStyleSheet(
                    f"""
                        QLabel {{
                            font-weight: bold;
                            font-style: italic;
                            font-size: 12px;
                            color: {self.color_theme["primary"]};
                            border: none;
                        }}
                    """
                )
                task_title.setAlignment(Qt.AlignCenter)

                content_label = QLabel(task.content)
                content_label.setStyleSheet(
                    f"""
                        QLabel {{
                            font-size: 10px;
                            color: {self.color_theme["text_primary"]};
                            border: none;
                        }}
                    """
                )
                content_label.setAlignment(Qt.AlignCenter)

                task_card_row = QWidget()
                task_card_row.setStyleSheet("border: none;")

                task_card_row_layout = QHBoxLayout(task_card_row)
                task_card_row_layout.setContentsMargins(0, 0, 0, 0)
                task_card_row_layout.setSpacing(10)
                task_card_row_layout.setAlignment(Qt.AlignCenter)

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
                            border: 2px solid {self.color_theme["primary"]};
                            border-radius: {self.color_theme["border_radius_small"]};
                            background-color: transparent;
                            width: 40px;
                            height: 20px;
                            font-size: 12px;
                        }}

                        QPushButton::hover {{
                            background-color: {self.color_theme["surface_light"]};
                        }}
                    """
                )
                edit_btn.clicked.connect(self.populate_form)

                del_btn = QPushButton("Delete")
                del_btn.setStyleSheet(
                    f"""
                        QPushButton {{
                            border: 2px solid {self.color_theme["primary"]};
                            border-radius: {self.color_theme["border_radius_small"]};
                            background-color: transparent;
                            width: 40px;
                            height: 20px;
                            font-size: 12px;
                        }}

                        QPushButton::hover {{
                            background-color: {self.color_theme["surface_light"]};
                        }}
                    """
                )
                del_btn.clicked.connect(self.delete_task)
                del_btn.setProperty("task_id", str(task.id))

                btn_container_layout.addWidget(edit_btn)
                btn_container_layout.addWidget(del_btn)

                task_card_layout.addWidget(task_title)
                task_card_layout.addWidget(content_label, 2)
                task_card_layout.addWidget(task_card_row)
                task_card_layout.addWidget(btn_container)

                row = index // 4
                col = index % 4
                scroll_content_layout.addWidget(task_card, row, col, 1, 1)

            for col in range(4):
                scroll_content_layout.setColumnStretch(col, 1)

            task_scroll_area.setWidget(scroll_content)

            panel_layout.addWidget(task_scroll_area)

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
                    color: {self.color_theme["primary"]};
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
                    border: 2px solid {self.color_theme["primary"]};
                    border-radius: {self.color_theme["border_radius_small"]};
                    height: 30px;
                    font-size: 12px;
                }}

                QLineEdit::hover {{
                    background-color: {self.color_theme["surface_light"]};
                }}

                QLineEdit::cursor {{
                    color: {self.color_theme["primary"]};
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
                    color: {self.color_theme["primary"]};
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
                    border: 2px solid {self.color_theme["primary"]};
                    border-radius: {self.color_theme["border_radius_small"]};
                    font-size: 12px;
                }}

                QTextEdit::hover {{
                    background-color: {self.color_theme["surface_light"]};
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
                    border: 2px solid {self.color_theme["primary"]};
                    border-radius: {self.color_theme["border_radius_small"]};
                    background-color: transparent;
                    width: 40px;
                    height: 20px;
                    font-size: 12px;
                }}

                QPushButton::hover {{
                    background-color: {self.color_theme["surface_light"]};
                }}
            """
        )
        clear_btn.clicked.connect(self.reset_form)

        submit_btn = QPushButton("Update" if self.editing_id else "Create")
        self.submit_btn = submit_btn
        submit_btn.setStyleSheet(
            f"""
                QPushButton {{
                    border: 2px solid {self.color_theme["primary"]};
                    border-radius: {self.color_theme["border_radius_small"]};
                    background-color: transparent;
                    width: 40px;
                    height: 20px;
                    font-size: 12px;
                }}

                QPushButton::hover {{
                    background-color: {self.color_theme["surface_light"]};
                }}
            """
        )
        submit_btn.clicked.connect(self.handle_task_submit)

        button_row_layout.addWidget(clear_btn)
        button_row_layout.addWidget(submit_btn)

        panel_layout.addWidget(title_label)
        panel_layout.addWidget(self.title_input)
        panel_layout.addWidget(content_label)
        panel_layout.addWidget(self.content_input, 2)
        panel_layout.addWidget(button_row)

        layout.addWidget(panel, 1)
        return layout

    def reset_form(self):
        self.title_input.clear()
        self.content_input.clear()
        self.editing_id = ""
        self.setup_ui()

    def handle_error_success(self, is_error: bool, msg: str):
        if is_error:
            self.status_bar.setStyleSheet(
                f"background-color: {self.color_theme['error']}; color: black;"
            )
        else:
            self.status_bar.setStyleSheet(
                f"background-color: {self.color_theme['success']}; color: black;"
            )

        self.status_bar.showMessage(msg)

        self.timer = QTimer()
        self.timer.setInterval(3000)
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
        new_content = self.content_input.toPlainText().strip()

        if not new_title:
            self.handle_error_success(True, "Title Error: title cannot be empty")
            return

        if not new_content:
            self.handle_error_success(
                True, "Details Error: details cannot be empty", 3000
            )
            return

        did_save, response = self.logic.save_task(new_title, new_content)
        self.load_tasks()
        return self.handle_error_success(did_save, response)

    def update_task(self):
        new_title = self.title_input.text().strip()
        new_content = self.content_input.toPlainText().strip()

        if not new_title:
            return self.handle_error_success(True, "Title Error: title cannot be empty")

        if not new_content:
            return self.handle_error_success(
                True, "Details Error: details cannot be empty"
            )

        did_update, response = self.logic.update_task(self.editing_id, new_title, new_content)

        return self.handle_error_success(did_update, response)

    def populate_form(self):
        sender = self.sender()
        task_id = sender.property("task_id")

        for task in self.all_tasks:
            if str(task.id) == task_id:
                self.editing_id = task_id
                self.title_input.setText(task.title)
                self.content_input.setText(task.content)
                self.submit_btn.setText("Update")
                break

    def delete_task(self):
        sender = self.sender()
        task_id = sender.property("task_id")

        did_delete, response = self.logic.delete_task(task_id)
        self.load_tasks()
        return self.handle_error_success(did_delete, response)

    def load_tasks(self):
        self.title_input.clear()
        self.content_input.clear()
        self.title_input.setFocus()
        self.all_tasks = self.logic.get_all_tasks()
        self.editing_id = ""
        self.setup_ui()
