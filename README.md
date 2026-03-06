<div align="center">
  <img src="./core/assets/icon.png" width="120" height="120" />
  <h1>Momentum</h1>
  <h4>
    A local‑first task manager for the terminal, desktop, and automation.
  </h4>
  <p>
    CLI • TUI • GUI --- powered by a shared core.
  </p>

  ![Python](https://img.shields.io/badge/Python-3.12+-blue)
  ![License](https://img.shields.io/badge/License-MIT-green) ![Local
First](https://img.shields.io/badge/Design-local--first-blue)

</div>

---

# Overview

**Momentum** is a minimalist task management application built with a
**modular mono‑repo architecture**.

It provides three interfaces that all share the same core logic:

• **CLI** -- for scripting and automation\
• **TUI** -- for terminal workflows\
• **GUI** -- for desktop users

All interfaces operate on the same **local SQLite database**, ensuring
your data always stays on your machine.

No accounts.\
No telemetry.\
No cloud dependency.

Just you and your tasks.

---

# Philosophy

Momentum follows a few simple principles:

• **Local‑first** --- your data belongs to you\
• **Minimalism** --- fewer features, done well\
• **Hackable** --- readable code and clear architecture\
• **No lock‑in** --- simple SQLite storage

---

# Features

✔ Create tasks\
✔ Edit tasks\
✔ Delete tasks\
✔ List tasks\
✔ Local SQLite database\
✔ CLI / TUI / GUI interfaces\
✔ Modular architecture for future expansion

---

# Architecture

Momentum is structured as a **mono‑repo** containing multiple
installable packages.

    momentum/
    │
    ├── cli/        → Command line interface
    ├── tui/        → Terminal UI (Rich based)
    ├── gui/        → Desktop application (PySide6 + Fluent UI)
    │
    ├── core/       → Shared application logic
    │   ├── database
    │   ├── models
    │   ├── utils
    │   └── logic.py
    │
    ├── pyproject.toml
    └── README.md

Each interface imports and uses the **shared core logic layer**.

    CLI/TUI/GUI
         │
        ▼
    Momentum Core
         │
        ▼
    SQLite Database

---

# Installation

Clone the repository:

``` bash
git clone https://github.com/mek0124/momentum.git
cd momentum
```

Create a virtual environment:

``` bash
python -m venv .venv
source .venv/bin/activate
```

Install the project:

``` bash
pip install -e .
```

---

# Running Momentum

After installation you can launch any interface.

### CLI

    momentum

Example:

    momentum hello --name Mek
    momentum add --title "Task" --content "Example task"
    momentum list

---

### Terminal UI

    momentum-tui

Provides a keyboard driven terminal interface powered by **Rich**.

---

### Desktop GUI

    momentum-gui

Launches the **PySide6 Fluent UI desktop application**.

---

# Data Storage

Momentum automatically creates a local data directory after you've agreed to the read/write permissions:

    ~/.momentum/

Inside you will find:

    config.json
    main.db

The database is a **SQLite file** that can be inspected or backed up
manually.

------------------------------------------------------------------------

# Development

Install development dependencies:

``` bash
pip install -e ".[dev]"
```

Recommended tools:

    black
    pytest
    mypy
    isort

Run tests:

``` bash
pytest
```

------------------------------------------------------------------------

# Contributing

Contributions are welcome.

Please read **CONTRIBUTING.md** before submitting a pull request.

------------------------------------------------------------------------

# License

MIT License

Copyright (c) mek0124
