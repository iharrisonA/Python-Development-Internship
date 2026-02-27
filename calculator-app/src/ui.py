"""
Calculator App — Terminal UI
==============================
Display helpers, ANSI colours, and input prompts.
"""

import os
import sys

# ── ANSI colours ──────────────────────────────────────────────────────────────
USE_COLOR = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

RESET   = '\033[0m'  if USE_COLOR else ''
BOLD    = '\033[1m'  if USE_COLOR else ''
DIM     = '\033[2m'  if USE_COLOR else ''
RED     = '\033[91m' if USE_COLOR else ''
GREEN   = '\033[92m' if USE_COLOR else ''
YELLOW  = '\033[93m' if USE_COLOR else ''
BLUE    = '\033[94m' if USE_COLOR else ''
MAGENTA = '\033[95m' if USE_COLOR else ''
CYAN    = '\033[96m' if USE_COLOR else ''
WHITE   = '\033[97m' if USE_COLOR else ''

WIDTH = 54


def clr(text, *codes):
    return ''.join(codes) + str(text) + RESET

def rule(char='─', width=WIDTH, color=DIM):
    return clr(char * width, color)

def center(text, width=WIDTH):
    visible = text
    # strip ANSI for length calculation
    import re
    visible = re.sub(r'\033\[[0-9;]*m', '', text)
    pad = max(0, width - len(visible))
    return ' ' * (pad // 2) + text

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input(clr('\n  Press Enter to continue…', DIM))

def prompt(msg: str, default: str = '') -> str:
    suffix = f' [{default}]' if default else ''
    try:
        val = input(clr(f'  ▶  {msg}{suffix}: ', CYAN)).strip()
        return val if val else default
    except (KeyboardInterrupt, EOFError):
        return default

def success(msg: str):
    print(clr(f'\n  ✔  {msg}', GREEN, BOLD))

def error(msg: str):
    print(clr(f'\n  ✖  {msg}', RED, BOLD))

def info(msg: str):
    print(clr(f'  ℹ  {msg}', CYAN))


# ── Screens ───────────────────────────────────────────────────────────────────

def print_header():
    print()
    print(clr('  ╔' + '═'*50 + '╗', BLUE, BOLD))
    print(clr('  ║', BLUE, BOLD) +
          center(clr('  🧮  PYTHON CALCULATOR', WHITE, BOLD), 50) +
          clr('║', BLUE, BOLD))
    print(clr('  ╚' + '═'*50 + '╝', BLUE, BOLD))
    print()


def print_menu():
    from engine import OPERATIONS
    print(clr('  OPERATIONS', BOLD, CYAN))
    print(f'  {rule()}')

    # Two-column layout
    keys = list(OPERATIONS.keys())
    half = (len(keys) + 1) // 2
    left  = keys[:half]
    right = keys[half:]

    for i in range(half):
        lk = left[i]
        sym_l, name_l, _, two_l = OPERATIONS[lk]
        tag_l = '' if two_l else clr(' (1 num)', DIM)
        left_str = f"  {clr(lk.rjust(2), YELLOW, BOLD)}  {clr(sym_l, MAGENTA)}  {name_l}{tag_l}"

        if i < len(right):
            rk = right[i]
            sym_r, name_r, _, two_r = OPERATIONS[rk]
            tag_r = '' if two_r else clr(' (1 num)', DIM)
            right_str = f"{clr(rk.rjust(2), YELLOW, BOLD)}  {clr(sym_r, MAGENTA)}  {name_r}{tag_r}"
            print(f"{left_str:<42}  {right_str}")
        else:
            print(left_str)

    print(f'  {rule()}')
    print(f"  {clr('H', YELLOW, BOLD)}  History    "
          f"  {clr('C', YELLOW, BOLD)}  Clear History    "
          f"  {clr('0', YELLOW, BOLD)}  Exit")
    print(f'  {rule()}')


def print_result_box(expression: str, result: str):
    print()
    print(clr('  ┌' + '─'*50 + '┐', GREEN))
    print(clr('  │', GREEN) +
          f"  {clr('Result', DIM)}".ljust(10) +
          clr('│', GREEN))
    print(clr('  │', GREEN) +
          f"  {clr(expression, WHITE)}".ljust(10) +
          clr('│', GREEN))
    print(clr('  │', GREEN) +
          f"  {clr('= ' + result, GREEN, BOLD)}".ljust(10) +
          clr('│', GREEN))
    print(clr('  └' + '─'*50 + '┘', GREEN))
    print()


def print_history(history: list):
    print()
    print(clr('  CALCULATION HISTORY', BOLD, CYAN))
    print(f'  {rule()}')
    if not history:
        print(clr('  No history yet.', DIM))
    else:
        for i, entry in enumerate(reversed(history), 1):
            print(f"  {clr(str(i).rjust(2), DIM)}.  {clr(entry.expression, WHITE)}")
            print(f"       {clr(entry.timestamp, DIM)}")
            print()
    print(f'  {rule()}')
