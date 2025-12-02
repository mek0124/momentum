#!bin/bash

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
  sqlalchemy

echo -e "Installed Application DEV Dependencies... Please Wait..."

uv pip install \
  pytest

echo -e "Creating requirements.txt"

uv pip freeze > requirements.txt

read -p "Installation Finished. Press Enter to Exit..."
exit