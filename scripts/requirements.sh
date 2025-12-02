#!/bin/bash

# Check if script is being run from project root
if [ ! -d "tm_config" ] && [ ! -d "tm_core" ] && [ ! -d "tm_storage" ]; then
    echo "Error: This script must be run from the task-manager project root directory."
    echo "Please navigate to the project root and try again."
    echo "Example: cd /path/to/task-manager && bash scripts/requirements.sh"
    exit 1
fi

echo -e "Checking and upgrading existing requirements... Please Wait..."

# Check if requirements.txt exists and upgrade dependencies
if [ -f "requirements.txt" ]; then
    echo "Found existing requirements.txt. Upgrading dependencies..."

    uv pip install --upgrade -r requirements.txt  
fi

echo -e "Install project dependencies"

uv pip install \
  setuptools \
  wheel \
  bcrypt \
  click \
  pyside6 \
  pytest \
  python-dotenv \
  sqlalchemy \
  textual \
  tm_config \
  tm_core \
  tm_storage \
  tm_cli
