# Momentum

![Momentum](https://img.shields.io/badge/Momentum-local--first-blue)
![Python](https://img.shields.io/badge/Python-3.12+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0+-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

Momentum is a **local-first**, minimalist task manager built with Flask and SQLAlchemy.
No accounts. No cloud. No tracking. Just tasks.

---

## Why Momentum?

Most task managers are bloated, cloud-dependent, or opinionated.
Momentum is intentionally boring — fast, local, and hackable.

- 🗂 Local SQLite database
- 🌓 Dark UI, modern CSS
- ⚡ Zero JS frameworks
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
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

Create `.env`:

```env
SECRET_KEY=change-me
SQLALCHEMY_DB_URL=sqlite:///./core/storage/main.db
```

Run:

```bash
python -m flask --app main run --debug
```

Open http://localhost:5000

---

## Project Layout

```
core/        database + models
static/     css + assets
templates/  jinja templates
main.py     flask app
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
