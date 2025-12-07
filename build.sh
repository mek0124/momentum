#!/bin/bash

clear

echo -e "Building Project... Please Wait..."

sleep 2

if [ -d ./dist ]; then
  echo -e "\ndist directory detected"
  echo -e "Removing dist directory"
  rm -rf ./dist
  echo -e "dist directory removed"
fi

if [ -d ./build ]; then
  echo -e "\nbuild directory detected"
  echo -e "Removing build directory"
  rm -rf ./build
  echo -e "build directory removed"
fi

sleep 1

echo -e "\nBuilding project using: 'pyinstaller --onefile --windowed --add-data \"app/data:app/data\" main.py' \n"

sleep 2

pyinstaller --onefile --windowed --add-data "app/data:app/data" main.py

echo -e "\nBuild completed... Press enter to exit.."
read
exit
