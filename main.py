"""
Main Entry Point for BluePrint Tkinter Desktop Application
Run with:
    python main.py
"""

import sys
import os

try:
    import tkinter as tk
except ImportError:
    print("Error: Python tkinter module is required to run the desktop GUI.")
    print("On Ubuntu/Debian, install with: sudo apt install python3-tk")
    print("On Fedora, install with: sudo dnf install python3-tkinter")
    print("On macOS / Windows, Python standard installations include Tkinter by default.")
    sys.exit(1)

from gui_app import ModernTkinterApp

def main():
    root = tk.Tk()
    app = ModernTkinterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
