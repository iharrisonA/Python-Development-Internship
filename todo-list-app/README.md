# ✅ To-Do List App

A feature-rich command-line To-Do List application built with Python. Manage your tasks efficiently with priorities, categories, due dates, search, filters, and a live statistics dashboard — all from your terminal.

> **Zero external dependencies** — uses Python standard library only.

---

## 📁 Project Structure

```
todo-list-app/
│
├── src/
│   ├── app.py          # Main application & all user interactions
│   ├── models.py       # Task dataclass & JSON storage engine
│   └── ui.py           # Terminal UI, colour helpers & display functions
│
├── data/
│   └── tasks.json      # Persistent task storage (auto-created on first run)
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

```bash
# 1. Clone the repository
git clone https://github.com/your-username/todo-list-app.git
cd todo-list-app

# 2. No installation needed — just run it!
python src/app.py
```

> Requires **Python 3.7+**. No pip install needed.

---

## 🚀 Features

| Feature | Description |
|---|---|
| ➕ Add Task | Title, description, priority, category & due date |
| 👁 View Tasks | Sort by priority, due date, date added, or status |
| ✔ Complete | Toggle tasks complete / incomplete |
| ✏️ Edit Task | Update any field of an existing task |
| 🗑 Delete Task | Remove tasks with confirmation prompt |
| 🔍 Search | Find tasks by keyword across title, description & category |
| 🔎 Filter | Filter by category, priority, status, or overdue |
| 📊 Statistics | Progress bar, counts by priority & category |
| 💾 Persistent | All tasks saved to `data/tasks.json` automatically |

---

## 🎯 Priorities

| Symbol | Level | Use For |
|---|---|---|
| ▽ | Low | Nice to do |
| ◈ | Medium | Should do |
| ▲ | High | Must do |

---

## 📂 Categories

`General` · `Work` · `Personal` · `Shopping` · `Health` · `Study` · `Other`

---

## 🖥 Screenshots

```
╔════════════════════════════════════════════════════════════════════╗
║             ✅  TO-DO LIST  —  Stay Organised, Stay Ahead           ║
╚════════════════════════════════════════════════════════════════════╝

  Tasks: 4 total  |  3 pending  |  1 overdue

  MENU
──────────────────────────────────────────────────────────────────────
  1  Add Task          5  Delete Task
  2  View Tasks        6  Search / Filter
  3  Complete Task     7  Statistics
  4  Edit Task         0  Exit
──────────────────────────────────────────────────────────────────────
```

---

## 🛠 Tech Stack

- **Python 3.7+** — standard library only
- `dataclasses` — Task model
- `json` — persistent file storage
- `uuid` — unique task IDs
- ANSI escape codes — coloured terminal output

---

## 💡 How It Works

1. Tasks are stored as JSON objects in `data/tasks.json`
2. Each task has a unique 8-character ID for fast lookup
3. Partial ID matching — type just the first few characters to find a task
4. Due dates are automatically compared to today to flag overdue tasks
5. All changes are saved instantly after every action

---

## 👤 Author

Built as part of a Python Development Internship project.
