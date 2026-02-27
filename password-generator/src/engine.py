"""
Password Generator — Core Engine
==================================
All password generation logic, strength analysis, and character sets.
"""

import random
import string
import secrets
import math
from typing import List, Dict


# ── Character sets ────────────────────────────────────────────────────────────

CHAR_SETS = {
    'uppercase': string.ascii_uppercase,          # A-Z
    'lowercase': string.ascii_lowercase,          # a-z
    'digits':    string.digits,                   # 0-9
    'symbols':   '!@#$%^&*()_+-=[]{}|;:,.<>?',  # special chars
    'ambiguous': 'lI1O0',                         # visually similar chars
}

# Presets: (name, description, uppercase, lowercase, digits, symbols, exclude_ambiguous)
PRESETS = {
    '1': ('Basic',      'Letters & numbers only',         True,  True,  True,  False, False),
    '2': ('Strong',     'Letters, numbers & symbols',     True,  True,  True,  True,  False),
    '3': ('Max',        'All chars, max complexity',      True,  True,  True,  True,  False),
    '4': ('PIN',        'Numbers only',                   False, False, True,  False, False),
    '5': ('Memorable',  'No ambiguous characters',        True,  True,  True,  True,  True),
    '6': ('Custom',     'You choose which sets to use',   False, False, False, False, False),
}

DEFAULT_LENGTHS = {
    '1': 12,
    '2': 16,
    '3': 20,
    '4': 6,
    '5': 16,
    '6': 16,
}


# ── Generator ─────────────────────────────────────────────────────────────────

def build_charset(uppercase: bool, lowercase: bool,
                  digits: bool, symbols: bool,
                  exclude_ambiguous: bool = False) -> str:
    """Assemble the character pool from chosen sets."""
    pool = ''
    if uppercase: pool += CHAR_SETS['uppercase']
    if lowercase: pool += CHAR_SETS['lowercase']
    if digits:    pool += CHAR_SETS['digits']
    if symbols:   pool += CHAR_SETS['symbols']

    if exclude_ambiguous:
        pool = ''.join(c for c in pool if c not in CHAR_SETS['ambiguous'])

    return pool


def generate_password(length: int,
                      uppercase: bool = True,
                      lowercase: bool = True,
                      digits: bool    = True,
                      symbols: bool   = True,
                      exclude_ambiguous: bool = False) -> str:
    """
    Generate a cryptographically secure random password.

    Guarantees at least one character from each enabled set,
    then fills remaining positions randomly.
    Uses secrets module for cryptographic randomness.
    """
    pool = build_charset(uppercase, lowercase, digits, symbols, exclude_ambiguous)

    if not pool:
        raise ValueError("At least one character set must be selected.")

    # Guarantee minimum one char from each selected set
    required = []
    if uppercase:
        src = CHAR_SETS['uppercase']
        if exclude_ambiguous:
            src = ''.join(c for c in src if c not in CHAR_SETS['ambiguous'])
        if src:
            required.append(secrets.choice(src))

    if lowercase:
        src = CHAR_SETS['lowercase']
        if exclude_ambiguous:
            src = ''.join(c for c in src if c not in CHAR_SETS['ambiguous'])
        if src:
            required.append(secrets.choice(src))

    if digits:
        src = CHAR_SETS['digits']
        if exclude_ambiguous:
            src = ''.join(c for c in src if c not in CHAR_SETS['ambiguous'])
        if src:
            required.append(secrets.choice(src))

    if symbols:
        required.append(secrets.choice(CHAR_SETS['symbols']))

    # Fill remaining
    remaining = length - len(required)
    if remaining < 0:
        # length too short — just fill with pool chars
        password_list = [secrets.choice(pool) for _ in range(length)]
    else:
        password_list = required + [secrets.choice(pool) for _ in range(remaining)]

    # Shuffle so required chars aren't always at start
    random.SystemRandom().shuffle(password_list)
    return ''.join(password_list)


def generate_batch(count: int, length: int, **kwargs) -> List[str]:
    """Generate multiple passwords at once."""
    return [generate_password(length, **kwargs) for _ in range(count)]


# ── Strength analysis ─────────────────────────────────────────────────────────

def analyse_strength(password: str) -> Dict:
    """
    Return a dict with strength score (0–100), label, and feedback.
    """
    length   = len(password)
    has_upper  = any(c.isupper() for c in password)
    has_lower  = any(c.islower() for c in password)
    has_digit  = any(c.isdigit() for c in password)
    has_symbol = any(c in CHAR_SETS['symbols'] for c in password)

    # Pool size for entropy calculation
    pool = 0
    if has_upper:  pool += 26
    if has_lower:  pool += 26
    if has_digit:  pool += 10
    if has_symbol: pool += len(CHAR_SETS['symbols'])

    entropy = length * math.log2(pool) if pool > 0 else 0

    # Score
    score = 0
    score += min(40, int(entropy / 3))   # entropy up to 40 pts
    score += 10 if has_upper  else 0
    score += 10 if has_lower  else 0
    score += 10 if has_digit  else 0
    score += 15 if has_symbol else 0
    score += 15 if length >= 16 else (10 if length >= 12 else 5 if length >= 8 else 0)
    score  = min(100, score)

    if score >= 80:
        label, color_key = 'Very Strong', 'green'
    elif score >= 60:
        label, color_key = 'Strong',      'cyan'
    elif score >= 40:
        label, color_key = 'Moderate',    'yellow'
    elif score >= 20:
        label, color_key = 'Weak',        'red'
    else:
        label, color_key = 'Very Weak',   'red'

    feedback = []
    if length < 12:
        feedback.append('Use at least 12 characters for better security.')
    if not has_upper:
        feedback.append('Add uppercase letters (A–Z).')
    if not has_lower:
        feedback.append('Add lowercase letters (a–z).')
    if not has_digit:
        feedback.append('Add numbers (0–9).')
    if not has_symbol:
        feedback.append('Add symbols (!@#$…) for maximum strength.')

    return {
        'score':     score,
        'label':     label,
        'color_key': color_key,
        'entropy':   round(entropy, 1),
        'length':    length,
        'has_upper': has_upper,
        'has_lower': has_lower,
        'has_digit': has_digit,
        'has_symbol':has_symbol,
        'feedback':  feedback,
    }
