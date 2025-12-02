<label id="top"></label>

<div align="center">
  <img src="../original.png" alt="app icon" width="60" height="60" />
  <h1>Task Manager - Storage Library</h1>
  <h5>SQLite3 | Cloud Storage</h5>
</div>

Table of Contents:

- [Introduction](#introduction)
- [Installation](#installation)
- [How To Use](#how-to-use)
- [API Reference](#api-reference)
- [Architecture](#architecture)
- [Changelog](#changelog)
- [Contributing](#contributing)
- [Licensing](#licensing)
- [Issues](#issues)

---

<h3 id="introduction">Introduction</h3>

Welcome to the storage library for the task management application. This library provides a unified interface for both offline and online storage with automatic fallback mechanisms. The system is designed to handle SQLite3 for local storage and cloud-based storage with seamless transition between modes.

**Key Features:**
- **Offline Storage**: SQLite3 database for local task management
- **Online Storage**: Cloud-based storage interface (stub implementation ready for extension)
- **Automatic Fallback**: If online storage is unavailable after 5 attempts, automatically switches to offline storage
- **Type Safety**: Full type hints throughout the codebase
- **Task Model Integration**: Uses `tm_core.models.Task` for data consistency
- **Error Handling**: Comprehensive error handling with detailed messages

[Top](#top)

---

<h3 id="installation">Installation</h3>

### Prerequisites
- Python 3.12 or higher
- Git

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/mek0124/task-manager.git
   cd task-manager
   ```

2. Install the storage module in development mode:
   ```bash
   # Create and activate virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install the storage library
   pip install -e storage
   ```

### Dependencies
The library automatically installs:
- `sqlalchemy >= 2.0.0`

[Top](#top)

---

<h3 id="how-to-use">How To Use</h3>

### Basic Usage Example:

```python
from tm_storage import StorageController
from tm_core.models import Task
from uuid import uuid4
from datetime import datetime

# Create a new Task object
new_task = Task(
    id=str(uuid4()),
    title="Complete Project Documentation",
    details="Write comprehensive documentation for the storage module",
    priority=2,  # 1 = high, 2 = medium, 3 = low
    created_at=datetime.now(),
    updated_at=datetime.now(),
    is_completed=False
)

# Initialize the storage controller
storage = StorageController()

# Create a task (automatically uses offline storage as default)
success, message = storage.create_task(new_task)

if success:
    print(f"Success: {message}")
else:
    print(f"Error: {message}")

# Retrieve all tasks
success, tasks = storage.get_all_tasks()
if success:
    for task in tasks:
        print(f"Task: {task['title']}")

# Get a specific task by ID
task_id = "your-task-id-here"
success, task = storage.get_task_by_id(task_id)

# Update a task
task.title = "Updated Title"
success, message = storage.update_task(task)

# Delete a task
success, message = storage.delete_task(task_id)
```

### Storage Mode Selection
The library automatically handles storage mode selection:
- By default, uses offline storage (SQLite)
- Online storage can be implemented by extending `OnlineStorageController`
- Automatic fallback occurs when online storage is unavailable

[Top](#top)

---

<h3 id="api-reference">API Reference</h3>

### StorageController Class

#### Methods:

**`get_all_tasks() -> Tuple[bool, Union[List[dict], str]]`**
Retrieves all tasks from storage.
- Returns: `(success, tasks_or_error_message)`

**`get_task_by_id(task_id: str) -> Tuple[bool, Union[dict, str]]`**
Retrieves a specific task by its ID.
- Parameters: `task_id` - The unique identifier of the task
- Returns: `(success, task_or_error_message)`

**`create_task(task: Task) -> Tuple[bool, str]`**
Creates a new task in storage.
- Parameters: `task` - A Task model instance
- Returns: `(success, message)`

**`update_task(task: Task) -> Tuple[bool, str]`**
Updates an existing task.
- Parameters: `task` - A Task model instance with updated values
- Returns: `(success, message)`

**`delete_task(task_id: str) -> Tuple[bool, str]`**
Deletes a task by its ID.
- Parameters: `task_id` - The unique identifier of the task
- Returns: `(success, message)`

### Data Model
All operations use the `Task` model from `tm_core.models` with the following structure:
- `id`: str - Unique identifier
- `title`: str - Task title
- `details`: str - Task description
- `priority`: int - Priority level (1=high, 2=medium, 3=low)
- `created_at`: datetime - Creation timestamp
- `updated_at`: datetime - Last update timestamp
- `is_completed`: bool - Completion status

[Top](#top)

---

<h3 id="architecture">Architecture</h3>

### File Structure:
```
tm_storage/
├── __init__.py          # Exports StorageController and db
├── controller.py        # Main controller with automatic fallback logic
├── changelog.md         # Project version history
├── controllers/
│   ├── __init__.py     # Exports both controller types
│   ├── offline.py      # SQLite3 offline storage implementation
│   └── online.py       # Cloud storage implementation (stub)
├── database.py          # Database initialization and session management
├── data/               # SQLite database storage location
└── pyproject.toml      # Package configuration
```

### Database Configuration
The SQLite database is automatically created in `tm_storage/data/tasks.db` with the following features:
- Automatic table creation using SQLAlchemy
- Session management for thread-safe operations
- Support for custom database paths via constructor

### Extension Points
1. **Online Storage**: Implement cloud storage by extending `OnlineStorageController` in `controllers/online.py`
2. **Custom Database**: Pass custom database path to `Database()` constructor
3. **Additional Models**: Extend database schema by importing and registering new models

[Top](#top)

---

<h3 id="changelog">Changelog</h3>

For detailed version history and changes, see [CHANGELOG.md](changelog.md)

**Recent Highlights:**
- **v1.0.0**: Fixed method name consistency and task model handling
- **v0.8.0**: Updated to accept Task models instead of dictionaries
- **v0.6.0**: Added SQLAlchemy database integration
- **v0.4.0**: Reconstructed for "local storage first" architecture

[Top](#top)

---

<h3 id="contributing">Contributing</h3>

At this time, I am not open to contributions as this application is still in the very beginning stages. Please check back!

[Top](#top)

---

<h3 id="licensing">Licensing</h3>

This suite, its components, various UI's, core logic, storage algorithms, etc are all sole proprietary property of mek0124.

[Top](#top)

---

<h3 id="issues">Issues</h3>

For any and all issues, please create a new issue on the [issues page](https://github.com/mek0124/task-manager/issues)

[Top](#top)
