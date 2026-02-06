<table align="center">
  <tr>
    <th><img src="./app/assets/icon.png" width="60" height="60" /></th>
    <th>Momentum</th>
    <th>v2.0.0</th>
  </tr>
</table>

<div align="center">
  
  ![Momentum](https://img.shields.io/badge/Momentum-local--first-blue)
  ![Python](https://img.shields.io/badge/Python-3.12+-blue)
  ![PySide6](https://img.shields.io/badge/PySide6-6.9+-green)
  ![License](https://img.shields.io/badge/License-MIT-green)
</div>


Momentum is a task manager built with PySide6 and SQLAlchemy

-- FOSS --MIT Licensed --**local-first** --minimalist --No online accounts --No online cloud --No tracking

Just You and Your Tasks...

---

## Why Momentum?

Most task managers are bloated, cloud-dependent, or opinionated.
Momentums' FOSS version is intentionally boring — fast, local, and hackable.

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
# clone the repo
git clone https://github.com/mek0124/momentum.git

# cd into the project
cd momentum

# create the virtual environment
python -m venv .venv

# activate the virtual environment
# linux/mac
source .venv/bin/activate

# windows
.venv\Scripts\Activate.ps1

# install the dependencies
pip install -r pyproject.toml"
```

Create `.env`:

```env
SECRET_KEY=change-me
SQLALCHEMY_DB_URL=sqlite:///./core/storage/main.db
```

Run:

```bash
# linux/mac
python3 main.py

# windows
python main.py
```

> The latest release also comes with an executable that <u>is **not** compatible</u> with Windows.

---

## Project Layout

|parent|sub-parent|file|description|
|-|-|-|-|
|app|||Momentum main application|
|||app.py|Momentum main window class|
||assets|| static assets folder|
|||icon.png| icon|
||core|| logic layer|
|||logic.py| logic class|
||database|| data layer|
|||db.py| database configuration|
||models|| data validation layer|
|||task.py|validation class for task|
||pages||ui layer|
|||dashboard.py|user landing screen|
||storage||app/user data storage folder|
|||config.json|user permissions storage file|
|||main.db|user task database file|
||utils||utilities folder|
|||color_theme.py|color theme file|
|updater|||Momentum update application|
|||app.py|Momentum update window class|
||pages||ui layer|
|||dashboard.py|user landing screen|
||utils||utilities folder|
|||update_thread.py|update utility class|

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
