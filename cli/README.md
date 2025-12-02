<label id="top"></label>

<div align="center">
  <img src="../original.png" alt="app icon" width="60" height="60" />
  <h1>Task Manager - CLI Tool</h1>
  <h5>Click</h5>
</div>

Table of Contents:

- [Introduction](#introduction)
- [How To Use](#how-to-use)
- [Contributing](#contributing)
- [Licensing](#licensing)
- [Issues](#issues)

---

<h3 id="introduction">Introduction</h3>

Welcome to the cli tool version of the task manager application. This CLI was developed using Click and serves as a console based wrapper around the core and storage components of the application.

[Top](#top)

---

<h3 id="how-to-use">How To Use</h3>

To use this cli tool, you can clone the repository and pip install it or run it from source

1. Open Command Prompt
2. Run `git clone https://github.com/mek0124/task-manager.git`
3. Change directories `cd task-manager/cli`
4. Install the module
  - create a virtual environment in your project if you haven't already and activate it
  - run `pip install -e .` and run it with `tm_cli add_task --title Some Awesome title --details Some very awesome details about this task --priority 2`
    - or
  - run `python3 tm_cli add_task --title Some Awesome title --details Some very awesome details about this task --priority 2`


|command|parameters|example|description|
|-|-|-|-|
|add_task|--title|add_task --title Some Awesome Title|the title of the task item|
||--details|add_task --details Some very awesome details about this task|the details about the task item|
||--priority|add_task --priority 1|the priority level of the task item. can be 1 = high, 2 = medium, or 3 = low|
|edit_task|--task_id|edit_task --task_id ##@#!f-v9i09sid2=0e=2j-q|the id of the task item to edit|
||--title|edit_task --title Some Awesome Title|the updated title of the task item|
||--details|edit_task --details Some very awesome details about this task|the updated details about the task item|
||--priority|edit_task --priority 1|the updated priority level of the task item. can be 1 = high, 2 = medium, or 3 = low|
|delete_task|--task_id|delete_task --task_id ##@#!f-v9i09sid2=0e=2j-q|the id of the task item to delete|
|list_all|||lists all currently existing tasks|
|list_all|--task_id|list_all --task_id ##@#!f-v9i09sid2=0e=2j-q|displays the information about the target task id|

```
# to add a new task
tm_cli add_task --title Some Awesome Title --details Some very awesome details about this task item --priority 2

# to update an existing task
tm_cli edit_task --task_id ##@#!f-v9i09sid2=0e=2j-q --title Some New Updated Awesome Title

# to delete an existing task
tm_cli delete_task --task_id ##@#!f-v9i09sid2=0e=2j-q

# to list all tasks
tm_cli list_all

# to list a task by id
tm_cli list_all --task_id ##@#!f-v9i09sid2=0e=2j-q
```

[Top](#top)

---

<h3 id="contributing">Contributing</h3>

At this time, I am not open to contributions as this project is still under the very, very beginning stages. Please do keep checking back!

[Top](#top)

---

<h3 id="licensing">Licensing</h3>

This suite, its components, various ui's, core logic, storage algorithms, etc are all sole proprietary property of mek0124.

[Top](#top)

---

<h3 id="issues">Issues</h3>

For any and all issues, please create a new issues on the [issues page](https://github.com/mek0124/task-manager/issues)

[Top](#top)

---