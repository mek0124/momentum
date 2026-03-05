from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich import box

from core.logic import Logic
from core.utils.color_theme import COLOR_THEME

import sys

console = Console()


class MomentumConsole:
    def __init__(self, logic):
        self.logic = logic
        self.all_tasks = self.logic.get_all_tasks()

    def clear_console(self):
        console.clear()

    def print_header(self):
        header_text = Text("Momentum", style=f"bold {COLOR_THEME['primary']}")
        subtitle_text = Text("v1.0.0", style=COLOR_THEME['text_muted'])
        console.print(Panel(header_text + subtitle_text, box=box.DOUBLE_EDGE))

    def show_menu(self):
        menu_text = Text()

        menu_options = {
            "1 ": "View All Tasks\n",
            "2 ": "Add Task\n",
            "3 ": "Edit Task\n",
            "4 ": "Delete Task\n",
            "5 ": "Exit"
        }

        for index, value in menu_options.items():
            menu_text.append(index, style=COLOR_THEME['primary'])
            menu_text.append(value, style=COLOR_THEME['text_primary'])

        console.print(Panel(menu_text, title="Menu", border_style=COLOR_THEME['primary']))

    def view_all_tasks(self):
        self.clear_console()
        self.print_header()

        tasks = self.logic.get_all_tasks()

        if not tasks:
            console.print(Panel("No Tasks Found", style=COLOR_THEME['warning']))
            Prompt.ask("Press enter to continue")
            return
        
        table = Table(box=box.ROUNDED, border_style=COLOR_THEME['warning'])
        table.add_column("ID", style=COLOR_THEME['primary'])
        table.add_column("Title", style=COLOR_THEME['text_primary'])
        table.add_column("Content", style=COLOR_THEME['text_secondary'])

        for task in tasks:
            table.add_row(
                str(task.id),
                task.title,
                task.content
            )

        console.print(table)
        Prompt.ask("Press enter to continue")

    def add_task(self):
        self.clear_console()
        self.print_header()

        console.print(Panel("New Task", style=COLOR_THEME['success']))

        title = Prompt.ask("Title")
        console.print("Content (enter '.' on a new line to finish):")

        content_lines = []

        while True:
            line = input()

            if line == '.':
                break

            content_lines.append(line)

        content = '\n'.join(content_lines)

        did_save, response = self.logic.save_task(title, content)
        console.print(response, style=COLOR_THEME['success'] if did_save else COLOR_THEME['error'])
        
        Prompt.ask("Press enter to continue")

    def edit_task(self):
        self.clear_console()
        self.print_header()

        tasks = self.logic.get_all_tasks()

        if not tasks:
            console.print(Panel("No Tasks Found", style=COLOR_THEME['error']))
            Prompt.ask("Press enter to continue")
            return
        
        table = Table(box=box.SIMPLE, border_style=COLOR_THEME['primary'])
        table.add_column("ID", style=COLOR_THEME['primary'])
        table.add_column("Title", style=COLOR_THEME['text_primary'])
        table.add_column('Content', style=COLOR_THEME['text_muted'])

        for task in tasks:
            table.add_row(str(task.id), task.title, task.content)

        console.print(table)

        try:
            task_id = int(Prompt.ask("Entry task id to edit"))
            task = next((t for t in tasks if t.id == task_id), None)

            if not task:
                console.print(Panel(f"No entry found by ID: {task_id}", style=COLOR_THEME['error']))
                Prompt.ask("Press enter to continue")
                return
            
            console.print(f"Editing: {task_id}")

            new_title = Prompt.ask("New title (press Enter to keep current)", default=task.title)
            console.print("New content (press Enter to keep current, '.' on new line to finish):")

            content_lines = []

            while True:
                line = input()

                if line == '.':
                    break

                content_lines.append(line)

            new_content = '\n'.join(content_lines) if content_lines else None

            success, message = self.logic.update_task(task_id, new_title, new_content)
            color = COLOR_THEME['success'] if success else COLOR_THEME['error']

            console.print(Panel(message, style=color, border_style=color))
        
        except ValueError:
            console.print(Panel("Invalid ID", style=COLOR_THEME['error']))

        Prompt.ask("Press enter to continue")

    def delete_task(self):
        self.clear_console()
        self.print_header()

        tasks = self.logic.get_all_tasks()

        if not tasks:
            console.print(Panel("No Tasks Found", style=COLOR_THEME['warning']))
            Prompt.ask("Press enter to continue")
            return
        
        table = Table(box=box.SIMPLE, border_style=COLOR_THEME['primary'])
        table.add_column("ID", style=COLOR_THEME['primary'])
        table.add_column("Title", style=COLOR_THEME['text_primary'])
        table.add_column("Content", style=COLOR_THEME['text_muted'])

        for task in tasks:
            table.add_row(str(task.id), task.title, task.content)

        console.print(table)

        try:
            task_id = int(Prompt.ask("Enter task id to delete"))

            if Confirm.ask(f"Are you sure you want to delete task {task_id}?"):
                success, message = self.logic.delete_task(task_id)
                color = COLOR_THEME['success'] if success else COLOR_THEME['error']

                console.print(Panel(message, border_style=color, style=color))

            else:
                console.print(Panel("Deletion Cancelled", style=COLOR_THEME['error'], border_style=COLOR_THEME['error']))
            
        except ValueError:
            console.print(Panel("Invalid ID", style=COLOR_THEME['error'], border_style=COLOR_THEME['error']))

        Prompt.ask("Press enter to continue")

    def run(self):
        while True:
            self.clear_console()
            self.print_header()
            self.show_menu()

            choice = Prompt.ask("Select Option", choices=["1", "2", "3", "4", "5"])

            if choice == "1":
                self.view_all_tasks()

            elif choice == "2":
                self.add_task()
            
            elif choice == "3":
                self.edit_task()

            elif choice == "4":
                self.delete_task()

            elif choice == "5":
                console.print(Panel("Goodbye!", style=COLOR_THEME['primary']))
                sys.exit(0)

            self.all_tasks = self.logic.get_all_tasks()


def main():
    app_dir = Path.home() / ".momentum"
    logic = Logic(app_dir)
    app = MomentumConsole(logic)
    app.run()


if __name__ == '__main__':
    main()