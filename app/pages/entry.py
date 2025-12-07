from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.markup import escape
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Input, TextArea, Header, Footer

from datetime import datetime


class EntryScreen(Screen):
    title = reactive('')
    details = reactive('')
    due_by = reactive('')
    priority = reactive('')

    BINDINGS = [
        Binding('ctrl+s', 'save_entry', 'Save Entry', True),
        Binding('ctrl+b', 'go_back', 'Go Back', True),
    ]

    def __init__(self, config, logic_gate, save_callback, task_id=None) -> None:
        super().__init__()

        self.config = config
        self.logic_gate = logic_gate
        self.save_callback = save_callback
        self.task_id = task_id

    def on_mount(self) -> None:
        app_name = self.config.get_app_name()
        version = self.config.get_version()
        
        if self.task_id:
            self.title = f"{app_name} - v{version} - Edit Task"
            self.get_task()
        else:
            self.title = f"{app_name} - v{version} - New Entry"

    def get_task(self) -> None:
        if not self.task_id:
            return
        
        try:
            all_tasks = self.logic_gate.db_service.get_all_tasks()
            found_task = None
            
            for task in all_tasks:
                if str(task.id) == self.task_id:
                    found_task = task
                    break

            if not found_task:
                self.app.notify(
                    f"No Task Found By ID: {self.task_id}",
                    title = "Task Found Error",
                    severity = "error"
                )
                self.dismiss()
                return

            # Update reactive attributes FIRST
            self.title = found_task.title
            self.details = found_task.details
            
            if found_task.due_by:
                self.due_by = found_task.due_by.strftime('%m/%d/%Y %H:%M')
                
            self.priority = str(found_task.priority)

            # THEN update the widgets
            title_input = self.query_one("#title", Input)
            title_input.value = self.title
            
            due_by_input = self.query_one("#due_by", Input)
            due_by_input.value = self.due_by
            
            priority_input = self.query_one("#priority", Input)
            priority_input.value = str(self.priority)
            
            details_textarea = self.query_one(TextArea)
            details_textarea.text = self.details
            
            # Make sure TextArea triggers the change event
            self.on_text_area_changed(TextArea.Changed(details_textarea))

        except Exception as e:
            self.app.notify(
                escape(f"Issues Loading Task to Update: {e}"),
                title = "Task Edit Issue",
                severity = "error"
            )
            self.dismiss()

    def on_input_changed(self, event: Input.Changed) -> None:
        input_id = event.input.id
        value = event.input.value

        match input_id:
            case "title":
                self.title = value

            case "due_by":
                cleaned = ''.join(filter(str.isdigit, value))
                
                formatted = ''
                if len(cleaned) > 0:
                    formatted = cleaned[:2]
                if len(cleaned) > 2:
                    formatted += '/' + cleaned[2:4]
                if len(cleaned) > 4:
                    formatted += '/' + cleaned[4:8]
                if len(cleaned) > 8:
                    formatted += ' ' + cleaned[8:10]
                if len(cleaned) > 10:
                    formatted += ':' + cleaned[10:12]
                
                self.due_by = formatted
                event.input.value = formatted
                event.input.cursor_position = len(formatted)

            case "priority":
                try:
                    self.priority = int(value) if value else 3
                except ValueError:
                    self.priority = 3

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        self.details = event.text_area.text

    def action_save_entry(self) -> None:
        new_task = {
            "title": self.title,
            "details": self.details,
            "due_by": self.due_by,
            "priority": self.priority
        }

        try:
            # Use update_task if we're editing an existing task
            if self.task_id:
                response = self.logic_gate.update_task(self.task_id, new_task)
            else:
                # Otherwise create a new task
                response = self.logic_gate.create_task(new_task)
                
            self.notify(
                str(response),
                title="Task Action",
                severity="information" if "Successfully" in response else "error",
                timeout=3
            )

            if "Successfully" in response:
                if self.save_callback:
                    self.save_callback()
                self.dismiss()
            # Don't dismiss on error - let user fix the issue

        except Exception as e:
            self.notify(f"Error: {e}", title="Save Error", severity="error")

    def action_go_back(self) -> None:
        self.dismiss()

    def compose(self) -> ComposeResult:
        yield Header(
            show_clock = True,
            classes = "custom-header",
            icon = "TM",
            time_format = "%H:%M"
        )

        yield Vertical(
            Vertical(
                Input(
                    id="title",
                    value=self.title,
                    placeholder="Enter Title Here...",
                    type="text",
                    classes="user-input",
                ),
                Input(
                    id="due_by",
                    value=self.due_by,
                    placeholder="mm/dd/yyyy hh:mm",
                    type="text",
                    classes="user-input",
                ),
                Input(
                    id="priority",
                    value=str(self.priority),
                    placeholder="Enter priority (1-3)",
                    type="integer",
                    classes="user-input",
                    max_length=1
                ),
                TextArea(
                    text=self.details,
                    show_cursor=True,
                    show_line_numbers=True,
                    placeholder="Enter details here...",
                    classes="user-input",
                ),
            ),
        )

        yield Footer(
            compact = True
        )