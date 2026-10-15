#!/usr/bin/env bash
echo "Launching BluePrint Tkinter Desktop App..."
if command -v python3 &>/dev/null; then
    python3 main.py
elif command -v python &>/dev/null; then
    python main.py
else
    echo "Python 3 is required to run this application."
    exit 1
fi
