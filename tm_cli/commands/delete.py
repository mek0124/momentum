import click
import sys

from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from tm_core.controller import CoreController
from tm_core.validators import Validators


@click.command("delete_task")
@click.option("--id", required=True, help="the id of the task to delete.")
def delete_task(id: str) -> None:

    validator = Validators()

    valid_id, id_error = validator.validate_id(id)

    if not valid_id:
        raise click.ClickException(f"Invalid ID: {id_error}")


    core_controller = CoreController()

    from tm_config.config import Config
    config = Config()
    use_online_storage = config.get_online_storage_preference()
    
    did_delete, response = core_controller.delete_task(id, use_online_storage)

    if not did_delete:
        raise click.ClickException(f"Failed to delete task: {response}")
    
    click.echo(f"Task deleted: {response}")