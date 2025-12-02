<label id="top"></label>

<div align="center">
  <img src="../original.png" alt="app icon" width="60" height="60" />
  <h1>Task Manager - CLI Tool</h1>
  <h5>Version 1.0.0 | Built with Click</h5>
</div>

Table of Contents:

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Contributing](#contributing)
- [Licensing](#licensing)
- [Issues](#issues)

---

<h3 id="introduction">Introduction</h3>

Welcome to the CLI tool version of the Task Manager application. This CLI was developed using Click and serves as a console-based wrapper around the core and storage components of the application.

[Top](#top)

---

<h3 id="installation">Installation</h3>

#### From Source:
1. Clone the repository:
   ```bash
   git clone https://github.com/mek0124/task-manager.git
   cd task-manager/cli
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install the package in editable mode:
   ```bash
   pip install -e .
   ```

[Top](#top)

---

<h3 id="usage">Usage</h3>

Once installed, the `tm_cli` command will be available in your terminal:

```bash
# Basic usage pattern
tm_cli [COMMAND] [OPTIONS]
```

[Top](#top)

---

<h3 id="commands">Commands</h3>

#### `add_task` - Create a new task
**Options:**
- `--title` (required): Title of the task
- `--details`: Additional details about the task
- `--priority`: Priority level (1=high, 2=medium, 3=low, default=3)

**Example:**
```bash
tm_cli add_task --title "Complete project" --details "Finish the CLI documentation" --priority 1
```

#### `edit_task` - Update an existing task
**Options:**
- `--id` (required): ID of the task to edit
- `--title`: Updated title
- `--details`: Updated details
- `--priority`: Updated priority level (1-3)
- `--is_completed`: Mark task as completed (flag)

**Example:**
```bash
tm_cli edit_task --id "task_123" --title "Updated title" --priority 2 --is_completed
```

#### `delete_task` - Remove a task
**Options:**
- `--id` (required): ID of the task to delete

**Example:**
```bash
tm_cli delete_task --id "task_123"
```

#### `list_tasks` - List tasks
**Options:**
- `--id`: (optional) ID of a specific task to display

**Examples:**
```bash
# List all tasks
tm_cli list_tasks

# Show specific task
tm_cli list_tasks --id "task_123"
```

[Top](#top)

---

<h3 id="contributing">Contributing</h3>

At this time, I am not open to contributions as this project is still in the early stages. Please check back later for updates!

[Top](#top)

---

<h3 id="licensing">Licensing</h3>

This suite, its components, various UIs, core logic, storage algorithms, etc. are all sole proprietary property of mek0124.

[Top](#top)

---

<h3 id="issues">Issues</h3>

For any issues, please create a new ticket on the [Issues page](https://github.com/mek0124/task-manager/issues).

[Top](#top)