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

uv pip freeze > requirements.txt