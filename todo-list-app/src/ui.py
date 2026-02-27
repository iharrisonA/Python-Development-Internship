"""
To-Do List App — Terminal UI
==============================
All display, colour, and formatting helpers.
Uses only the standard library (no external deps).
"""

import os
import sys
from typing import List
from models import Task, PRIORITY_LABELS, CATEGORIES

# ── ANSI colours ──────────────────────────────────────────────────────────────
def _supports_color():
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

USE_COLOR = _supports_color()

RESET  = '\033[0m'  if USE_COLOR else ''
BOLD   = '\033[1m'  if USE_COLOR else ''
DIM    = '\033[2m'  if USE_COLOR else ''

BLACK  = '\033[30m' if USE_COLOR else ''
RED    = '\033[91m' if USE_COLOR else ''
GREEN  = '\033[92m' if USE_COLOR else ''
YELLOW = '\033[93m' if USE_COLOR else ''
BLUE   = '\033[94m' if USE_COLOR else ''
MAGENTA= '\033[95m' if USE_COLOR else ''
CYAN   = '\033[96m' if USE_COLOR else ''
WHITE  = '\033[97m' if USE_COLOR else ''

BG_NAVY  = '\033[44m'  if USE_COLOR else ''
BG_GREEN = '\033[42m'  if USE_COLOR else ''
BG_RED   = '\033[41m'  if USE_COLOR else ''

WIDTH = 72


def clr(text, *codes):
    return ''.join(codes) + str(text) + RESET


def center(text, width=WIDTH):
    return text.center(width)


def rule(char='─', width=WIDTH, color=DIM):
    return clr(char * width, color)


# ── Priority styling ──────────────────────────────────────────────────────────
PRIORITY_COLOR = {1: CYAN, 2: YELLOW, 3: RED}
PRIORITY_ICON  = {1: '▽', 2: '◈', 3: '▲'}

def priority_badge(p: int) -> str:
    icon  = PRIORITY_ICON.get(p, '◈')
    label = PRIORITY_LABELS.get(p, 'Medium')
    color = PRIORITY_COLOR.get(p, YELLOW)
    return clr(f' {icon} {label} ', color, BOLD)


def category_badge(cat: str) -> str:
    return clr(f'[{cat}]', MAGENTA)


def status_icon(task: Task) -> str:
    if task.done:
        return clr('✔', GREEN, BOLD)
    if task.is_overdue():
        return clr('!', RED, BOLD)
    return clr('○', BLUE)


# ── Screens ───────────────────────────────────────────────────────────────────
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    print()
    print(clr('╔' + '═'*68 + '╗', BLUE, BOLD))
    print(clr('║' + center('  ✅  TO-DO LIST  —  Stay Organised, Stay Ahead', 68) + '║', BLUE, BOLD))
    print(clr('╚' + '═'*68 + '╝', BLUE, BOLD))
    print()


def print_menu():
    items = [
        ('1', 'Add Task'),
        ('2', 'View Tasks'),
        ('3', 'Complete Task'),
        ('4', 'Edit Task'),
        ('5', 'Delete Task'),
        ('6', 'Search / Filter'),
        ('7', 'Statistics'),
        ('0', 'Exit'),
    ]
    print(clr('  MENU', BOLD, CYAN))
    print(rule())
    for key, label in items:
        print(f"  {clr(key, YELLOW, BOLD)}  {label}")
    print(rule())


def print_task_row(task: Task, idx: int = None):
    prefix = f"{clr(str(idx).rjust(2), DIM)}. " if idx is not None else '   '
    done_style = DIM if task.done else ''
    title = task.title
    if task.done:
        title = clr(f'~~{title}~~', DIM)
    else:
        title = clr(title, WHITE, BOLD)

    due_str = ''
    if task.due_date:
        if task.is_overdue():
            due_str = clr(f' ⚠ Due {task.due_date}', RED)
        else:
            due_str = clr(f' 📅 {task.due_date}', DIM)

    line1 = (f"{prefix}{status_icon(task)}  {title}"
             f"  {category_badge(task.category)}{due_str}")
    line2 = (f"      {priority_badge(task.priority)}"
             f"  {clr('ID: ' + task.id, DIM)}")

    print(line1)
    print(line2)
    if task.description:
        print(f"      {clr(task.description[:60] + ('…' if len(task.description)>60 else ''), DIM)}")
    print()


def print_task_list(tasks: List[Task], title: str = 'ALL TASKS'):
    print()
    print(clr(f'  {title}', BOLD, CYAN))
    print(rule())
    if not tasks:
        print(clr('  No tasks found.', DIM))
    else:
        for i, task in enumerate(tasks, 1):
            print_task_row(task, i)
    print(rule())


def print_task_detail(task: Task):
    print()
    print(rule('─'))
    print(clr(f'  Task Detail  [{task.id}]', BOLD, CYAN))
    print(rule('─'))
    print(f"  {clr('Title      :', DIM)}  {clr(task.title, WHITE, BOLD)}")
    print(f"  {clr('Status     :', DIM)}  {'✔ Done' if task.done else '○ Pending'}")
    print(f"  {clr('Priority   :', DIM)}  {priority_badge(task.priority)}")
    print(f"  {clr('Category   :', DIM)}  {category_badge(task.category)}")
    print(f"  {clr('Due Date   :', DIM)}  {task.due_date or '—'}")
    print(f"  {clr('Description:', DIM)}  {task.description or '—'}")
    print(f"  {clr('Created    :', DIM)}  {task.created_at}")
    if task.completed_at:
        print(f"  {clr('Completed  :', DIM)}  {task.completed_at}")
    print(rule('─'))
    print()


def print_stats(tasks: List[Task]):
    total     = len(tasks)
    done      = sum(1 for t in tasks if t.done)
    pending   = total - done
    overdue   = sum(1 for t in tasks if t.is_overdue())
    by_cat    = {}
    by_pri    = {1: 0, 2: 0, 3: 0}
    for t in tasks:
        by_cat[t.category] = by_cat.get(t.category, 0) + 1
        by_pri[t.priority] += 1

    pct = int((done / total * 100)) if total else 0
    bar_filled = int(pct / 5)
    bar = clr('█' * bar_filled, GREEN) + clr('░' * (20 - bar_filled), DIM)

    print()
    print(clr('  STATISTICS', BOLD, CYAN))
    print(rule())
    print(f"  {clr('Total Tasks :', DIM)}  {clr(str(total), WHITE, BOLD)}")
    print(f"  {clr('Completed   :', DIM)}  {clr(str(done), GREEN, BOLD)}")
    print(f"  {clr('Pending     :', DIM)}  {clr(str(pending), YELLOW, BOLD)}")
    print(f"  {clr('Overdue     :', DIM)}  {clr(str(overdue), RED, BOLD)}")
    print()
    print(f"  Progress  [{bar}]  {clr(str(pct)+'%', WHITE, BOLD)}")
    print()
    print(f"  {clr('By Priority:', DIM)}")
    for p, count in by_pri.items():
        print(f"    {priority_badge(p)}  {count} task(s)")
    print()
    print(f"  {clr('By Category:', DIM)}")
    for cat, count in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f"    {category_badge(cat)}  {count} task(s)")
    print(rule())
    print()


def prompt(msg: str, default: str = '') -> str:
    suffix = f' [{default}]' if default else ''
    try:
        val = input(clr(f'  ▶ {msg}{suffix}: ', CYAN)).strip()
        return val if val else default
    except (KeyboardInterrupt, EOFError):
        return default


def confirm(msg: str) -> bool:
    val = prompt(f'{msg} (y/n)', 'n').lower()
    return val == 'y'


def success(msg: str):
    print(clr(f'\n  ✔  {msg}', GREEN, BOLD))


def error(msg: str):
    print(clr(f'\n  ✖  {msg}', RED, BOLD))


def info(msg: str):
    print(clr(f'\n  ℹ  {msg}', CYAN))


def pause():
    input(clr('\n  Press Enter to continue…', DIM))
