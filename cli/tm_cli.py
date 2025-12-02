from commands.add import add_task
from commands.edit import edit_task
from commands.delete import delete_task
from commands.list import list_task

from core.controller import CoreController

import click


class MyCLI:
    def __init__(self):
        self.cli = click.Group()
        self._register_commands()
    
    def _register_commands(self):
        """Register all commands with the CLI group"""
        # Register methods decorated with @click.command()
        self.cli.add_command(self.my_command)
        
        # You can also add other commands like this:
        # self.cli.add_command(self.another_command)
    
    def __call__(self, *args, **kwargs):
        """Make the class instance callable"""
        return self.cli(*args, **kwargs)
    
    # Option 1: Define commands as instance methods
    @click.command()
    def my_command(self):
        """Example command"""
        click.echo("Hello from my_command!")