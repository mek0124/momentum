from pathlib import Path

from .commands import (
    hello_command,
    add_command,
    edit_command,
    delete_command,
    list_command
)


import click
import sys


project_rooot = Path(__file__).parent
sys.path.insert(0, str(project_rooot))

from core.logic import Logic


@click.group
@click.pass_context
def cli(ctx):
    app_dir = Path.home() / ".momentum"
    ctx.obj = Logic(app_dir)


cli.add_command(hello_command)
cli.add_command(add_command)
cli.add_command(edit_command)
cli.add_command(delete_command)
cli.add_command(list_command)


if __name__ == '__main__':
    cli()