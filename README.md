# 📝 Task Manager

A sleek, terminal-based task management application built with **Python** and **Textual**, designed for efficiency and simplicity. Manage your to-dos with a keyboard-friendly interface that doesn't leave the terminal.

![Task Manager Application Screenshot](https://via.placeholder.com/800x450/0c2b4e/f4f4f4?text=Task+Manager+Screenshot)

## ✨ Features

- **📋 Task Management**: Create, edit, delete, and organize tasks with ease
- **🎨 Modern TUI**: Clean, responsive terminal interface with intuitive navigation
- **📅 Due Dates**: Set deadlines for tasks with flexible date formatting
- **⚡ Quick Actions**: Keyboard shortcuts for power users (Ctrl+N for new task, Ctrl+S to save)
- **💾 Persistent Storage**: SQLite database for reliable data storage
- **🎨 Custom Theme**: Beautiful blue theme inspired by professional design palettes

## Future-Features
- **🔄 Auto-Updates**: Built-in update checker for GitHub releases
- **🔔 Smart Notifications**: Stay informed with timely alerts and reminders
- **🎨 Updated Modern UI**: Clean, styled, responsive terminal interface with intuitive nagivation

## 🚀 Quick Start

> NOTE: This application currently only runs on Linux. If you would like to build and maintain working versions for the other two operating systems, please join the discord server [here](https://discord.gg/gQQwawtWmF) and message me about it please and thank you :)

### For End Users (No Python Required)

1. **Download the latest release** from the [Releases page](https://github.com/mek0124/task-manager/releases)
2. **Run the executable**:
   - **Windows**: Double-click `TaskManager.exe`
   - **macOS/Linux**: Open terminal and run `./TaskManager`
3. **Follow the initial setup** to grant read/write permissions

### For Developers

```bash
# Clone the repository
git clone https://github.com/yourusername/task-manager.git
cd task-manager

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 📦 Installation

### Prerequisites
- Python 3.12 or higher
- pip package manager

### Step-by-Step Setup

```bash
# 1. Clone and enter the project
git clone https://github.com/mek0124/task-manager.git
cd task-manager

# 2. Create a virtual environment (recommended)
python -m venv venv

# 3. Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python3 main.py
```

## 🎮 Usage Guide

### Basic Navigation

| Action | Keyboard Shortcut | Description |
|--------|-------------------|-------------|
| New Task | `Ctrl + N` | Create a new task |
| Save Entry | `Ctrl + S` | Save current task (in edit mode) |
| Go Back | `Ctrl + B` | Return to main screen |
| Quit | `Ctrl + Q` | Exit the application |

### Managing Tasks

1. **Creating a Task**:
   - Press `Ctrl + N` from the main screen
   - Fill in title, details, due date, and priority (1-3)
   - Press `Ctrl + S` to save

2. **Editing a Task**:
   - Click the "Edit" button on any task card
   - Modify the task details
   - Press `Ctrl + S` to save changes

3. **Deleting a Task**:
   - Click the "Delete" button on any task card
   - Confirm the deletion in the notification

### Due Date Format
Enter dates in the format: `MM/DD/YYYY HH:MM`
- Example: `12/25/2024 14:30` for Christmas at 2:30 PM

## 🛠️ Building from Source

To create a standalone executable for distribution:

```bash
# Install PyInstaller
pip install pyinstaller

# Build the executable
pyinstaller --onefile --windowed --add-data "app/data:app/data" main.py
```

The executable will be available in the `dist/` folder.

## 🏗️ Project Structure

```
task-manager/
├── app/
│ ├── init.py
│ ├── app.py # Main application class
│ ├── config/
│ │ └── config.py # Configuration manager
│ ├── data/
│ │ ├── agreement_text.txt # User agreement
│ │ └── config.json # App settings (name, version, repo)
│ ├── database/
│ │ ├── init.py
│ │ └── db.py # Database connection & SQLAlchemy setup
│ ├── logic/
│ │ ├── init.py
│ │ ├── logic_gate.py # Business logic (CRUD operations)
│ │ ├── models/
│ │ │ ├── init.py
│ │ │ └── task.py # SQLAlchemy Task model
│ │ └── services/
│ │ ├── init.py
│ │ └── db.py # Database service layer
│ └── pages/
│ ├── init.py
│ └── entry.py # Task entry/edit screen
├── main.py # Application entry point (permissions check & launch)
├── main.spec # PyInstaller configuration (auto-generated)
├── pyproject.toml # Python project metadata
├── requirements.txt # Python dependencies
└── README.md # This documentation file
```

## 🔧 Dependencies
The application relies on the following Python packages

#### In pyproject.toml
```python
dependencies = [
  "pydantic>=2.12.5",        # Data validation and settings management
  "pyinstaller>=6.17.0",     # Application packaging into executables
  "pytest>=9.0.1",           # Testing framework
  "pytest-asyncio>=1.3.0",   # Async support for tests
  "setuptools>=80.9.0",      # Package building and distribution
  "sqlalchemy>=2.0.44",      # Database ORM for SQLite
  "textual>=6.7.1",          # Modern Text User Interface framework
  "wheel>=0.45.1"            # Built-package format for Python
]
```

|Development|vs.|Runtime Dependencies|
|-|-|-|
|Package|Purpose|Required For|
|textual|Terminal UI framework|✅ Runtime
|sqlalchemy|Database operations|✅ Runtime
|pydantic|Data validation|✅ Runtime
|pyinstaller|Building executables|⚠️ Build-time only
|pytest, pytest-asyncio|Testing|🧪 Development only
|setuptools, wheel|Packaging|📦 Distribution only|

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow existing code style and structure
- Add tests for new functionality
- Update documentation as needed
- Ensure backward compatibility

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Permission denied" when running the executable
**Solution**: Make the file executable: `chmod +x TaskManager`

**Issue**: Database not found or corrupted
**Solution**: Delete `app/data/main.db` and restart the app

### Getting Help
If you encounter issues not covered here:
1. Check the [Issues page](https://github.com/yourusername/task-manager/issues) for existing reports
2. Create a new issue with details about the problem
3. Include your OS, Python version, and error messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Python Software Foundation** for the versatile programming language that made this application possible

- **Textual team** for the amazing TUI framework that powers the interface

- **SQLAlchemy contributors** for the robust database ORM

- **ColorHunt** for the beautiful color palette (#0c2b4e, #1a3d64, #1d546c, #f4f4f4)

- **Pydantic team** for the elegant data validation library

- **All open-source contributors** whose work forms the foundation of this project

- **The users and testers** who provide valuable feedback to improve the application

## 📈 Roadmap

Planned features for future releases:
- [ ] Task categories and tags
- [ ] Search and filter functionality
- [ ] Export tasks to CSV/JSON
- [ ] Dark/Light theme toggle
- [ ] Recurring tasks
- [ ] Task prioritization algorithms
- [ ] (optional) convert TUI to PySide6 for DesktopGUI

---

**⭐ If you find this project useful, please consider giving it a star on GitHub!**

---

*Built with ❤️ using Python and Textual. Last updated: Dec 5th, 2025*