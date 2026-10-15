# BluePrint - Modern Blue & White Task & Productivity Suite (Tkinter)

A clean, responsive desktop application built with Python and `tkinter`. Designed with an attractive blue-and-white theme, intuitive cards, high-contrast accessible typography, and decoupled object-oriented architecture.

---

## 🚀 Quick Start

### Windows
Double-click **`run.bat`** or run in Command Prompt / PowerShell:
```cmd
python main.py
```

### macOS & Linux
Make `run.sh` executable and launch, or run directly:
```bash
chmod +x run.sh
./run.sh
# Or directly:
python3 main.py
```

*Note on Linux:* If Tkinter is not already installed on your distribution:
```bash
# Ubuntu / Debian / Mint
sudo apt-get install python3-tk

# Fedora / RedHat
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

---

## 🎨 Design Highlights
- **Palette:** Deep Navy (`#1E3A8A`), Royal Blue (`#2563EB`), Soft Ice Blue (`#EFF6FF`), and Crisp Card White (`#FFFFFF`).
- **Responsive Layout:** Dynamic canvas scrolling, flexible column grid, accessible typography.
- **Accessibility:** High-contrast text colors matching WCAG AA/AAA standards.

---

## 📁 File Structure
- `main.py`: Entry point and Tk initialization.
- `gui_app.py`: `ModernTkinterApp` class managing views (Tasks, Notes, Analytics, Settings).
- `styles.py`: Color tokens, ttk custom styles, and font metrics.
- `logic.py`: Object-oriented data models (`TaskItem`, `NoteItem`, `TaskManager`, `NoteManager`).
- `tasks_data.json` & `notes_data.json`: Local JSON persistence stores.
