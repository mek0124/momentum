import click


@click.command("hello")
@click.option("--name", help="the name of the user to greet")
def hello_command(name: str = "User"):
    return click.echo(f"Hello, {name}! Welcome to Momentum!")


@click.command("add")
@click.option("--title", help="the title of the task item")
@click.option("--content", help="the content of the task item")
@click.pass_context
def add_command(ctx, title: str, content: str):
    logic = ctx.obj
    _, response = logic.save_task(title, content)
    return click.echo(response)


@click.command("edit")
@click.option("--id", help="the id of the task to update")
@click.option("--title", help="the updated task title")
@click.option("--content", help="the updated task content")
@click.pass_context
def edit_command(ctx, id: int, title: str = None, content: str = None):
    logic = ctx.obj
    _, response = logic.update_task(id, title, content)
    return click.echo(response)


@click.command("delete")
@click.option("--id")
@click.pass_context
def delete_command(ctx, id: int):
    logic = ctx.obj
    _, response = logic.delete_task(id)
    return click.echo(response)


@click.command("list")
@click.pass_context
def list_command(ctx):
    logic = ctx.obj

    all_tasks = logic.get_all_tasks()

    for task in all_tasks:
        id = task.id
        title = task.title
        content = task.content

        print("-"*50)
        print(f"ID: {id}\nTitle: {title}\nContent: {content}")
        print("-"*50)