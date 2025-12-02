import click
import sys

from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from tm_core.validators import Validators
from tm_core.controller import CoreController


@click.command("edit_task")
@click.option("--id", required=True, help="the id of the task to edit.")
@click.option("--title", help="the updated title of the task item.")
@click.option("--details", help="the updated details of the task item.")
@click.option("--priority", type=click.IntRange(1, 3), help="the updated priority level of the task item: 1 = high, 2 = medium, 3 = low.")
@click.option("--is_completed", is_flag=True, help="mark the task as completed.")
def edit_task(id: str, title: str = None, details: str = None, priority: int = None, is_completed: bool = False) -> None:

    if not title and not details and priority is None and not is_completed:
        raise click.ClickException("Bruh. Can't edit nothing... try again -_-")
    

    validator = Validators()
    
    updated_task = {}

    if title:
        valid_title, title_error = validator.validate_title(title)

        if not valid_title:
            raise click.ClickException(f"Invalid title: {title_error}")

        updated_task["title"] = title

    if details:
        valid_details, details_error = validator.validate_details(details)

        if not valid_details:
            raise click.ClickException(f"Invalid details: {details_error}")

        updated_task["details"] = details

    if priority:
        updated_task["priority"] = priority

    if is_completed:
        updated_task["is_completed"] = 1

    elif is_completed is not None:
        updated_task["is_completed"] = 0


    if not updated_task:
        raise click.ClickException("Bruh. Can't edit nothing... try again -_-")


    core_controller = CoreController()

    from tm_config.config import Config
    config = Config()
    use_online_storage = config.get_online_storage_preference()
    
    did_update, response = core_controller.update_task(id, updated_task, use_online_storage)

    if not did_update:
        raise click.ClickException(f"Failed to update task: {response}")
    
    click.echo(f"Task updated: {response}")