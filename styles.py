"""
Styles and Theme Configuration for BluePrint Tkinter App
Implements an attractive, clean blue-and-white visual identity.
"""

import tkinter as tk
from tkinter import ttk

# Colors
COLOR_BG_WINDOW = "#F1F5F9"      # Very light slate/white background
COLOR_CARD_BG = "#FFFFFF"        # Pure white card
COLOR_HEADER_BG = "#1E3A8A"      # Deep classic Navy Blue
COLOR_PRIMARY_BLUE = "#2563EB"   # Vibrant Royal Blue
COLOR_PRIMARY_HOVER = "#1D4ED8"  # Darker blue on hover
COLOR_ACCENT_LIGHT = "#DBEAFE"   # Soft ice blue
COLOR_ACCENT_SUBTLE = "#EFF6FF"  # Very faint blue highlight
COLOR_BORDER = "#CBD5E1"         # Crisp slate border
COLOR_BORDER_LIGHT = "#E2E8F0"   # Light border
COLOR_TEXT_MAIN = "#0F172A"      # Charcoal slate for maximum readability
COLOR_TEXT_MUTED = "#64748B"     # Slate grey
COLOR_TEXT_LIGHT = "#94A3B8"     # Faint slate
COLOR_TEXT_WHITE = "#FFFFFF"     # White text
COLOR_SUCCESS = "#10B981"        # Emerald green
COLOR_WARNING = "#F59E0B"        # Amber
COLOR_DANGER = "#EF4444"         # Red for urgent tasks

# Typography fonts
FONT_FAMILY = "Segoe UI" if tk.TkVersion >= 8.6 else "Helvetica"
FONT_TITLE = (FONT_FAMILY, 15, "bold")
FONT_HEADING = (FONT_FAMILY, 12, "bold")
FONT_SUBHEADING = (FONT_FAMILY, 11, "bold")
FONT_BODY = (FONT_FAMILY, 10, "normal")
FONT_BODY_BOLD = (FONT_FAMILY, 10, "bold")
FONT_SMALL = (FONT_FAMILY, 9, "normal")
FONT_BADGE = (FONT_FAMILY, 8, "bold")


def apply_theme(root: tk.Tk):
    """Configures the Tkinter root and ttk.Style for a modern Blue & White UI."""
    try:
        # Enable DPI awareness on Windows if applicable
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    style = ttk.Style(root)

    # Use 'clam' or 'alt' as base theme for consistent cross-platform styling
    available = style.theme_names()
    if "clam" in available:
        style.theme_use("clam")

    # General Frame styles
    style.configure("TFrame", background=COLOR_BG_WINDOW)
    style.configure("Card.TFrame", background=COLOR_CARD_BG, relief="flat")
    style.configure("Header.TFrame", background=COLOR_HEADER_BG)
    style.configure("Sidebar.TFrame", background=COLOR_CARD_BG)

    # Label styles
    style.configure("TLabel", background=COLOR_BG_WINDOW, foreground=COLOR_TEXT_MAIN, font=FONT_BODY)
    style.configure("Card.TLabel", background=COLOR_CARD_BG, foreground=COLOR_TEXT_MAIN, font=FONT_BODY)
    style.configure("Title.TLabel", background=COLOR_CARD_BG, foreground=COLOR_PRIMARY_BLUE, font=FONT_HEADING)
    style.configure("Muted.TLabel", background=COLOR_CARD_BG, foreground=COLOR_TEXT_MUTED, font=FONT_SMALL)
    style.configure("HeaderTitle.TLabel", background=COLOR_HEADER_BG, foreground=COLOR_TEXT_WHITE, font=FONT_TITLE)
    style.configure("HeaderSub.TLabel", background=COLOR_HEADER_BG, foreground=COLOR_ACCENT_LIGHT, font=FONT_SMALL)

    # Primary Blue Button
    style.configure(
        "Primary.TButton",
        background=COLOR_PRIMARY_BLUE,
        foreground=COLOR_TEXT_WHITE,
        font=FONT_BODY_BOLD,
        borderwidth=0,
        focuscolor="none",
        padding=(14, 8)
    )
    style.map(
        "Primary.TButton",
        background=[("active", COLOR_PRIMARY_HOVER), ("pressed", COLOR_HEADER_BG)],
        foreground=[("active", COLOR_TEXT_WHITE)]
    )

    # Secondary Outline Button
    style.configure(
        "Secondary.TButton",
        background=COLOR_CARD_BG,
        foreground=COLOR_PRIMARY_BLUE,
        font=FONT_BODY,
        borderwidth=1,
        bordercolor=COLOR_BORDER,
        focuscolor="none",
        padding=(12, 6)
    )
    style.map(
        "Secondary.TButton",
        background=[("active", COLOR_ACCENT_SUBTLE), ("pressed", COLOR_ACCENT_LIGHT)],
        foreground=[("active", COLOR_PRIMARY_HOVER)]
    )

    # Danger Button
    style.configure(
        "Danger.TButton",
        background="#FEE2E2",
        foreground=COLOR_DANGER,
        font=FONT_SMALL,
        borderwidth=0,
        padding=(8, 4)
    )
    style.map("Danger.TButton", background=[("active", "#FECACA")])

    # Navigation / Tab Button
    style.configure(
        "Nav.TButton",
        background=COLOR_CARD_BG,
        foreground=COLOR_TEXT_MAIN,
        font=FONT_BODY_BOLD,
        anchor="w",
        padding=(16, 10),
        borderwidth=0
    )
    style.map(
        "Nav.TButton",
        background=[("active", COLOR_ACCENT_SUBTLE), ("selected", COLOR_ACCENT_LIGHT)],
        foreground=[("active", COLOR_PRIMARY_BLUE), ("selected", COLOR_PRIMARY_BLUE)]
    )

    # Entry and Combobox
    style.configure(
        "TEntry",
        fieldbackground=COLOR_CARD_BG,
        foreground=COLOR_TEXT_MAIN,
        bordercolor=COLOR_BORDER,
        padding=6
    )
    style.configure(
        "TCombobox",
        fieldbackground=COLOR_CARD_BG,
        foreground=COLOR_TEXT_MAIN,
        bordercolor=COLOR_BORDER,
        padding=6
    )

    # Notebook tabs (if used)
    style.configure("TNotebook", background=COLOR_BG_WINDOW, borderwidth=0)
    style.configure("TNotebook.Tab", background=COLOR_ACCENT_SUBTLE, foreground=COLOR_TEXT_MAIN, padding=(16, 8), font=FONT_BODY_BOLD)
    style.map("TNotebook.Tab", background=[("selected", COLOR_PRIMARY_BLUE)], foreground=[("selected", COLOR_TEXT_WHITE)])

    # Progressbar
    style.configure("Horizontal.TProgressbar", troughcolor=COLOR_ACCENT_SUBTLE, background=COLOR_PRIMARY_BLUE, thickness=8)

    # Checkbutton
    style.configure("Card.TCheckbutton", background=COLOR_CARD_BG, foreground=COLOR_TEXT_MAIN, font=FONT_BODY)
    style.map("Card.TCheckbutton", background=[("active", COLOR_CARD_BG)])
