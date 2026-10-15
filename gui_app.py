"""
Modern Tkinter Application GUI
Implements a responsive, clean blue-and-white user interface for the desktop app.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from logic import TaskManager, NoteManager, TaskItem, NoteItem
import styles

class ModernTkinterApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("BluePrint - Modern Task & Productivity Suite")
        self.root.geometry("1024x680")
        self.root.minsize(800, 540)
        self.root.configure(bg=styles.COLOR_BG_WINDOW)

        # Initialize Managers
        self.task_manager = TaskManager()
        self.note_manager = NoteManager()

        # UI state
        self.current_tab = "tasks"
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_content())
        self.filter_category = tk.StringVar(value="All")
        self.filter_priority = tk.StringVar(value="All")
        self.filter_status = tk.StringVar(value="All")

        # Apply Theme
        styles.apply_theme(self.root)

        # Build Layout
        self.build_header()
        self.build_main_container()

        # Initial view
        self.switch_tab("tasks")

    def build_header(self):
        """Top blue header bar with title, quick stats, and date."""
        self.header_frame = tk.Frame(self.root, bg=styles.COLOR_HEADER_BG, height=64)
        self.header_frame.pack(side="top", fill="x")

        # Inner container with padding
        inner = tk.Frame(self.header_frame, bg=styles.COLOR_HEADER_BG)
        inner.pack(fill="x", padx=24, pady=12)

        # Left branding
        brand_frame = tk.Frame(inner, bg=styles.COLOR_HEADER_BG)
        brand_frame.pack(side="left")

        logo_badge = tk.Label(
            brand_frame,
            text="BP",
            font=(styles.FONT_FAMILY, 11, "bold"),
            bg=styles.COLOR_PRIMARY_BLUE,
            fg=styles.COLOR_TEXT_WHITE,
            padx=8,
            pady=3
        )
        logo_badge.pack(side="left", padx=(0, 10))

        title_label = tk.Label(
            brand_frame,
            text="BluePrint Suite",
            font=styles.FONT_TITLE,
            bg=styles.COLOR_HEADER_BG,
            fg=styles.COLOR_TEXT_WHITE
        )
        title_label.pack(side="left")

        tagline = tk.Label(
            brand_frame,
            text="| Digital Productivity",
            font=styles.FONT_SMALL,
            bg=styles.COLOR_HEADER_BG,
            fg=styles.COLOR_ACCENT_LIGHT
        )
        tagline.pack(side="left", padx=8)

        # Right status
        right_frame = tk.Frame(inner, bg=styles.COLOR_HEADER_BG)
        right_frame.pack(side="right")

        today_str = datetime.datetime.now().strftime("%A, %B %d")
        self.date_label = tk.Label(
            right_frame,
            text=today_str,
            font=styles.FONT_BODY,
            bg=styles.COLOR_HEADER_BG,
            fg=styles.COLOR_ACCENT_LIGHT
        )
        self.date_label.pack(side="right", padx=10)

    def build_main_container(self):
        """Builds sidebar and dynamic content area."""
        self.body_frame = tk.Frame(self.root, bg=styles.COLOR_BG_WINDOW)
        self.body_frame.pack(side="top", fill="both", expand=True)

        # Left Sidebar Navigation
        self.sidebar_frame = tk.Frame(self.body_frame, bg=styles.COLOR_CARD_BG, width=220, highlightthickness=1, highlightbackground=styles.COLOR_BORDER_LIGHT)
        self.sidebar_frame.pack(side="left", fill="y", padx=(16, 8), pady=16)
        self.sidebar_frame.pack_propagate(False)

        # Sidebar Title
        nav_header = tk.Label(
            self.sidebar_frame,
            text="NAVIGATION",
            font=styles.FONT_BADGE,
            bg=styles.COLOR_CARD_BG,
            fg=styles.COLOR_TEXT_MUTED
        )
        nav_header.pack(anchor="w", padx=20, pady=(20, 10))

        # Nav Buttons
        self.nav_buttons = {}
        items = [
            ("tasks", " Tasks & Milestones"),
            ("notes", " Smart Notes"),
            ("analytics", " Analytics & Stats"),
            ("export", " Data & System")
        ]

        for key, label in items:
            btn = tk.Button(
                self.sidebar_frame,
                text=label,
                font=styles.FONT_BODY_BOLD,
                bg=styles.COLOR_CARD_BG,
                fg=styles.COLOR_TEXT_MAIN,
                activebackground=styles.COLOR_ACCENT_SUBTLE,
                activeforeground=styles.COLOR_PRIMARY_BLUE,
                relief="flat",
                bd=0,
                anchor="w",
                padx=16,
                pady=10,
                cursor="hand2",
                command=lambda k=key: self.switch_tab(k)
            )
            btn.pack(fill="x", padx=8, pady=3)
            self.nav_buttons[key] = btn

        # Quick stats summary card at bottom of sidebar
        self.build_sidebar_stats()

        # Right Dynamic Content Area
        self.content_frame = tk.Frame(self.body_frame, bg=styles.COLOR_BG_WINDOW)
        self.content_frame.pack(side="left", fill="both", expand=True, padx=(8, 16), pady=16)

    def build_sidebar_stats(self):
        """Displays completion metrics in the sidebar."""
        stats_container = tk.Frame(self.sidebar_frame, bg=styles.COLOR_ACCENT_SUBTLE, padx=12, pady=12, highlightthickness=1, highlightbackground=styles.COLOR_BORDER_LIGHT)
        stats_container.pack(side="bottom", fill="x", padx=12, pady=16)

        lbl = tk.Label(stats_container, text="QUICK SUMMARY", font=styles.FONT_BADGE, bg=styles.COLOR_ACCENT_SUBTLE, fg=styles.COLOR_PRIMARY_BLUE)
        lbl.pack(anchor="w")

        self.sidebar_stats_label = tk.Label(
            stats_container,
            text="Loading stats...",
            font=styles.FONT_SMALL,
            bg=styles.COLOR_ACCENT_SUBTLE,
            fg=styles.COLOR_TEXT_MAIN,
            justify="left"
        )
        self.sidebar_stats_label.pack(anchor="w", pady=(6, 0))

    def update_sidebar_stats(self):
        stats = self.task_manager.get_stats()
        text = f"Total Tasks: {stats['total']}\nDone: {stats['completed']} ({stats['completion_rate']}%)\nUrgent: {stats['urgent']}"
        self.sidebar_stats_label.config(text=text)

    def switch_tab(self, tab_name: str):
        self.current_tab = tab_name

        # Highlight active button
        for key, btn in self.nav_buttons.items():
            if key == tab_name:
                btn.config(bg=styles.COLOR_ACCENT_LIGHT, fg=styles.COLOR_PRIMARY_BLUE)
            else:
                btn.config(bg=styles.COLOR_CARD_BG, fg=styles.COLOR_TEXT_MAIN)

        self.refresh_content()
        self.update_sidebar_stats()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def refresh_content(self):
        self.clear_content()
        if self.current_tab == "tasks":
            self.render_tasks_view()
        elif self.current_tab == "notes":
            self.render_notes_view()
        elif self.current_tab == "analytics":
            self.render_analytics_view()
        elif self.current_tab == "export":
            self.render_export_view()
        self.update_sidebar_stats()

    # ==========================
    # TASKS VIEW
    # ==========================
    def render_tasks_view(self):
        # Action Bar (Title, Search, Add Task)
        top_bar = tk.Frame(self.content_frame, bg=styles.COLOR_CARD_BG, padx=16, pady=12, highlightthickness=1, highlightbackground=styles.COLOR_BORDER_LIGHT)
        top_bar.pack(fill="x", pady=(0, 12))

        # Title
        t_label = tk.Label(top_bar, text="Tasks & Milestones", font=styles.FONT_TITLE, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_PRIMARY_BLUE)
        t_label.pack(side="left")

        # Add Task Button
        add_btn = tk.Button(
            top_bar,
            text="+ Add New Task",
            font=styles.FONT_BODY_BOLD,
            bg=styles.COLOR_PRIMARY_BLUE,
            fg=styles.COLOR_TEXT_WHITE,
            activebackground=styles.COLOR_PRIMARY_HOVER,
            activeforeground=styles.COLOR_TEXT_WHITE,
            relief="flat",
            bd=0,
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.open_add_task_dialog
        )
        add_btn.pack(side="right")

        # Filters and Search Bar
        filter_bar = tk.Frame(self.content_frame, bg=styles.COLOR_BG_WINDOW)
        filter_bar.pack(fill="x", pady=(0, 12))

        # Search Entry
        search_frame = tk.Frame(filter_bar, bg=styles.COLOR_CARD_BG, highlightthickness=1, highlightbackground=styles.COLOR_BORDER, padx=8, pady=4)
        search_frame.pack(side="left", fill="x", expand=True, padx=(0, 8))

        s_icon = tk.Label(search_frame, text="🔍", bg=styles.COLOR_CARD_BG, fg=styles.COLOR_TEXT_MUTED)
        s_icon.pack(side="left", padx=(2, 6))

        s_entry = tk.Entry(search_frame, textvariable=self.search_var, font=styles.FONT_BODY, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_TEXT_MAIN, bd=0, relief="flat")
        s_entry.pack(side="left", fill="x", expand=True)

        # Status filter dropdown
        s_combo = ttk.Combobox(filter_bar, values=["All", "Active", "Completed"], textvariable=self.filter_status, state="readonly", width=12)
        s_combo.pack(side="left", padx=4)
        s_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_content())

        # Category filter dropdown
        c_combo = ttk.Combobox(filter_bar, values=["All", "General", "Work", "Personal", "Projects"], textvariable=self.filter_category, state="readonly", width=12)
        c_combo.pack(side="left", padx=4)
        c_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_content())

        # Priority filter dropdown
        p_combo = ttk.Combobox(filter_bar, values=["All", "Low", "Medium", "High", "Urgent"], textvariable=self.filter_priority, state="readonly", width=12)
        p_combo.pack(side="left", padx=4)
        p_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_content())

        # Scrollable Task List
        list_container = tk.Frame(self.content_frame, bg=styles.COLOR_BG_WINDOW)
        list_container.pack(fill="both", expand=True)

        canvas = tk.Canvas(list_container, bg=styles.COLOR_BG_WINDOW, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=styles.COLOR_BG_WINDOW)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=740)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Fetch filtered tasks
        tasks = self.task_manager.get_filtered_tasks(
            search=self.search_var.get(),
            category=self.filter_category.get(),
            priority=self.filter_priority.get(),
            status=self.filter_status.get()
        )

        if not tasks:
            empty_card = tk.Frame(scrollable_frame, bg=styles.COLOR_CARD_BG, padx=24, pady=32, highlightthickness=1, highlightbackground=styles.COLOR_BORDER_LIGHT)
            empty_card.pack(fill="x", pady=8)
            tk.Label(empty_card, text="No tasks found matching your filter criteria.", font=styles.FONT_HEADING, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_TEXT_MUTED).pack()
            tk.Label(empty_card, text="Try adjusting your search or add a new task above.", font=styles.FONT_SMALL, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_TEXT_LIGHT).pack(pady=4)
            return

        for task in tasks:
            self.render_task_item(scrollable_frame, task)

    def render_task_item(self, parent, task: TaskItem):
        card = tk.Frame(parent, bg=styles.COLOR_CARD_BG, padx=16, pady=12, highlightthickness=1, highlightbackground=styles.COLOR_BORDER_LIGHT)
        card.pack(fill="x", pady=4)

        # Checkbox toggle
        chk_val = tk.BooleanVar(value=task.completed)

        def on_toggle():
            self.task_manager.toggle_task(task.id)
            self.refresh_content()

        chk = tk.Checkbutton(
            card,
            variable=chk_val,
            command=on_toggle,
            bg=styles.COLOR_CARD_BG,
            activebackground=styles.COLOR_CARD_BG,
            relief="flat",
            bd=0,
            cursor="hand2"
        )
        chk.pack(side="left", padx=(0, 10))

        # Task Text Container
        text_frame = tk.Frame(card, bg=styles.COLOR_CARD_BG)
        text_frame.pack(side="left", fill="both", expand=True)

        title_font = (styles.FONT_FAMILY, 10, "overstrike") if task.completed else styles.FONT_BODY_BOLD
        title_color = styles.COLOR_TEXT_MUTED if task.completed else styles.COLOR_TEXT_MAIN

        t_lbl = tk.Label(text_frame, text=task.title, font=title_font, fg=title_color, bg=styles.COLOR_CARD_BG, anchor="w")
        t_lbl.pack(fill="x")

        if task.description:
            d_lbl = tk.Label(text_frame, text=task.description, font=styles.FONT_SMALL, fg=styles.COLOR_TEXT_MUTED, bg=styles.COLOR_CARD_BG, anchor="w")
            d_lbl.pack(fill="x", pady=(2, 0))

        # Meta tags (Category, Priority, Due)
        meta_frame = tk.Frame(text_frame, bg=styles.COLOR_CARD_BG)
        meta_frame.pack(fill="x", pady=(4, 0))

        # Category pill
        cat_lbl = tk.Label(
            meta_frame,
            text=f"📂 {task.category}",
            font=styles.FONT_BADGE,
            bg=styles.COLOR_ACCENT_SUBTLE,
            fg=styles.COLOR_PRIMARY_BLUE,
            padx=6,
            pady=2
        )
        cat_lbl.pack(side="left", padx=(0, 6))

        # Priority pill
        priority_colors = {
            "Urgent": (styles.COLOR_DANGER, "#FEE2E2"),
            "High": (styles.COLOR_WARNING, "#FEF3C7"),
            "Medium": (styles.COLOR_PRIMARY_BLUE, styles.COLOR_ACCENT_LIGHT),
            "Low": (styles.COLOR_TEXT_MUTED, "#F1F5F9")
        }
        p_fg, p_bg = priority_colors.get(task.priority, (styles.COLOR_PRIMARY_BLUE, styles.COLOR_ACCENT_LIGHT))

        p_lbl = tk.Label(
            meta_frame,
            text=f"⚡ {task.priority}",
            font=styles.FONT_BADGE,
            bg=p_bg,
            fg=p_fg,
            padx=6,
            pady=2
        )
        p_lbl.pack(side="left", padx=(0, 6))

        if task.due_date:
            due_lbl = tk.Label(meta_frame, text=f"⏱ {task.due_date}", font=styles.FONT_BADGE, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_TEXT_MUTED)
            due_lbl.pack(side="left")

        # Right actions (Delete button)
        del_btn = tk.Button(
            card,
            text="✕",
            font=styles.FONT_SMALL,
            bg=styles.COLOR_CARD_BG,
            fg=styles.COLOR_TEXT_LIGHT,
            activeforeground=styles.COLOR_DANGER,
            activebackground=styles.COLOR_CARD_BG,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda tid=task.id: self.delete_task(tid)
        )
        del_btn.pack(side="right", padx=4)

    def delete_task(self, task_id: str):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            self.task_manager.delete_task(task_id)
            self.refresh_content()

    def open_add_task_dialog(self):
        """Clean modal dialog to add a task."""
        dlg = tk.Toplevel(self.root)
        dlg.title("Add New Task")
        dlg.geometry("460x420")
        dlg.minsize(400, 380)
        dlg.configure(bg=styles.COLOR_CARD_BG)
        dlg.transient(self.root)
        dlg.grab_set()

        # Header
        h_frame = tk.Frame(dlg, bg=styles.COLOR_PRIMARY_BLUE, padx=20, pady=16)
        h_frame.pack(fill="x")
        tk.Label(h_frame, text="Create New Task", font=styles.FONT_HEADING, bg=styles.COLOR_PRIMARY_BLUE, fg=styles.COLOR_TEXT_WHITE).pack(anchor="w")

        body = tk.Frame(dlg, bg=styles.COLOR_CARD_BG, padx=20, pady=16)
        body.pack(fill="both", expand=True)

        # Title
        tk.Label(body, text="Task Title*", font=styles.FONT_BODY_BOLD, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_TEXT_MAIN).pack(anchor="w")
        t_entry = tk.Entry(body, font=styles.FONT_BODY, highlightthickness=1, highlightbackground=styles.COLOR_BORDER)
        t_entry.pack(fill="x", pady=(4, 12))
        t_entry.focus_set()

        # Description
        tk.Label(body, text="Description", font=styles.FONT_BODY_BOLD, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_TEXT_MAIN).pack(anchor="w")
        d_entry = tk.Entry(body, font=styles.FONT_BODY, highlightthickness=1, highlightbackground=styles.COLOR_BORDER)
        d_entry.pack(fill="x", pady=(4, 12))

        # Category and Priority row
        row = tk.Frame(body, bg=styles.COLOR_CARD_BG)
        row.pack(fill="x", pady=(0, 12))

        cat_col = tk.Frame(row, bg=styles.COLOR_CARD_BG)
        cat_col.pack(side="left", fill="x", expand=True, padx=(0, 8))
        tk.Label(cat_col, text="Category", font=styles.FONT_BODY_BOLD, bg=styles.COLOR_CARD_BG).pack(anchor="w")
        cat_combo = ttk.Combobox(cat_col, values=["General", "Work", "Personal", "Projects"], state="readonly")
        cat_combo.set("General")
        cat_combo.pack(fill="x", pady=(4, 0))

        pri_col = tk.Frame(row, bg=styles.COLOR_CARD_BG)
        pri_col.pack(side="left", fill="x", expand=True)
        tk.Label(pri_col, text="Priority", font=styles.FONT_BODY_BOLD, bg=styles.COLOR_CARD_BG).pack(anchor="w")
        pri_combo = ttk.Combobox(pri_col, values=["Low", "Medium", "High", "Urgent"], state="readonly")
        pri_combo.set("Medium")
        pri_combo.pack(fill="x", pady=(4, 0))

        # Due Date
        tk.Label(body, text="Due Date / Milestone", font=styles.FONT_BODY_BOLD, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_TEXT_MAIN).pack(anchor="w")
        due_entry = tk.Entry(body, font=styles.FONT_BODY, highlightthickness=1, highlightbackground=styles.COLOR_BORDER)
        due_entry.insert(0, "Today, 5:00 PM")
        due_entry.pack(fill="x", pady=(4, 16))

        # Submit button
        def save_and_close():
            title = t_entry.get().strip()
            if not title:
                messagebox.showerror("Validation Error", "Please enter a task title.", parent=dlg)
                return
            self.task_manager.add_task(
                title=title,
                description=d_entry.get().strip(),
                category=cat_combo.get(),
                priority=pri_combo.get(),
                due_date=due_entry.get().strip()
            )
            dlg.destroy()
            self.refresh_content()

        btn_row = tk.Frame(body, bg=styles.COLOR_CARD_BG)
        btn_row.pack(fill="x")

        save_btn = tk.Button(
            btn_row,
            text="Save Task",
            font=styles.FONT_BODY_BOLD,
            bg=styles.COLOR_PRIMARY_BLUE,
            fg=styles.COLOR_TEXT_WHITE,
            relief="flat",
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            command=save_and_close
        )
        save_btn.pack(side="right")

        cancel_btn = tk.Button(
            btn_row,
            text="Cancel",
            font=styles.FONT_BODY,
            bg=styles.COLOR_CARD_BG,
            fg=styles.COLOR_TEXT_MUTED,
            relief="flat",
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
            command=dlg.destroy
        )
        cancel_btn.pack(side="right", padx=8)

    # ==========================
    # NOTES VIEW
    # ==========================
    def render_notes_view(self):
        top_bar = tk.Frame(self.content_frame, bg=styles.COLOR_CARD_BG, padx=16, pady=12, highlightthickness=1, highlightbackground=styles.COLOR_BORDER_LIGHT)
        top_bar.pack(fill="x", pady=(0, 12))

        tk.Label(top_bar, text="Smart Notes & Quick Capture", font=styles.FONT_TITLE, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_PRIMARY_BLUE).pack(side="left")

        add_btn = tk.Button(
            top_bar,
            text="+ Add Note",
            font=styles.FONT_BODY_BOLD,
            bg=styles.COLOR_PRIMARY_BLUE,
            fg=styles.COLOR_TEXT_WHITE,
            activebackground=styles.COLOR_PRIMARY_HOVER,
            relief="flat",
            bd=0,
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.open_add_note_dialog
        )
        add_btn.pack(side="right")

        # Scrollable note list
        list_container = tk.Frame(self.content_frame, bg=styles.COLOR_BG_WINDOW)
        list_container.pack(fill="both", expand=True)

        canvas = tk.Canvas(list_container, bg=styles.COLOR_BG_WINDOW, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=styles.COLOR_BG_WINDOW)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=740)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        notes = self.note_manager.get_notes(search=self.search_var.get())

        if not notes:
            empty_card = tk.Frame(scrollable_frame, bg=styles.COLOR_CARD_BG, padx=24, pady=32, highlightthickness=1, highlightbackground=styles.COLOR_BORDER_LIGHT)
            empty_card.pack(fill="x", pady=8)
            tk.Label(empty_card, text="No notes found.", font=styles.FONT_HEADING, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_TEXT_MUTED).pack()
            return

        for note in notes:
            self.render_note_item(scrollable_frame, note)

    def render_note_item(self, parent, note: NoteItem):
        card = tk.Frame(parent, bg=styles.COLOR_CARD_BG, padx=16, pady=14, highlightthickness=1, highlightbackground=styles.COLOR_BORDER_LIGHT)
        card.pack(fill="x", pady=6)

        # Header row of card
        h_row = tk.Frame(card, bg=styles.COLOR_CARD_BG)
        h_row.pack(fill="x")

        pin_symbol = "📌 " if note.pinned else ""
        t_lbl = tk.Label(h_row, text=f"{pin_symbol}{note.title}", font=styles.FONT_HEADING, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_PRIMARY_BLUE)
        t_lbl.pack(side="left")

        # Right actions
        del_btn = tk.Button(
            h_row,
            text="✕",
            font=styles.FONT_SMALL,
            bg=styles.COLOR_CARD_BG,
            fg=styles.COLOR_TEXT_LIGHT,
            activeforeground=styles.COLOR_DANGER,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda nid=note.id: self.delete_note(nid)
        )
        del_btn.pack(side="right")

        pin_btn = tk.Button(
            h_row,
            text="Unpin" if note.pinned else "Pin",
            font=styles.FONT_SMALL,
            bg=styles.COLOR_CARD_BG,
            fg=styles.COLOR_TEXT_MUTED,
            activeforeground=styles.COLOR_PRIMARY_BLUE,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda nid=note.id: self.toggle_note_pin(nid)
        )
        pin_btn.pack(side="right", padx=6)

        # Content
        c_lbl = tk.Label(card, text=note.content, font=styles.FONT_BODY, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_TEXT_MAIN, justify="left", wraplength=700)
        c_lbl.pack(anchor="w", pady=(8, 8))

        # Footer row
        f_row = tk.Frame(card, bg=styles.COLOR_CARD_BG)
        f_row.pack(fill="x")

        tag_lbl = tk.Label(f_row, text=f"🏷 {note.tag}", font=styles.FONT_BADGE, bg=styles.COLOR_ACCENT_SUBTLE, fg=styles.COLOR_PRIMARY_BLUE, padx=6, pady=2)
        tag_lbl.pack(side="left")

        time_lbl = tk.Label(f_row, text=f"Updated: {note.updated_at}", font=styles.FONT_SMALL, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_TEXT_MUTED)
        time_lbl.pack(side="right")

    def toggle_note_pin(self, note_id: str):
        self.note_manager.toggle_pin(note_id)
        self.refresh_content()

    def delete_note(self, note_id: str):
        if messagebox.askyesno("Confirm Delete", "Delete this note?"):
            self.note_manager.delete_note(note_id)
            self.refresh_content()

    def open_add_note_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Add New Note")
        dlg.geometry("480x400")
        dlg.configure(bg=styles.COLOR_CARD_BG)
        dlg.transient(self.root)
        dlg.grab_set()

        h_frame = tk.Frame(dlg, bg=styles.COLOR_PRIMARY_BLUE, padx=20, pady=16)
        h_frame.pack(fill="x")
        tk.Label(h_frame, text="Create New Note", font=styles.FONT_HEADING, bg=styles.COLOR_PRIMARY_BLUE, fg=styles.COLOR_TEXT_WHITE).pack(anchor="w")

        body = tk.Frame(dlg, bg=styles.COLOR_CARD_BG, padx=20, pady=16)
        body.pack(fill="both", expand=True)

        tk.Label(body, text="Note Title*", font=styles.FONT_BODY_BOLD, bg=styles.COLOR_CARD_BG).pack(anchor="w")
        t_entry = tk.Entry(body, font=styles.FONT_BODY, highlightthickness=1, highlightbackground=styles.COLOR_BORDER)
        t_entry.pack(fill="x", pady=(4, 12))

        tk.Label(body, text="Content*", font=styles.FONT_BODY_BOLD, bg=styles.COLOR_CARD_BG).pack(anchor="w")
        c_text = tk.Text(body, font=styles.FONT_BODY, height=6, highlightthickness=1, highlightbackground=styles.COLOR_BORDER)
        c_text.pack(fill="both", expand=True, pady=(4, 12))

        row = tk.Frame(body, bg=styles.COLOR_CARD_BG)
        row.pack(fill="x", pady=(0, 16))

        tk.Label(row, text="Tag:", font=styles.FONT_BODY_BOLD, bg=styles.COLOR_CARD_BG).pack(side="left")
        tag_entry = tk.Entry(row, font=styles.FONT_BODY, width=16, highlightthickness=1, highlightbackground=styles.COLOR_BORDER)
        tag_entry.insert(0, "General")
        tag_entry.pack(side="left", padx=8)

        pin_var = tk.BooleanVar(value=False)
        pin_chk = tk.Checkbutton(row, text="Pin to top", variable=pin_var, bg=styles.COLOR_CARD_BG)
        pin_chk.pack(side="left", padx=12)

        def save_note():
            title = t_entry.get().strip()
            content = c_text.get("1.0", "end-1c").strip()
            if not title or not content:
                messagebox.showerror("Error", "Title and Content are required.", parent=dlg)
                return
            self.note_manager.add_note(title, content, tag=tag_entry.get().strip() or "General", pinned=pin_var.get())
            dlg.destroy()
            self.refresh_content()

        btn_row = tk.Frame(body, bg=styles.COLOR_CARD_BG)
        btn_row.pack(fill="x")
        save_btn = tk.Button(btn_row, text="Save Note", font=styles.FONT_BODY_BOLD, bg=styles.COLOR_PRIMARY_BLUE, fg=styles.COLOR_TEXT_WHITE, relief="flat", bd=0, padx=16, pady=8, cursor="hand2", command=save_note)
        save_btn.pack(side="right")

    # ==========================
    # ANALYTICS VIEW
    # ==========================
    def render_analytics_view(self):
        stats = self.task_manager.get_stats()

        top_bar = tk.Frame(self.content_frame, bg=styles.COLOR_CARD_BG, padx=16, pady=12, highlightthickness=1, highlightbackground=styles.COLOR_BORDER_LIGHT)
        top_bar.pack(fill="x", pady=(0, 16))
        tk.Label(top_bar, text="Analytics & Productivity Metrics", font=styles.FONT_TITLE, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_PRIMARY_BLUE).pack(side="left")

        # Stat cards row
        cards_row = tk.Frame(self.content_frame, bg=styles.COLOR_BG_WINDOW)
        cards_row.pack(fill="x", pady=(0, 16))

        metrics = [
            ("Total Tasks", str(stats["total"]), "All captured items", styles.COLOR_PRIMARY_BLUE),
            ("Completed", str(stats["completed"]), f"{stats['completion_rate']}% success rate", styles.COLOR_SUCCESS),
            ("Pending", str(stats["pending"]), "Remaining to finish", styles.COLOR_WARNING),
            ("Urgent Priority", str(stats["urgent"]), "Immediate attention", styles.COLOR_DANGER)
        ]

        for title, val, sub, color in metrics:
            card = tk.Frame(cards_row, bg=styles.COLOR_CARD_BG, padx=16, pady=16, highlightthickness=1, highlightbackground=styles.COLOR_BORDER_LIGHT)
            card.pack(side="left", fill="both", expand=True, padx=4)

            tk.Label(card, text=title, font=styles.FONT_SMALL, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_TEXT_MUTED).pack(anchor="w")
            tk.Label(card, text=val, font=(styles.FONT_FAMILY, 22, "bold"), bg=styles.COLOR_CARD_BG, fg=color).pack(anchor="w", pady=4)
            tk.Label(card, text=sub, font=styles.FONT_BADGE, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_TEXT_MUTED).pack(anchor="w")

        # Progress bar card
        p_card = tk.Frame(self.content_frame, bg=styles.COLOR_CARD_BG, padx=20, pady=20, highlightthickness=1, highlightbackground=styles.COLOR_BORDER_LIGHT)
        p_card.pack(fill="x", pady=(0, 16))

        tk.Label(p_card, text="Milestone Progress Overview", font=styles.FONT_HEADING, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_TEXT_MAIN).pack(anchor="w")
        p_bar = ttk.Progressbar(p_card, orient="horizontal", mode="determinate", value=stats["completion_rate"])
        p_bar.pack(fill="x", pady=(12, 6))

        tk.Label(p_card, text=f"Overall Completion: {stats['completion_rate']}% of milestones achieved", font=styles.FONT_BODY, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_TEXT_MUTED).pack(anchor="w")

        # Tips Card
        tips_card = tk.Frame(self.content_frame, bg=styles.COLOR_ACCENT_SUBTLE, padx=20, pady=16, highlightthickness=1, highlightbackground=styles.COLOR_BORDER)
        tips_card.pack(fill="x")

        tk.Label(tips_card, text="💡 Productivity Tip", font=styles.FONT_HEADING, bg=styles.COLOR_ACCENT_SUBTLE, fg=styles.COLOR_PRIMARY_BLUE).pack(anchor="w")
        tk.Label(tips_card, text="Prioritize your 'Urgent' items at the start of your workflow. Batch smaller tasks into 25-minute focused blocks to maintain momentum.", font=styles.FONT_BODY, bg=styles.COLOR_ACCENT_SUBTLE, fg=styles.COLOR_TEXT_MAIN, wraplength=700, justify="left").pack(anchor="w", pady=(6, 0))

    # ==========================
    # EXPORT & SYSTEM VIEW
    # ==========================
    def render_export_view(self):
        card = tk.Frame(self.content_frame, bg=styles.COLOR_CARD_BG, padx=24, pady=24, highlightthickness=1, highlightbackground=styles.COLOR_BORDER_LIGHT)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="Data Management & System Information", font=styles.FONT_TITLE, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_PRIMARY_BLUE).pack(anchor="w")
        tk.Label(card, text="Manage local persistence, backup JSON data, and configure application settings.", font=styles.FONT_BODY, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_TEXT_MUTED).pack(anchor="w", pady=(4, 20))

        # Action Buttons
        row1 = tk.Frame(card, bg=styles.COLOR_CARD_BG)
        row1.pack(fill="x", pady=6)

        tk.Button(row1, text="📁 Backup Data to JSON", font=styles.FONT_BODY_BOLD, bg=styles.COLOR_PRIMARY_BLUE, fg=styles.COLOR_TEXT_WHITE, relief="flat", bd=0, padx=16, pady=8, cursor="hand2", command=self.backup_data).pack(side="left")
        tk.Button(row1, text="🔄 Reload Default Datasets", font=styles.FONT_BODY, bg=styles.COLOR_CARD_BG, fg=styles.COLOR_PRIMARY_BLUE, relief="flat", bd=1, highlightbackground=styles.COLOR_BORDER, padx=14, pady=7, cursor="hand2", command=self.reset_defaults).pack(side="left", padx=10)

        # About Card
        about_frame = tk.Frame(card, bg=styles.COLOR_BG_WINDOW, padx=16, pady=16, highlightthickness=1, highlightbackground=styles.COLOR_BORDER_LIGHT)
        about_frame.pack(fill="x", pady=(24, 0))

        tk.Label(about_frame, text="About BluePrint Desktop Suite", font=styles.FONT_HEADING, bg=styles.COLOR_BG_WINDOW, fg=styles.COLOR_TEXT_MAIN).pack(anchor="w")
        tk.Label(about_frame, text="Designed with an attractive blue-and-white aesthetic, responsive ttk widgets, and clean decoupled logic classes.\nCompatible across Windows, macOS, and Linux.", font=styles.FONT_SMALL, bg=styles.COLOR_BG_WINDOW, fg=styles.COLOR_TEXT_MUTED, justify="left").pack(anchor="w", pady=(4, 0))

    def backup_data(self):
        self.task_manager.save()
        self.note_manager.save()
        messagebox.showinfo("Backup Successful", "Tasks and notes successfully saved to tasks_data.json and notes_data.json.")

    def reset_defaults(self):
        if messagebox.askyesno("Reset Data", "Reset tasks and notes to default samples?"):
            self.task_manager.seed_defaults()
            self.note_manager.seed_defaults()
            self.refresh_content()
            messagebox.showinfo("Reset Complete", "Default datasets restored.")
