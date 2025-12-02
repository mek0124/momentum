import click
import sys

from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from tm_core.validators import Validators
from tm_core.controller import CoreController


@click.command("add_task")
@click.option("--title", required=True, help="the title of the task")
@click.option("--details", default="", help="the details of the task item")
@click.option("--priority", default=3, type=click.IntRange(1, 3), help="the priority level of the task: 1 = high, 2 = medium, 3 = low. default 3")
def add_task(title: str, details: str, priority: int = 3) -> None:
    validator = Validators()

    valid_title, title_error = validator.validate_title(title)

    if not valid_title:
        raise click.ClickException(f"Invalid title: {title_error}")

    valid_details, details_error = validator.validate_details(details)

    if not valid_details:
        raise click.ClickException(f"Invalid details: {details_error}")

    core_controller = CoreController()

    new_task = {
        "title": title,
        "details": details if details else "",
        "priority": priority,
    }

    from tm_config.config import Config

    config = Config()
    use_online_storage = config.get_online_storage_preference()

    did_save, response = core_controller.create_task(
        new_task, use_online_storage)

    if not did_save:
        raise click.ClickException(f"Failed to create task: {response}")

    click.echo(f"Task created: {response}")
