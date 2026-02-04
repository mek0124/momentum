# Momentum

![Momentum](https://img.shields.io/badge/Momentum-local--first-blue)
![Python](https://img.shields.io/badge/Python-3.12+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0+-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

Momentum is a **local-first**, minimalist task manager built with PySide6 and SQLAlchemy.
No accounts. No cloud. No tracking. Just tasks.

---

## Why Momentum?

Most task managers are bloated, cloud-dependent, or opinionated.
Momentum is intentionally boring, fast, and local.

- 🗂 Local SQLite database
- 🌓 Dark UI, modern CSS
- 🔒 Your data never leaves your machine

---

## Features

- Create, edit, delete tasks
- Priority levels (Low / Medium / High)
- Optional due dates & times
- Live clock UI
- Responsive layout
- Session-based identity (no passwords)

---

## Install

```bash
git clone https://github.com/mek0124/momentum.git
cd momentum
python3 -m venv .venv

# linux
source .venv/bin/activate

# windows
.venv\Scripts\Activate.ps1

pip install -r pyproject.toml
```

Create `.env`:

```env
SECRET_KEY=change-me
SQLALCHEMY_DB_URL=sqlite:///./core/storage/main.db
```

Run:

```bash
python3 main.py
```

---

## Project Layout

```
- app/
  - assets/ - holds images
  - database/ - SQLAlchemy Database Configuration
  - models/ - An SQLAlchemy ORM for the Task
  - pages/ - the UI layer folder
  - storage/ - home of the database folder
  - utils/ - a centralized area for configs and color themes
- main.py - the main entry file
```

---

## Philosophy

Momentum follows a few rules:

- Local-first always
- Simple > clever
- Readable code > abstractions
- Ship features that matter

---

## License

MIT © mek0124
