<label id="top"></label>

<div align="center">
  <img src="../original.png" alt="app icon" width="60" height="60" />
  <h1>Task Manager - Storage Library</h1>
  <h5>SQLite3 | Cloud Storage</h5>
</div>

Table of Contents:

- [Introduction](#introduction)
- [How To Use](#how-to-use)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [Licensing](#licensing)
- [Issues](#issues)

---

<h3 id="introduction">Introduction</h3>

Welcome to the storage library for the task management application. This library provides a unified interface for both offline and online storage with automatic fallback mechanisms. The system is designed to handle SQLite3 for local storage and cloud-based storage with seamless transition between modes.

- **Offline Storage**: SQLite3 database for local task management
- **Online Storage**: Cloud-based storage (MongoDB API planned)
- **Automatic Fallback**: If online storage is unavailable after 5 attempts, automatically switches to offline storage

[Top](#top)

---

<h3 id="how-to-use">How To Use</h3>

To use this library in your project, you can clone the repository and install it:

1. Open Command Prompt/Terminal
2. Run `git clone https://github.com/mek0124/task-manager.git`
3. Change directories `cd task-manager`
4. Install the module
  - Create a virtual environment in your project if you haven't already and activate it
  - Run `pip install -e storage`

### Basic Usage Example:

```python
from storage import StorageController
from uuid import uuid4
from datetime import datetime

# Create a new task
new_task = {
    "id": str(uuid4()),
    "title": "Some Awesome Title",
    "details": "Some very awesome details about this task",
    "priority": 3,  # 1 = high, 2 = medium, 3 = low
    "created_at": datetime.now(),
    "updated_at": datetime.now(),
    "is_completed": 0  # 0 = False, 1 = True
}

# Initialize the storage controller
storage = StorageController()

# Option 1: Use offline storage (default)
did_save, response = storage.create_task(new_task, use_online_storage=False)

# Option 2: Try online storage first (will fallback to offline if unavailable)
did_save, response = storage.create_task(new_task, use_online_storage=True)

if not did_save:
    raise Exception(f"Error Saving Task Item: {response}")

print("Task Item Saved Successfully")
```

### Available Methods:

```python
# Get all tasks
success, tasks = storage.get_all_tasks(use_online_storage=False)

# Get task by ID
success, task = storage.list_task_by_id(task_id="your-task-id", use_online_storage=False)

# Create a task
success, message = storage.create_task(new_task, use_online_storage=False)

# Update task
success, message = storage.update_task(task_id="your-task-id", updated_task=updated_data, use_online_storage=False)

# Delete task
success, message = storage.delete_task(task_id="your-task-id", use_online_storage=False)
```

[Top](#top)

---

<h3 id="architecture">Architecture</h3>

### File Structure:
```
storage/
├── __init__.py          # Exports StorageController
├── controller.py        # Main controller with automatic fallback logic
├── controllers/
│   ├── __init__.py     # Exports both controller types
│   ├── offline.py      # SQLite3 offline storage implementation
│   └── online.py       # Cloud storage implementation (stub)
└── data/               # SQLite database storage location
```

### Key Features:

1. **Unified Interface**: Both storage controllers implement the same methods
2. **Automatic Fallback**: Online storage attempts connection 5 times before defaulting to offline
3. **Error Handling**: Comprehensive error handling with detailed messages
4. **Database Management**: Automatically creates SQLite database if it doesn't exist

### Storage Controller Methods:
- `get_storage_controller()`: Returns appropriate controller based on online status
- `get_all_tasks()`: Retrieve all tasks
- `list_task_by_id()`: Retrieve specific task by ID
- `create_task()`: Create new task
- `update_task()`: Update existing task
- `delete_task()`: Delete task

> **Note**: The online storage controller is currently a stub and returns "Online Storage Controller Not Setup At This Time". Implement the cloud storage API in `controllers/online.py` when ready.

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

---