#!/bin/bash

if [ -d ./dist ]; then
  rm -rf ./dist
fi

if [ -d ./build ]; then
  rm -rf ./build
fi

pyinstaller --onefile --windowed --add-data "app/data:app/data" main.py

bash ./run.sh
