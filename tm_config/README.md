# Task Manager Configuration Library (`tm_config`)

A lightweight Python library for managing application configuration in JSON format, designed specifically for the Task Manager application.

## 📦 Features

- **JSON-based configuration** with UTF-8 BOM support
- **Automatic file creation** – config file is created if missing
- **Full CRUD operations** for version management
- **Type hints** throughout for better developer experience
- **Database configuration** support (SQLite by default)
- **Error handling** for JSON parsing and file operations
- **Semantic versioning** aligned with project standards

## 📁 Project Structure

```
tm_config/
├── __init__.py          # Package exports
├── config.py            # Main Config class
├── config.json          # Default configuration
├── pyproject.toml       # Build configuration
├── changelog.md         # Version history
└── README.md            # This file
```

## 🔧 Installation

```bash
pip install tm_config
```

Or install from source:

```bash
git clone https://github.com/mek0124/task-manager/
cd task-manager
pip install .
```

## 🚀 Quick Start

```python
from tm_config import Config

# Initialize configuration
config = Config()

# Get database settings
db_type = config.get_database_type()      # "sqlite"
db_path = config.get_database_path()      # "storage/data/tasks.db"

# Get all configuration data
success, data = config.get_all_version_items("")
if success:
    print(data)

# Update a version item
update_data = {
    "app_name": "Task Manager Pro",
    "version": "1.1.0"
}
config.update_version_item(1, update_data)
```

## 📝 Default Configuration

The library uses `config.json` with this default structure:

```json
{
  "database": {
    "type": "sqlite",
    "path": "storage/data/tasks.db"
  },
  "app": {
    "name": "Task Manager",
    "version": "0.6.0"
  }
}
```

## 🧩 API Reference

### `Config` Class

#### Core Methods
- `_load_config()` – Loads configuration from JSON file
- `get_config_file_path()` – Returns path to config file (creates if missing)
- `get_all_version_items(keyword)` – Retrieves config items, optionally filtered

#### Version Management
- `create_new_version_item(new_version)` – Adds a new version entry
- `update_version_item(version_id, updated_version)` – Updates existing version
- `delete_version_item(version_id)` – Removes a version entry

#### Database Configuration
- `get_database_config()` – Returns full database configuration
- `get_database_path()` – Returns database file path
- `get_database_type()` – Returns database type (e.g., "sqlite")

## 📄 Configuration File Format

Version items in `config.json` should follow this structure:

```json
[
  {
    "id": 1,
    "app_name": "Task Manager",
    "version": "1.0.0",
    "updated_at": "12/03/2025 - 14:30:00"
  }
]
```

## 🔒 Error Handling

All public methods return tuples `(bool, Union[result, error_message])`:
- `True` + data on success
- `False` + error message on failure

Example:
```python
success, result = config.create_new_version_item(new_item)
if not success:
    print(f"Error: {result}")
```

## 📈 Version History

See [CHANGELOG.md](changelog.md) for detailed version history and changes.

## 🛠 Requirements

- Python >= 3.12
- No external dependencies

## 📄 License

Proprietary – © 2025 mek0124

## 🤝 Contributing

Issues and pull requests are welcome on GitHub:
- Repository: https://github.com/mek0124/task-manager/
- Issues: https://github.com/mek0124/task-manager/issues/

## 📧 Contact

**Author:** mek0124  
**Email:** mek0124@proton.me  
**Project:** Task Manager Configuration Library