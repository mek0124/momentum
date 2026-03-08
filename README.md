<div align="center">
  <img src="./core/assets/icon.png" width="120" height="120" />
  <h1>Momentum</h1>
  <h4>
    A local‑first task manager for the web.
  </h4>
  <p>
    Built with Flask • SQLite • Modern HTML/CSS/JS
  </p>

  ![Python](https://img.shields.io/badge/Python-3.12+-blue)
  ![License](https://img.shields.io/badge/License-MIT-green)
  ![Local First](https://img.shields.io/badge/Design-local--first-blue)

</div>

---

# Overview

**Momentum** is a minimalist task management application with a clean, modern web interface.

All data is stored **locally** in a SQLite database on your machine.

No accounts.\
No telemetry.\
No cloud dependency.

Just you and your tasks.

---

# Philosophy

Momentum follows a few simple principles:

- **Local-first** — your data belongs to you
- **Minimalism** — fewer features, done well
- **Hackable** — readable code and clear architecture
- **No lock-in** — simple SQLite storage

---

# Features

✔ Create, edit, and delete tasks\
✔ Mark tasks as complete/incomplete\
✔ Filter tasks (All, Active, Completed)\
✔ Local SQLite database\
✔ Modern, responsive dark UI\
✔ Keyboard shortcuts (`/` to focus search, `Esc` to close modal)

---

# Screenshots

The application features a clean, modern dark theme with:
- Smooth animations and transitions
- Responsive design for all screen sizes
- Intuitive task management interface
- Modal-based editing

---

# Installation

Clone the repository:

```bash
git clone https://github.com/mek0124/momentum.git
cd momentum
```

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Install dependencies:

```bash
pip install -e .
```

---

# Running Momentum

Start the Flask application:

```bash
python app.py
```

Open your browser and navigate to:

```
http://localhost:5000
```

---

# Data Storage

Momentum automatically creates a local data directory:

```
~/.momentum/
```

Inside you will find:

```
main.db    → SQLite database with your tasks
```

The database can be inspected or backed up manually.

---

# API Endpoints

Momentum exposes a RESTful API for programmatic access:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | Get all tasks (optional: `?status=active` or `?status=completed`) |
| GET | `/api/tasks/<id>` | Get a single task |
| POST | `/api/tasks` | Create a new task (body: `{title, content}`) |
| PUT | `/api/tasks/<id>` | Update a task (body: `{title?, content?, completed?}`) |
| DELETE | `/api/tasks/<id>` | Delete a task |
| POST | `/api/tasks/toggle/<id>` | Toggle task completion |

---

# Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Recommended tools:

- black (formatting)
- pytest (testing)
- mypy (type checking)
- isort (import sorting)

Run tests:

```bash
pytest
```

---

# Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `/` | Focus on the task title input |
| `Esc` | Close edit modal |

---

# Contributing

Contributions are welcome!

Please feel free to submit issues and pull requests.

---

# License

MIT License

Copyright (c) mek0124

---

# Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy
- **Database:** SQLite
- **Frontend:** Vanilla HTML, CSS, JavaScript
- **Fonts:** Inter (Google Fonts)
