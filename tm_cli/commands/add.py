import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from tm_core.controller import CoreController
from tm_core.validators import Validators
import click

@click.command("add_task")
@click.option("--title", required=True, help="the title of the task")
@click.option("--details", default="", help="the details of the task item")
@click.option("--priority", default=3, type=click.IntRange(1, 3), help="the priority level of the task: 1 = high, 2 = medium, 3 = low. default 3")
@click.option("--is_completed", is_flag=True, default=False, help="the completed status of the task. default is false")
def add_task(title: str, details: str, priority: int = 3, is_completed: bool = False) -> None:
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
        "is_completed": is_completed
    }

    # Get user preference from config
    from tm_config.config import Config
    config = Config()
    use_online_storage = config.get_online_storage_preference()
    
    did_save, response = core_controller.create_task(new_task, use_online_storage)

    if not did_save:
        raise click.ClickException(f"Failed to create task: {response}")
    
    click.echo(f"Task created: {response}")


"""
Traceback (most recent call last):
  File "/home/mekasu0124/Documents/dev/portfolio/task-manager/tm_cli/tm_cli.py", line 14, in <module>
    tm_cli()
  File "/home/mekasu0124/anaconda3/envs/python3.12/lib/python3.12/site-packages/click/core.py", line 1485, in __call__
    return self.main(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mekasu0124/anaconda3/envs/python3.12/lib/python3.12/site-packages/click/core.py", line 1406, in main
    rv = self.invoke(ctx)
         ^^^^^^^^^^^^^^^^
  File "/home/mekasu0124/anaconda3/envs/python3.12/lib/python3.12/site-packages/click/core.py", line 1873, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mekasu0124/anaconda3/envs/python3.12/lib/python3.12/site-packages/click/core.py", line 1269, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mekasu0124/anaconda3/envs/python3.12/lib/python3.12/site-packages/click/core.py", line 824, in invoke
    return callback(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mekasu0124/Documents/dev/portfolio/task-manager/tm_cli/commands/add.py", line 41, in add_task
    did_save, response = core_controller.create_task(new_task, use_online_storage)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mekasu0124/Documents/dev/portfolio/task-manager/tm_core/controller.py", line 69, in create_task
    return controller.create_task(new_task, use_online_storage)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: OfflineStorageController.create_task() takes 2 positional arguments but 3 were given
"""