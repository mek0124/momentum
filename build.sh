#!/bin/bash

# Task Manager Build Script

clear

if [ -d ./dist ]; then
  rm -rf ./dist
fi

if [ -d ./build ]; then
  rm -rf ./build
fi

python3 -m build
