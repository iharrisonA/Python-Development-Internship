#!/usr/bin/env python3
"""
Calculator App — Main Application
===================================
A feature-rich command-line calculator supporting 10 operations,
chained calculations, and full session history.

Operations:
  Basic    : Addition, Subtraction, Multiplication, Division
  Advanced : Power, Modulo, Floor Division, Square Root
  Extras   : Percentage, Absolute Value

Usage:
    python src/app.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from engine import (OPERATIONS, needs_two, fmt,
                    build_expression, HistoryEntry)
from ui     import (clear, print_header, print_menu,
                    print_result_box, print_history,
                    prompt, success, error, info, pause,
                    clr, BOLD, CYAN, GREEN, YELLOW, DIM, RED, WHITE)


# ── Input helpers ─────────────────────────────────────────────────────────────

def get_number(msg: str, allow_previous: bool = False,
               previous: float = None) -> float:
    """Prompt until a valid number is entered."""
    while True:
        if allow_previous and previous is not None:
            hint = f'{msg} (or Enter to use {fmt(previous)})'
        else:
            hint = msg

        raw = prompt(hint)

        if allow_previous and raw == '' and previous is not None:
            return previous

        try:
            return float(raw)
        except ValueError:
            error(f'"{raw}" is not a valid number. Please try again.')


# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    history:  list  = []
    last_result: float = None

    while True:
        clear()
        print_header()

        # Session summary line
        if history:
            last = history[-1]
            print(clr(f'  Last result: {last.expression}', DIM))
        else:
            print(clr('  Welcome! Choose an operation to get started.', DIM))
        print()

        print_menu()
        choice = prompt('Choose operation').strip().upper()

        # ── Special commands ──────────────────────────────────────────────────
        if choice == '0':
            clear()
            print(clr('\n  Thanks for using the Calculator. Goodbye! 👋\n', CYAN, BOLD))
            sys.exit(0)

        if choice == 'H':
            clear()
            print_header()
            print_history(history)
            pause()
            continue

        if choice == 'C':
            history.clear()
            last_result = None
            success('History cleared.')
            pause()
            continue

        # ── Validate operation choice ─────────────────────────────────────────
        if choice not in OPERATIONS:
            error(f'"{choice}" is not a valid option. Choose 1–10, H, C, or 0.')
            pause()
            continue

        symbol, name, func, two_operands = OPERATIONS[choice]

        # ── Get operand(s) ────────────────────────────────────────────────────
        print()
        print(clr(f'  ── {name.upper()} ({symbol}) ──', BOLD, CYAN))
        print()

        a = get_number('Enter first number',
                       allow_previous=(last_result is not None),
                       previous=last_result)

        b = None
        if two_operands:
            b = get_number('Enter second number')

        # ── Calculate ─────────────────────────────────────────────────────────
        try:
            if two_operands:
                result = func(a, b)
            else:
                result = func(a)

            result_str  = fmt(result)
            expr_str    = (f"{fmt(a)} {symbol} {fmt(b)}"
                           if two_operands
                           else f"{symbol}({fmt(a)})")

            print_result_box(expr_str, result_str)

            # Save to history
            entry = HistoryEntry(expr_str, result)
            history.append(entry)
            last_result = result

            # Offer to chain calculation
            print(clr(f'  Use {fmt(result)} as first number in next calculation?', DIM))
            chain = prompt('Continue with this result? (y/n)', 'y').lower()
            if chain != 'y':
                last_result = None

        except (ZeroDivisionError, ValueError) as e:
            error(str(e))
            pause()


if __name__ == '__main__':
    main()
