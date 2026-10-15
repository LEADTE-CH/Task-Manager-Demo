"""
Logic Module for BluePrint Application
Provides data models, state managers, and calculation functions for tasks and notes.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Optional, Any
import json
import os

@dataclass
class TaskItem:
    id: str
    title: str
    description: str = ""
    category: str = "General"  # General, Work, Personal, Projects, Urgent
    priority: str = "Medium"   # Low, Medium, High, Urgent
    completed: bool = False
    created_at: str = ""
    due_date: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TaskItem":
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            category=data.get("category", "General"),
            priority=data.get("priority", "Medium"),
            completed=data.get("completed", False),
            created_at=data.get("created_at", ""),
            due_date=data.get("due_date", "")
        )


@dataclass
class NoteItem:
    id: str
    title: str
    content: str
    tag: str = "General"
    pinned: bool = False
    updated_at: str = ""

    def __post_init__(self):
        if not self.updated_at:
            self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NoteItem":
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            content=data.get("content", ""),
            tag=data.get("tag", "General"),
            pinned=data.get("pinned", False),
            updated_at=data.get("updated_at", "")
        )


class TaskManager:
    """Manages tasks with persistence and query operations."""

    def __init__(self, storage_file: str = "tasks_data.json"):
        self.storage_file = storage_file
        self.tasks: List[TaskItem] = []
        self.load()

    def add_task(self, title: str, description: str = "", category: str = "General",
                 priority: str = "Medium", due_date: str = "") -> TaskItem:
        task_id = f"task_{int(datetime.now().timestamp() * 1000)}"
        new_task = TaskItem(
            id=task_id,
            title=title.strip(),
            description=description.strip(),
            category=category,
            priority=priority,
            due_date=due_date
        )
        self.tasks.insert(0, new_task)
        self.save()
        return new_task

    def toggle_task(self, task_id: str) -> Optional[TaskItem]:
        for task in self.tasks:
            if task.id == task_id:
                task.completed = not task.completed
                self.save()
                return task
        return None

    def update_task(self, task_id: str, **kwargs) -> Optional[TaskItem]:
        for task in self.tasks:
            if task.id == task_id:
                for key, val in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, val)
                self.save()
                return task
        return None

    def delete_task(self, task_id: str) -> bool:
        initial_len = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        if len(self.tasks) < initial_len:
            self.save()
            return True
        return False

    def get_filtered_tasks(self, search: str = "", category: str = "All",
                           priority: str = "All", status: str = "All") -> List[TaskItem]:
        results = self.tasks
        if search:
            q = search.lower()
            results = [t for t in results if q in t.title.lower() or q in t.description.lower()]
        if category and category != "All":
            results = [t for t in results if t.category.lower() == category.lower()]
        if priority and priority != "All":
            results = [t for t in results if t.priority.lower() == priority.lower()]
        if status == "Active":
            results = [t for t in results if not t.completed]
        elif status == "Completed":
            results = [t for t in results if t.completed]
        return results

    def get_stats(self) -> Dict[str, Any]:
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.completed)
        pending = total - completed
        urgent = sum(1 for t in self.tasks if not t.completed and t.priority.lower() == "urgent")
        completion_rate = (completed / total * 100) if total > 0 else 0
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "urgent": urgent,
            "completion_rate": round(completion_rate, 1)
        }

    def save(self):
        try:
            data = [t.to_dict() for t in self.tasks]
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def load(self):
        if not os.path.exists(self.storage_file):
            self.seed_defaults()
            return
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = [TaskItem.from_dict(d) for d in data]
        except Exception:
            self.seed_defaults()

    def seed_defaults(self):
        self.tasks = [
            TaskItem(
                id="task_1",
                title="Review Q4 Project Deliverables & Objectives",
                description="Coordinate with team leads to finalize the upcoming release milestone.",
                category="Work",
                priority="Urgent",
                due_date="Today, 5:00 PM"
            ),
            TaskItem(
                id="task_2",
                title="Refactor UI design with clean blue and white aesthetic",
                description="Ensure crisp typography, accessible contrast, and intuitive navigation.",
                category="Projects",
                priority="High",
                completed=True,
                due_date="Completed"
            ),
            TaskItem(
                id="task_3",
                title="Verify responsive components on mobile & tablet viewport",
                description="Check touch targets, flexible flex-grids, and modal dialog behavior.",
                category="Projects",
                priority="Medium",
                due_date="Tomorrow"
            ),
            TaskItem(
                id="task_4",
                title="Weekly team sync & status architecture roundup",
                description="Present progress on the desktop Tkinter interface & zip package distribution.",
                category="Work",
                priority="Low",
                due_date="Friday, 10:00 AM"
            )
        ]
        self.save()


class NoteManager:
    """Manages notes with persistence and query operations."""

    def __init__(self, storage_file: str = "notes_data.json"):
        self.storage_file = storage_file
        self.notes: List[NoteItem] = []
        self.load()

    def add_note(self, title: str, content: str, tag: str = "General", pinned: bool = False) -> NoteItem:
        note_id = f"note_{int(datetime.now().timestamp() * 1000)}"
        new_note = NoteItem(
            id=note_id,
            title=title.strip(),
            content=content.strip(),
            tag=tag,
            pinned=pinned
        )
        if pinned:
            self.notes.insert(0, new_note)
        else:
            self.notes.append(new_note)
        self.save()
        return new_note

    def update_note(self, note_id: str, **kwargs) -> Optional[NoteItem]:
        for note in self.notes:
            if note.id == note_id:
                for key, val in kwargs.items():
                    if hasattr(note, key):
                        setattr(note, key, val)
                note.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.save()
                return note
        return None

    def delete_note(self, note_id: str) -> bool:
        initial_len = len(self.notes)
        self.notes = [n for n in self.notes if n.id != note_id]
        if len(self.notes) < initial_len:
            self.save()
            return True
        return False

    def toggle_pin(self, note_id: str) -> Optional[NoteItem]:
        for note in self.notes:
            if note.id == note_id:
                note.pinned = not note.pinned
                self.save()
                return note
        return None

    def get_notes(self, search: str = "") -> List[NoteItem]:
        res = sorted(self.notes, key=lambda n: not n.pinned)
        if search:
            q = search.lower()
            res = [n for n in res if q in n.title.lower() or q in n.content.lower() or q in n.tag.lower()]
        return res

    def save(self):
        try:
            data = [n.to_dict() for n in self.notes]
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving notes: {e}")

    def load(self):
        if not os.path.exists(self.storage_file):
            self.seed_defaults()
            return
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.notes = [NoteItem.from_dict(d) for d in data]
        except Exception:
            self.seed_defaults()

    def seed_defaults(self):
        self.notes = [
            NoteItem(
                id="note_1",
                title="Design System & Color Tokens",
                content="Primary palette: Cobalt Blue (#1D4ED8), Deep Navy (#1E40AF), Ice Blue (#EFF6FF), Crisp White (#FFFFFF). High contrast ratio ensuring WCAG accessibility.",
                tag="Design",
                pinned=True
            ),
            NoteItem(
                id="note_2",
                title="Tkinter Architecture Principles",
                content="Keep logic decoupled from Tkinter widgets. Use ttk.Style for unified modern theming across Windows, macOS, and Linux.",
                tag="Architecture",
                pinned=False
            )
        ]
        self.save()
