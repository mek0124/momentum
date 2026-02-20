Change Log for Momentum

> Note: so I'm a dutz and forgot to run a change log from conception T_T so here we go

### 02/04/2026 - Added Updater Application

- created updater app
- started updater incorporation in main.py
- started UI for updater
  - dashboard page that displays update announcement
    - No button -> launches app at current version
    - Yes button -> updates application to newest version and then launches the main application
  - changelog page which displays the changelog of the application to the user for reading
- merged update thread to separate file
- updated splash screen progress bar to be more fluid
- updated readme

### 02/19/2026 - cleaned up files
- removed 'redo/' from .gitignore
- corrected package name in pyproject.toml
  - from: qfluentwidgets>=x.x.x
  - to: pyside6-fluent-widgets>=x.x.x