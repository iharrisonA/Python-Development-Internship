#!/usr/bin/env python3
"""
To-Do List App — Main Application
===================================
A feature-rich command-line To-Do List application.

Features:
  • Add tasks with title, description, priority, category & due date
  • View all tasks (sorted by priority / due date)
  • Mark tasks as complete / incomplete
  • Edit any field of a task
  • Delete tasks (with confirmation)
  • Search by keyword | Filter by category, priority, or status
  • Statistics dashboard with progress bar
  • Persistent JSON storage

Usage:
    python src/app.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime
from typing   import List

from models import (Task, load_tasks, save_tasks, find_task,
                    PRIORITIES, PRIORITY_LABELS, CATEGORIES)
from ui     import (clear, print_header, print_menu, print_task_list,
                    print_task_detail, print_stats,
                    prompt, confirm, success, error, info, pause,
                    clr, BOLD, CYAN, YELLOW, DIM, rule)


# ── Helpers ───────────────────────────────────────────────────────────────────

def pick_priority() -> int:
    print(clr('\n  Priority:', CYAN))
    for k, label in PRIORITY_LABELS.items():
        print(f"    {clr(str(k), YELLOW, BOLD)}  {label}")
    val = prompt('Choose priority (1/2/3)', '2')
    return int(val) if val in ('1', '2', '3') else 2


def pick_category() -> str:
    print(clr('\n  Category:', CYAN))
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"    {clr(str(i), YELLOW, BOLD)}  {cat}")
    val = prompt(f'Choose category (1–{len(CATEGORIES)})', '1')
    try:
        idx = int(val) - 1
        return CATEGORIES[idx] if 0 <= idx < len(CATEGORIES) else 'General'
    except ValueError:
        return 'General'


def pick_date() -> str:
    while True:
        val = prompt('Due date (YYYY-MM-DD) or leave blank', '')
        if not val:
            return None
        try:
            datetime.strptime(val, '%Y-%m-%d')
            return val
        except ValueError:
            error('Invalid date format. Use YYYY-MM-DD.')


def get_task_by_input(tasks: List[Task], action: str = 'select') -> Task:
    id_input = prompt(f'Enter task ID to {action}')
    if not id_input:
        return None
    task = find_task(tasks, id_input)
    if not task:
        error(f'No task found with ID starting with "{id_input}".')
    return task


# ── Actions ───────────────────────────────────────────────────────────────────

def action_add(tasks: List[Task]):
    print(clr('\n  ── ADD NEW TASK ──', BOLD, CYAN))
    title = prompt('Task title')
    if not title:
        error('Title cannot be empty.')
        return
    desc     = prompt('Description (optional)', '')
    priority = pick_priority()
    category = pick_category()
    due_date = pick_date()

    task = Task(
        title       = title,
        description = desc,
        priority    = priority,
        category    = category,
        due_date    = due_date,
    )
    tasks.append(task)
    save_tasks(tasks)
    success(f'Task "{title}" added!  [ID: {task.id}]')


def action_view(tasks: List[Task]):
    print(clr('\n  Sort by:', CYAN))
    print(f"    {clr('1', YELLOW, BOLD)}  Priority (High → Low)")
    print(f"    {clr('2', YELLOW, BOLD)}  Due Date")
    print(f"    {clr('3', YELLOW, BOLD)}  Date Added")
    print(f"    {clr('4', YELLOW, BOLD)}  Status (Pending first)")
    sort = prompt('Choose sort (1–4)', '1')

    if sort == '2':
        sorted_tasks = sorted(tasks, key=lambda t: (t.due_date or '9999', t.priority * -1))
    elif sort == '3':
        sorted_tasks = sorted(tasks, key=lambda t: t.created_at)
    elif sort == '4':
        sorted_tasks = sorted(tasks, key=lambda t: (t.done, t.priority * -1))
    else:
        sorted_tasks = sorted(tasks, key=lambda t: (t.done, -t.priority))

    print_task_list(sorted_tasks)

    # Option to view detail
    detail = prompt('Enter task ID for details (or Enter to skip)', '')
    if detail:
        task = find_task(tasks, detail)
        if task:
            print_task_detail(task)
        else:
            error('Task not found.')


def action_complete(tasks: List[Task]):
    print(clr('\n  ── COMPLETE / UNCOMPLETE TASK ──', BOLD, CYAN))
    pending = [t for t in tasks if not t.done]
    done    = [t for t in tasks if t.done]
    print_task_list(pending, 'PENDING TASKS')
    if done:
        info(f'{len(done)} completed task(s) hidden. Filter to view them.')

    task = get_task_by_input(tasks, 'toggle')
    if not task:
        return

    if task.done:
        if confirm(f'Mark "{task.title}" as incomplete?'):
            task.uncomplete()
            save_tasks(tasks)
            success(f'"{task.title}" marked as incomplete.')
    else:
        task.complete()
        save_tasks(tasks)
        success(f'"{task.title}" marked as complete! 🎉')


def action_edit(tasks: List[Task]):
    print(clr('\n  ── EDIT TASK ──', BOLD, CYAN))
    print_task_list(tasks)
    task = get_task_by_input(tasks, 'edit')
    if not task:
        return

    print_task_detail(task)
    print(clr('  Leave blank to keep current value.\n', DIM))

    new_title = prompt(f'Title', task.title)
    if new_title:
        task.title = new_title

    new_desc = prompt(f'Description', task.description)
    task.description = new_desc

    print(f'\n  Current priority: {PRIORITY_LABELS[task.priority]}')
    if confirm('Change priority?'):
        task.priority = pick_priority()

    print(f'\n  Current category: {task.category}')
    if confirm('Change category?'):
        task.category = pick_category()

    print(f'\n  Current due date: {task.due_date or "None"}')
    if confirm('Change due date?'):
        task.due_date = pick_date()

    save_tasks(tasks)
    success(f'Task "{task.title}" updated!')


def action_delete(tasks: List[Task]):
    print(clr('\n  ── DELETE TASK ──', BOLD, CYAN))
    print_task_list(tasks)
    task = get_task_by_input(tasks, 'delete')
    if not task:
        return

    print_task_detail(task)
    if confirm(f'Permanently delete "{task.title}"?'):
        tasks.remove(task)
        save_tasks(tasks)
        success(f'Task deleted.')
    else:
        info('Deletion cancelled.')


def action_search(tasks: List[Task]):
    print(clr('\n  ── SEARCH & FILTER ──', BOLD, CYAN))
    print(f"    {clr('1', YELLOW, BOLD)}  Search by keyword")
    print(f"    {clr('2', YELLOW, BOLD)}  Filter by category")
    print(f"    {clr('3', YELLOW, BOLD)}  Filter by priority")
    print(f"    {clr('4', YELLOW, BOLD)}  Show only pending")
    print(f"    {clr('5', YELLOW, BOLD)}  Show only completed")
    print(f"    {clr('6', YELLOW, BOLD)}  Show overdue tasks")
    choice = prompt('Choose filter (1–6)', '1')

    if choice == '1':
        kw = prompt('Search keyword').lower()
        results = [t for t in tasks
                   if kw in t.title.lower() or kw in t.description.lower()
                   or kw in t.category.lower()]
        print_task_list(results, f'RESULTS FOR "{kw.upper()}"')

    elif choice == '2':
        print(clr('\n  Categories:', CYAN))
        for i, cat in enumerate(CATEGORIES, 1):
            print(f"    {clr(str(i), YELLOW, BOLD)}  {cat}")
        val = prompt(f'Choose category (1–{len(CATEGORIES)})', '1')
        try:
            cat = CATEGORIES[int(val) - 1]
        except (ValueError, IndexError):
            cat = 'General'
        results = [t for t in tasks if t.category == cat]
        print_task_list(results, f'CATEGORY: {cat.upper()}')

    elif choice == '3':
        priority = pick_priority()
        results  = [t for t in tasks if t.priority == priority]
        print_task_list(results, f'PRIORITY: {PRIORITY_LABELS[priority].upper()}')

    elif choice == '4':
        results = [t for t in tasks if not t.done]
        print_task_list(results, 'PENDING TASKS')

    elif choice == '5':
        results = [t for t in tasks if t.done]
        print_task_list(results, 'COMPLETED TASKS')

    elif choice == '6':
        results = [t for t in tasks if t.is_overdue()]
        print_task_list(results, 'OVERDUE TASKS')

    else:
        error('Invalid option.')


def action_stats(tasks: List[Task]):
    print_stats(tasks)


# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    tasks = load_tasks()

    while True:
        clear()
        print_header()

        # Quick summary line
        pending = sum(1 for t in tasks if not t.done)
        overdue = sum(1 for t in tasks if t.is_overdue())
        print(clr(f'  Tasks: {len(tasks)} total  |  '
                  f'{pending} pending  |  '
                  f'{overdue} overdue\n', DIM))

        print_menu()
        choice = prompt('Your choice')

        if choice == '1':
            action_add(tasks)
            pause()
        elif choice == '2':
            action_view(tasks)
            pause()
        elif choice == '3':
            action_complete(tasks)
            pause()
        elif choice == '4':
            action_edit(tasks)
            pause()
        elif choice == '5':
            action_delete(tasks)
            pause()
        elif choice == '6':
            action_search(tasks)
            pause()
        elif choice == '7':
            action_stats(tasks)
            pause()
        elif choice == '0':
            clear()
            print(clr('\n  Goodbye! Stay productive. 👋\n', CYAN, BOLD))
            sys.exit(0)
        else:
            error('Invalid option. Please choose 0–7.')
            pause()


if __name__ == '__main__':
    main()
