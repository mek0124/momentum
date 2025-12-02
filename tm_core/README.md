<label id="top"></label>

<div align="center">
  <img src="../original.png" alt="app icon" width="60" height="60" />
  <h1>Task Manager - Core Library</h1>
  <h5>SQLAlchemy | UUID | Validation | ORM Models | Task Management</h5>
</div>

Table of Contents:

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [CoreController](#corecontroller)
  - [Task Model](#task-model)
  - [Validators](#validators)
- [Project Structure](#project-structure)
- [Changelog](#changelog)
- [Contributing](#contributing)
- [License](#license)
- [Issues](#issues)

---

<h3 id="introduction">Introduction</h3>

Welcome to the **Task Manager Core Library** – the backbone of the Task Manager application. This library provides the essential business logic, data validation, ORM models, and controller logic for managing tasks within the application.

It is built with **SQLAlchemy** for database interactions, includes comprehensive validation layers, and follows a clean separation of concerns between core logic and storage layers.

[Top](#top)

---

<h3 id="features">Features</h3>

- **Task Model**: SQLAlchemy ORM-based `Task` model with UUID primary keys and timestamp tracking.
- **CoreController**: Handles all task operations (CRUD) with validation and error handling.
- **Validation Layer**: Robust input validation for titles, details, IDs, and more.
- **Storage-Agnostic**: Can work with both online and offline storage controllers.
- **Semantic Versioning**: Follows clear versioning and changelog practices.

[Top](#top)

---

<h3 id="installation">Installation</h3>

The library is available via `pyproject.toml` and can be installed as a package:

```bash
pip install .
```

**Dependencies:**
- Python >= 3.12
- SQLAlchemy >= 2.0.0

[Top](#top)

---

<h3 id="usage">Usage</h3>

### CoreController
The `CoreController` is the main entry point for task operations:

```python
from tm_core.controller import CoreController

controller = CoreController()

# Get all tasks
success, tasks = controller.get_all_tasks(use_online_storage=False)

# Create a new task
new_task = {
    "title": "Finish documentation",
    "details": "Update README and changelog",
    "priority": 2,
    "is_completed": 0
}
success, message = controller.create_task(new_task, use_online_storage=False)

# Update a task
success, message = controller.update_task(task_id, updated_fields, use_online_storage=True)

# Delete a task
success, message = controller.delete_task(task_id, use_online_storage=False)
```

### Task Model
The `Task` model is defined using SQLAlchemy ORM:

```python
from tm_core.models import Task

task = Task(
    id="uuid-string",
    title="Sample Task",
    details="Task details here",
    priority=1,
    is_completed=0
)

# Convert to dictionary
task_dict = task.to_dict()
```

### Validators
Input validation is handled by the `Validators` class:

```python
from tm_core.validators import Validators

validators = Validators()

# Validate ID
validators.validate_id("some-uuid")

# Validate title
validators.validate_title("A valid title")

# Validate details
validators.validate_details("Detailed description here")
```

[Top](#top)

---

<h3 id="project-structure">Project Structure</h3>

```
tm_core/
├── __init__.py
├── controller.py           # CoreController with business logic
├── models/
│   ├── __init__.py
│   └── task.py            # SQLAlchemy Task model
├── validators/
│   ├── __init__.py
│   └── validators.py      # Validation logic
├── pyproject.toml         # Package configuration
├── README.md              # This file
└── changelog.md           # Version history
```

[Top](#top)

---

<h3 id="changelog">Changelog</h3>

All changes are documented in [CHANGELOG.md](./changelog.md).  
The project follows [Semantic Versioning](https://semver.org/).

**Latest stable version:** `1.0.0` – Released 2025-12-03  
See the changelog for full details on fixes, changes, and additions.

[Top](#top)

---

<h3 id="contributing">Contributing</h3>

At this time, I am not open to contributions as this project is still in its early stages.  
Please check back later for updates on contribution guidelines.

[Top](#top)

---

<h3 id="license">License</h3>

This suite, including its components, UI, core logic, storage algorithms, etc., is the sole proprietary property of **mek0124**.

[Top](#top)

---

<h3 id="issues">Issues</h3>

For any issues, please create a new ticket on the [Issues Page](https://github.com/mek0124/task-manager/issues).

[Top](#top)
