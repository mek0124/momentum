#!/bin/bash

# Check if script is being run from project root
if [ ! -f "pyproject.toml" ] && [ ! -d "config" ] && [ ! -d "core" ] && [ ! -d "storage" ]; then
    echo "Error: This script must be run from the task-manager project root directory."
    echo "Please navigate to the project root and try again."
    echo "Example: cd /path/to/task-manager && bash scripts/requirements.sh"
    exit 1
fi

echo -e "Installing Application Self-Libraries... Please Wait..."

uv pip install -e config
uv pip install -e core
uv pip install -e storage

echo -e "Installing Application Dependencies... Please Wait..."

uv pip install \
  wheel \
  setuptools \
  click \
  textual \
  pyside6 \
  python-dotenv \
  bcrypt \
  sqlalchemy \
  pytest

uv pip freeze > requirements.txt

echo -e "Installation complete! Dependencies saved to requirements.txt"
