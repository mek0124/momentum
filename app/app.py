from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalGroup, VerticalScroll, HorizontalGroup
from textual.reactive import reactive
from textual.widgets import (
    Static,
    Input,
    Button,
    Header,
    Footer
)

from pathlib import Path

from app.config.config import Config
from app.logic.logic_gate import LogicGate
from app.pages.entry import EntryScreen 
 
class TaskManager(App):
    config = Config()
    logic_gate = LogicGate()

    current_tasks = reactive([])

    BINDINGS = [
        Binding("ctrl+n", "new_entry", "New Entry", False),
    ]

    def action_new_entry(self) -> None:
        def on_save() -> None:
            self.get_current_tasks()

        self.push_screen(EntryScreen(self.config, self.logic_gate, on_save))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_name, task_id = event.button.id.split("_")

        if button_name == "edit":
            def on_save() -> None:
                self.get_current_tasks()
                
            self.push_screen(EntryScreen(self.config, self.logic_gate, on_save, task_id))

        if button_name == "delete":
            delete_response = self.logic_gate.delete_task_by_id(task_id)
            self.notify(
                delete_response,
                title="Task Deletion",
                severity="error" if delete_response.startswith("Exception") else "success"
            )
            self.get_current_tasks()

    def load_tasks(self) -> None:
        task_list = self.query_one("#task-list", VerticalScroll)
        task_list.remove_children()

        if not self.current_tasks:
            return task_list.mount(
                Vertical(
                    Static("No Current Tasks Exist"),
                    Static("To create a new task"),
                    Static("Press ctrl + n"),
                    classes="task-card"
                ),
            )

        for task in self.current_tasks:
            due_by_str = task.due_by.strftime('%m/%d/%Y - %H:%M') if task.due_by else "No due date"
            created_str = task.created_at.strftime('%m/%d/%Y - %H:%M')
            updated_str = task.updated_at.strftime('%m/%d/%Y - %H:%M')
            details_preview = task.details[:25] + '...' if len(task.details) > 25 else task.details

            task_list.mount(
                VerticalGroup(
                    VerticalGroup(
                        VerticalGroup(
                            Static(f"ID: {task.id[:8]}..."),
                            Static(f"Title: {task.title}"),
                        ),
                        VerticalGroup(
                            Static(f"Due By: {due_by_str}"),
                            Static(f"Created On: {created_str}"),
                            Static(f"Last Updated: {updated_str}")
                        ),
                    ),
                    VerticalGroup(
                        Static("Details"),
                        Static(details_preview)
                    ),
                    HorizontalGroup(
                        Button("Edit", id=f"edit_{task.id}"),
                        Button("Delete", id=f"delete_{task.id}")
                    ),
                    classes="task-card"
                ),
            )

    def get_current_tasks(self) -> None:
        self.current_tasks = self.logic_gate.get_current_tasks()
        self.load_tasks()
        self.query_one("#task-list", VerticalScroll).loading = False

    def on_mount(self) -> None:
        app_name = self.config.get_app_name()
        version = self.config.get_version()
        
        self.title = f"{app_name} - v{version}"

        self.query_one("#task-list", VerticalScroll).loading = True
        self.get_current_tasks()

    def compose(self) -> ComposeResult:
        yield Header(
            show_clock = True,
            classes = "custom-header",
            time_format = "%H:%M",
            icon = "TM"
        )

        yield Vertical(
            Vertical(
                Static("Current Tasks", classes="title"),
                VerticalScroll(id="task-list", classes="task-list"),
            ),
        )

        yield Footer(
            compact = True
        )