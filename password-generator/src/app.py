#!/usr/bin/env python3
"""
Password Generator — Main Application
========================================
A feature-rich command-line password generator.

Features:
  • 5 presets: Basic, Strong, Max, PIN, Memorable, Custom
  • Specify exact password length
  • Generate a single password or a batch
  • Live strength analysis with entropy calculation
  • Check the strength of any existing password
  • Full session history

Usage:
    python src/app.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from engine import (generate_password, generate_batch, analyse_strength,
                    PRESETS, DEFAULT_LENGTHS)
from ui     import (clear, print_header, print_menu, print_presets,
                    print_password_box, print_strength_report,
                    print_history, print_batch,
                    prompt, success, error, info, pause, yn,
                    clr, BOLD, CYAN, YELLOW, DIM, WHITE, GREEN)


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_length(default: int = 16) -> int:
    while True:
        raw = prompt(f'Password length', str(default))
        try:
            n = int(raw)
            if 1 <= n <= 512:
                return n
            error('Length must be between 1 and 512.')
        except ValueError:
            error(f'"{raw}" is not a valid number.')


def get_preset_settings(preset_key: str) -> dict:
    """Return keyword args for generate_password() from a preset key."""
    _, _, upper, lower, digits, symbols, excl_ambig = PRESETS[preset_key]

    if preset_key == '6':
        # Custom — ask user which sets to include
        print()
        print(clr('  Customise your character sets:', CYAN))
        upper      = yn('  Include uppercase letters (A–Z)?', 'y')
        lower      = yn('  Include lowercase letters (a–z)?', 'y')
        digits     = yn('  Include numbers (0–9)?',           'y')
        symbols    = yn('  Include symbols (!@#$…)?',         'y')
        excl_ambig = yn('  Exclude ambiguous chars (0, O, l, I)?', 'n')

        if not any([upper, lower, digits, symbols]):
            error('You must select at least one character set. Defaulting to all.')
            upper = lower = digits = symbols = True

    return {
        'uppercase':         upper,
        'lowercase':         lower,
        'digits':            digits,
        'symbols':           symbols,
        'exclude_ambiguous': excl_ambig,
    }


def preset_label(preset_key: str, settings: dict, length: int) -> str:
    """Human-readable summary of what was used to generate."""
    name = PRESETS[preset_key][0]
    parts = []
    if settings['uppercase']:  parts.append('A–Z')
    if settings['lowercase']:  parts.append('a–z')
    if settings['digits']:     parts.append('0–9')
    if settings['symbols']:    parts.append('Symbols')
    if settings['exclude_ambiguous']: parts.append('No ambiguous')
    return f"{name}  |  {length} chars  |  {', '.join(parts)}"


# ── Actions ───────────────────────────────────────────────────────────────────

def action_generate(history: list):
    clear()
    print_header()
    print_presets()

    preset_key = prompt('Choose a preset (1–6)', '2')
    if preset_key not in PRESETS:
        error('Invalid preset. Using "Strong".')
        preset_key = '2'

    length   = get_length(DEFAULT_LENGTHS[preset_key])
    settings = get_preset_settings(preset_key)

    try:
        password = generate_password(length, **settings)
    except ValueError as e:
        error(str(e))
        pause()
        return

    strength = analyse_strength(password)
    label    = preset_label(preset_key, settings, length)

    clear()
    print_header()
    print_password_box(password, '  Your generated password:')
    print_strength_report(strength)

    history.append((password, label))
    success('Password generated and saved to session history.')

    # Regenerate option
    while yn('\n  Generate another with same settings?', 'n'):
        password = generate_password(length, **settings)
        strength = analyse_strength(password)
        print_password_box(password, '  Regenerated:')
        print_strength_report(strength)
        history.append((password, label))


def action_batch(history: list):
    clear()
    print_header()
    print_presets()

    preset_key = prompt('Choose a preset (1–6)', '2')
    if preset_key not in PRESETS:
        preset_key = '2'

    length   = get_length(DEFAULT_LENGTHS[preset_key])
    settings = get_preset_settings(preset_key)

    while True:
        raw = prompt('How many passwords to generate?', '5')
        try:
            count = int(raw)
            if 1 <= count <= 50:
                break
            error('Please enter a number between 1 and 50.')
        except ValueError:
            error('Invalid number.')

    try:
        passwords = generate_batch(count, length, **settings)
    except ValueError as e:
        error(str(e))
        pause()
        return

    clear()
    print_header()
    print_batch(passwords)

    label = preset_label(preset_key, settings, length)
    for pwd in passwords:
        history.append((pwd, label))

    success(f'{count} passwords generated and saved to session history.')


def action_check_strength():
    clear()
    print_header()
    print(clr('  CHECK PASSWORD STRENGTH', BOLD, CYAN))
    print()
    pwd = prompt('Enter a password to analyse')
    if not pwd:
        error('No password entered.')
        pause()
        return

    print_password_box(pwd, '  Analysing:')
    strength = analyse_strength(pwd)
    print_strength_report(strength)


def action_history(history: list):
    clear()
    print_header()
    print_history(history)

    if history and yn('  Clear session history?', 'n'):
        history.clear()
        success('History cleared.')


# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    history: list = []

    while True:
        clear()
        print_header()

        count = len(history)
        if count:
            print(clr(f'  {count} password(s) generated this session.\n', DIM))
        else:
            print(clr('  Generate strong, secure passwords instantly.\n', DIM))

        print_menu()
        choice = prompt('Your choice').strip()

        if choice == '1':
            action_generate(history)
            pause()
        elif choice == '2':
            action_batch(history)
            pause()
        elif choice == '3':
            action_check_strength()
            pause()
        elif choice == '4':
            action_history(history)
            pause()
        elif choice == '0':
            clear()
            print(clr('\n  Stay secure out there. Goodbye! 🔐\n', CYAN, BOLD))
            sys.exit(0)
        else:
            error('Invalid option. Please choose 0–4.')
            pause()


if __name__ == '__main__':
    main()
