"""
Password Generator — Terminal UI
===================================
Display helpers, ANSI colours, and input prompts.
"""

import os
import sys
import re

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

COLOR_MAP = {
    'green':  GREEN,
    'cyan':   CYAN,
    'yellow': YELLOW,
    'red':    RED,
    'white':  WHITE,
}

WIDTH = 58


def clr(text, *codes):
    return ''.join(codes) + str(text) + RESET

def strip_ansi(text):
    return re.sub(r'\033\[[0-9;]*m', '', text)

def rule(char='─', width=WIDTH, color=DIM):
    return clr(char * width, color)

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

def yn(msg: str, default='y') -> bool:
    return prompt(msg + ' (y/n)', default).lower() == 'y'


# ── Screens ───────────────────────────────────────────────────────────────────

def print_header():
    print()
    print(clr('  ╔' + '═'*54 + '╗', BLUE, BOLD))
    title = '  🔐  PASSWORD GENERATOR'
    pad   = 54 - len(title)
    print(clr('  ║', BLUE, BOLD) +
          clr(title + ' ' * pad, WHITE, BOLD) +
          clr('║', BLUE, BOLD))
    print(clr('  ╚' + '═'*54 + '╝', BLUE, BOLD))
    print()


def print_menu():
    print(clr('  MAIN MENU', BOLD, CYAN))
    print(f'  {rule()}')
    options = [
        ('1', 'Generate Password'),
        ('2', 'Generate Multiple Passwords'),
        ('3', 'Check Password Strength'),
        ('4', 'View Session History'),
        ('0', 'Exit'),
    ]
    for key, label in options:
        print(f"  {clr(key, YELLOW, BOLD)}  {label}")
    print(f'  {rule()}')


def print_presets():
    from engine import PRESETS, DEFAULT_LENGTHS
    print()
    print(clr('  PRESETS', BOLD, CYAN))
    print(f'  {rule()}')
    for key, (name, desc, *_) in PRESETS.items():
        default_len = DEFAULT_LENGTHS[key]
        print(f"  {clr(key, YELLOW, BOLD)}  {clr(name, WHITE, BOLD):<22}  "
              f"{clr(desc, DIM)}  {clr(f'(default: {default_len} chars)', DIM)}")
    print(f'  {rule()}')


def print_password_box(password: str, label: str = ''):
    width = max(len(password) + 6, 40)
    border_top    = '  ┌' + '─' * (width - 4) + '┐'
    border_bottom = '  └' + '─' * (width - 4) + '┘'
    inner_pad     = width - 4 - len(password)
    print()
    if label:
        print(clr(f'  {label}', DIM))
    print(clr(border_top, GREEN))
    print(clr('  │', GREEN) +
          '  ' + clr(password, WHITE, BOLD) + ' ' * inner_pad +
          clr('│', GREEN))
    print(clr(border_bottom, GREEN))
    print()


def print_strength_bar(score: int, label: str, color_key: str):
    color      = COLOR_MAP.get(color_key, WHITE)
    filled     = int(score / 5)
    empty      = 20 - filled
    bar        = clr('█' * filled, color, BOLD) + clr('░' * empty, DIM)
    score_str  = clr(f'{score}/100', color, BOLD)
    label_str  = clr(label, color, BOLD)
    print(f'  [{bar}]  {score_str}  {label_str}')


def print_strength_report(info_dict: dict):
    from engine import CHAR_SETS
    score     = info_dict['score']
    label     = info_dict['label']
    color_key = info_dict['color_key']
    color     = COLOR_MAP.get(color_key, WHITE)

    print()
    print(clr('  STRENGTH ANALYSIS', BOLD, CYAN))
    print(f'  {rule()}')

    print_strength_bar(score, label, color_key)
    print()

    checks = [
        ('Uppercase letters', info_dict['has_upper']),
        ('Lowercase letters', info_dict['has_lower']),
        ('Numbers',           info_dict['has_digit']),
        ('Symbols',           info_dict['has_symbol']),
        ('Length ≥ 12',       info_dict['length'] >= 12),
        ('Length ≥ 16',       info_dict['length'] >= 16),
    ]
    for check_label, passed in checks:
        icon  = clr('✔', GREEN) if passed else clr('✖', RED)
        print(f"  {icon}  {check_label}")

    print()
    print(f"  {clr('Length  :', DIM)}  {clr(str(info_dict['length']), WHITE, BOLD)} characters")
    print(f"  {clr('Entropy :', DIM)}  {clr(str(info_dict['entropy']), WHITE, BOLD)} bits")

    if info_dict['feedback']:
        print()
        print(clr('  Suggestions:', YELLOW))
        for tip in info_dict['feedback']:
            print(f"  {clr('→', YELLOW)}  {tip}")

    print(f'  {rule()}')
    print()


def print_history(history: list):
    print()
    print(clr('  SESSION HISTORY', BOLD, CYAN))
    print(f'  {rule()}')
    if not history:
        print(clr('  No passwords generated yet.', DIM))
    else:
        for i, (pwd, label) in enumerate(reversed(history), 1):
            print(f"  {clr(str(i).rjust(2), DIM)}.  {clr(pwd, WHITE, BOLD)}")
            print(f"       {clr(label, DIM)}")
            print()
    print(f'  {rule()}')
    print()


def print_batch(passwords: list):
    print()
    print(clr('  GENERATED PASSWORDS', BOLD, CYAN))
    print(f'  {rule()}')
    for i, pwd in enumerate(passwords, 1):
        print(f"  {clr(str(i).rjust(2), DIM)}.  {clr(pwd, WHITE, BOLD)}")
    print(f'  {rule()}')
    print()
