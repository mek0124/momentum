from commands.add import add_task
from commands.edit import edit_task
from commands.delete import delete_task
from commands.list import list_tasks

import click


@click.group()
def tm_cli():
    pass


tm_cli.add_command(add_task)
tm_cli.add_command(edit_task)
tm_cli.add_command(delete_task)
tm_cli.add_command(list_tasks)


if __name__ == '__main__':
    tm_cli()