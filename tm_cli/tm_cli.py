import click
from commands.add import add_task


@click.group()
def tm_cli():
    pass


tm_cli.add_command(add_task)


if __name__ == '__main__':
    tm_cli()