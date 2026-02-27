"""
To-Do List App — Task Model & Storage
======================================
Defines the Task dataclass and handles all JSON persistence.
"""

import json
import os
import uuid
from dataclasses import dataclass, field, asdict
from datetime    import datetime
from typing      import List, Optional

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'tasks.json')

PRIORITIES = {'low': 1, 'medium': 2, 'high': 3}
PRIORITY_LABELS = {1: 'Low', 2: 'Medium', 3: 'High'}

CATEGORIES = ['General', 'Work', 'Personal', 'Shopping', 'Health', 'Study', 'Other']


@dataclass
class Task:
    title:      str
    id:         str             = field(default_factory=lambda: str(uuid.uuid4())[:8])
    description: str            = ''
    priority:   int             = 2          # 1=Low 2=Medium 3=High
    category:   str             = 'General'
    due_date:   Optional[str]   = None       # 'YYYY-MM-DD'
    done:       bool            = False
    created_at: str             = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M'))
    completed_at: Optional[str] = None

    def complete(self):
        self.done         = True
        self.completed_at = datetime.now().strftime('%Y-%m-%d %H:%M')

    def uncomplete(self):
        self.done         = False
        self.completed_at = None

    def is_overdue(self) -> bool:
        if self.due_date and not self.done:
            return datetime.strptime(self.due_date, '%Y-%m-%d').date() < datetime.today().date()
        return False

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> 'Task':
        return Task(**d)


# ── Storage ───────────────────────────────────────────────────────────────────

def _ensure_data_dir():
    os.makedirs(os.path.dirname(os.path.abspath(DATA_FILE)), exist_ok=True)


def load_tasks() -> List[Task]:
    _ensure_data_dir()
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return [Task.from_dict(d) for d in json.load(f)]
    except (json.JSONDecodeError, KeyError):
        return []


def save_tasks(tasks: List[Task]):
    _ensure_data_dir()
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([t.to_dict() for t in tasks], f, indent=2, ensure_ascii=False)


def find_task(tasks: List[Task], task_id: str) -> Optional[Task]:
    """Find by full or partial ID (case-insensitive)."""
    task_id = task_id.lower()
    for t in tasks:
        if t.id.lower().startswith(task_id):
            return t
    return None
