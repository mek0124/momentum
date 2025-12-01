<label id="top"></label>

<div align="center">
  <img src="../original.png" alt="app icon" width="60" height="60" />
  <h1>Task Manager - Storage Library</h1>
  <h3>Active Version: 0.4.0</h3>
  <h5>SQLAlchemy | MongoDB</h5>
</div>

Table of Contents:

- [Introduction](#introduction)
- [How To Use](#how-to-use)
- [Contributing](#contributing)
- [Licensing](#licensing)
- [Issues](#issues)

---

<h3 id="introduction">Introduction</h3>

Welcome to the storage library for the task management application. This library is comprised of working with JSON files for user configuration, a relational database for offline storage, and an API for online storage.

- Breakdown
  - JSON
    - handles minor app configuration settings, user preferred settings, user custom settings, and more
  - SQLAlchemy Relational Database
    - handles securely storing the user's task items
  - MongoDB Cloud-Based Storage API
    - handles securely storing the user's tasks in an online database for cloud-like storage

[Top](#top)

---

<h3 id="how-to-use">How To Use</h3>

To use this library in your regular project, you can clone the repository and pip install it

1. Open Command Prompt
2. Run `git clone https://github.com/mek0124/task-manager.git`
3. Change directories `cd task-manager`
4. Install the module
  - create a virtual environment in your project if you haven't already and activate it
  - run `pip install -e storage`

from here, you would just import and use as normal

```python
from storage import OfflineStorageController

from uuid import uuid4
from datetime import datetime

new_task = {
  "id": uuid4(),
  "title": "Some Awesome Title",
  "details": "Some very awesome details about this task",
  "priority": 3, # 1 = high, 2 = medium, 3 (default) = low
  "created_at": datetime.now(),
  "updated_at": datetime.now(),
  "is_completed": False
}

offline_storage = OfflineStorageController()
offline_storage.check_for_db_file()

did_save, response = offline_storage.create_task(new_task)

if not did_save:
    raise Exception(f"Error Saving Task Item: {response}")

print("Task Item Saved Successfully")
```

> NOTE: Both controllers basically offer the same functionality. One just interacts with a json file and the other handles api calls to/from mongodb for cloud storage.

[Top](#top)

---

<h3 id="contributing">Contributing</h3>

At this time, I am not open to contributions as this application is still in the very, very beginning stages. Please check back!

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