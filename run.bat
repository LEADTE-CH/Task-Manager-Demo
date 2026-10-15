@echo off
title BluePrint Suite (Tkinter)
echo Starting BluePrint Modern Suite...
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Python failed to start. Ensure Python is installed and added to PATH.
    pause
)
