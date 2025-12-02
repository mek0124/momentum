import click
import sys

from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from tm_core.controller import CoreController
from tm_core.validators import Validators


@click.command("list_tasks")
@click.option("--id", help="the id of a specific task to list.")
def list_tasks(id: str = None) -> None:

    validator = Validators()


    if id:
        valid_id, id_error = validator.validate_id(id)

        if not valid_id:
            raise click.ClickException(f"Invalid ID: {id_error}")


    core_controller = CoreController()

    from tm_config.config import Config
    config = Config()
    use_online_storage = config.get_online_storage_preference()
    

    if id:
        did_find, response = core_controller.get_task_by_id(id, use_online_storage)

        if not did_find:
            raise click.ClickException(f"Failed to find task: {response}")

        click.echo("Task found:")
        click.echo(f"ID: {response.get('id')}")
        click.echo(f"Title: {response.get('title')}")
        click.echo(f"Details: {response.get('details')}")
        click.echo(f"Priority: {response.get('priority')}")
        click.echo(f"Created: {response.get('created_at')}")
        click.echo(f"Updated: {response.get('updated_at')}")
        click.echo(f"Completed: {'Yes' if response.get('is_completed') else 'No'}")

    else:
        did_find, response = core_controller.get_all_tasks(use_online_storage)

        if not did_find:
            raise click.ClickException(f"Failed to list tasks: {response}")

        if not response:
            click.echo("No tasks found.")
            return

        click.echo(f"Found {len(response)} task(s):")
        click.echo("")

        for task in response:
            click.echo(f"ID: {task.get('id')}")
            click.echo(f"Title: {task.get('title')}")
            click.echo(f"Priority: {task.get('priority')}")
            click.echo(f"Completed: {'Yes' if task.get('is_completed') else 'No'}")
            click.echo("-" * 40)