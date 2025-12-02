<label id="top"></label>

<div align="center">
  <img src="./original.png" alt="app icon" width="60" height="60" />
  <h1>Task Manager</h1>
  <h3>A suite of applications sharing a like-minded core and storage library</h3>
  <h5>CLI | TUI | Desktop | Mobile | Web</h5>
</div>

---

## Table of Contents

- [Introduction](#introduction)
- [Project Architecture](#project-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Development Setup](#development-setup)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Issues](#issues)

---

<div align="center">
  <h2 id="introduction">Introduction</h2>
  
  Welcome to <b><u><i>Task Manager</i></u></b>, a light-weight task tracking application developed by mek0124 as a portfolio project. This repository contains the full codebase for the project, spanning multiple platforms. It includes a Python desktop application for a Graphical User Interface (GUI), a Python Textual Text-Based User Interface (TUI), alongside a powerful Command-Line Interface (CLI). The ecosystem is completed by a cross-platform mobile app (Expo) and a modern web application (Next.js).

  The project follows a modular architecture with separate components for core logic, storage, configuration, and various user interfaces.
</div>

[Top](#top)

---

<h2 id="project-architecture">Project Architecture</h2>

The project is organized into several core modules:

### Core Modules
- **tm_core/**: Core business logic, models, and validators
- **tm_storage/**: Storage abstraction layer with offline (SQLite) and online (planned) support
- **tm_config/**: Configuration management with JSON-based settings

### User Interfaces
- **tm_cli/**: Command-line interface using Click
- **tui/**: Text-based user interface using Textual (Python)
- **desktop/**: GUI application using PySide6 (Python)
- **mobile/**: Cross-platform mobile app using Expo (TypeScript)
- **web/**: Web application using Next.js (TypeScript)

### Supporting Files
- **tests/**: Comprehensive test suite using pytest
- **scripts/**: Utility scripts for setup and management
- **pytest.ini**: pytest configuration

### Key Dependencies
- **SQLAlchemy**: Database ORM
- **Click**: CLI framework
- **Textual**: TUI framework
- **PySide6**: Desktop GUI framework
- **pytest**: Testing framework

[Top](#top)

---

<h2 id="installation">Installation</h2>

### Prerequisites
- Python 3.12 or higher
- [UV package manager](https://github.com/astral-sh/uv) (recommended) or pip
- Git

### Quick Start
1. Clone the repository:
   ```bash
   git clone https://github.com/mek0124/task-manager.git
   cd task-manager
   ```

2. Install dependencies using the provided script:
   ```bash
   bash scripts/requirements.sh
   ```

   This script will:
   - Check for required project structure
   - Upgrade existing dependencies if found
   - Install all project modules and dependencies

### Manual Installation
If you prefer not to use UV, you can install dependencies manually:
```bash
pip install setuptools wheel bcrypt click pyside6 pytest python-dotenv sqlalchemy textual
```

[Top](#top)

---

<h2 id="usage">Usage</h2>

### CLI Usage
The CLI provides a comprehensive interface for task management:

```bash
# Add a new task
tm_cli add_task --title "Complete project" --details "Finish the README documentation" --priority 1

# List all tasks
tm_cli list_tasks
#  or a task by ID
tm_cli list_tasks --id <insert_id_here>

# Edit a task
tm_cli edit_task --id <task_id> --title "Updated title" --priority 2

# Delete a task
tm_cli delete_task --id <task_id>
```

### Available Commands
- `add_task`: Create a new task with title, details, and priority
- `list_tasks`: List all tasks or view a specific task by ID
- `edit_task`: Update an existing task with partial updates
- `delete_task`: Remove a task by ID

### Configuration
The application uses a JSON configuration file (`tm_config/config.json`) for settings:
- Database type and path
- Application name and version
- Storage preferences

[Top](#top)

---

<h2 id="development-setup">Development Setup</h2>

### Project Structure
```
task-manager/
├── tm_core/          # Core logic and models
├── tm_storage/       # Storage layer
├── tm_config/        # Configuration
├── tm_cli/           # CLI interface
├── tests/            # Test suite
├── scripts/          # Utility scripts
└── tui/, desktop/    # Other UIs (in development)
```

### Setting Up Development Environment
1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e .[dev]  # If dev extras are defined
   ```

### Module Installation
Each module can be installed individually:
```bash
# Install core module
pip install -e tm_core

# Install storage module
pip install -e tm_storage

# Install CLI module
pip install -e tm_cli
```

[Top](#top)

---

<h2 id="testing">Testing</h2>

The project includes a comprehensive test suite using pytest.

### Running Tests
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test module
pytest tests/test_core.py

# Run tests with short traceback
pytest --tb=short
```

### Test Structure
- **tests/test_config.py**: Configuration tests
- **tests/test_core.py**: Core model and logic tests
- **tests/test_storage.py**: Storage layer tests
- **tests/conftest.py**: Test fixtures and setup

### Test Configuration
Tests are configured in `pytest.ini`:
- Test paths: `tests/`
- Python files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

[Top](#top)

---

<h2 id="contributing">Contributing</h2>

This is a portfolio project for me. All assistance is welcome in sharing knowledge and expertise. I do ask that any fellow developer who would like to contribute to this project to please fork the repository to your repo and push to those forks.

### Contribution Guidelines
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add or update tests as necessary
5. Ensure all tests pass
6. Submit a pull request

For easier communication, please join the project's Discord community (link to be added).

[Top](#top)

---

<h2 id="license">License</h2>

This suite, its components, various UIs, core logic, storage algorithms, etc. are all sole proprietary property of mek0124.

All rights reserved. No part of this project may be reproduced, distributed, or transmitted in any form or by any means without the prior written permission of the author.

[Top](#top)

---

<h2 id="issues">Issues</h2>

For any and all issues, please create a new issue on the [issues page](https://github.com/mek0124/task-manager/issues).

When reporting issues, please include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)

[Top](#top)

---

<div align="center">
  <sub>Built with ❤️ by mek0124</sub>
</div>
```

This updated README.md provides:
1. **Comprehensive project overview** that matches the actual codebase structure
2. **Clear installation instructions** using the provided `scripts/requirements.sh`
3. **Detailed usage examples** for the CLI interface
4. **Development setup guide** for contributors
5. **Testing information** that references the existing test suite
6. **Proper project structure** based on the actual modules (tm_core, tm_storage, tm_config, tm_cli)
7. **Consistent formatting** with the original style and table of contents
8. **Updated contribution guidelines** based on the project's current state