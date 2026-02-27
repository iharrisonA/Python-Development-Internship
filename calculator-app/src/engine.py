"""
Calculator App — Core Engine
==============================
All arithmetic operations and calculation history logic.
"""

import math
from datetime import datetime
from typing   import List, Tuple, Optional


# ── Operations ────────────────────────────────────────────────────────────────

def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b

def power(a: float, b: float) -> float:
    return a ** b

def modulo(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot modulo by zero.")
    return a % b

def floor_divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a // b

def square_root(a: float, _: float = None) -> float:
    if a < 0:
        raise ValueError("Cannot take square root of a negative number.")
    return math.sqrt(a)

def percentage(a: float, b: float) -> float:
    """a% of b"""
    return (a / 100) * b

def absolute(a: float, _: float = None) -> float:
    return abs(a)


# ── Operation registry ────────────────────────────────────────────────────────

OPERATIONS = {
    '1':  ('+',   'Addition',         add,          True),
    '2':  ('-',   'Subtraction',      subtract,     True),
    '3':  ('×',   'Multiplication',   multiply,     True),
    '4':  ('÷',   'Division',         divide,       True),
    '5':  ('^',   'Power',            power,        True),
    '6':  ('%',   'Modulo',           modulo,       True),
    '7':  ('//',  'Floor Division',   floor_divide, True),
    '8':  ('√',   'Square Root',      square_root,  False),  # single operand
    '9':  ('%of', 'Percentage (a% of b)', percentage, True),
    '10': ('|x|', 'Absolute Value',   absolute,     False),  # single operand
}

# needs_two_operands flag
def needs_two(key: str) -> bool:
    return OPERATIONS[key][3]


# ── History ───────────────────────────────────────────────────────────────────

class HistoryEntry:
    def __init__(self, expression: str, result: float, timestamp: str = None):
        self.expression = expression
        self.result     = result
        self.timestamp  = timestamp or datetime.now().strftime('%H:%M:%S')

    def __str__(self):
        return f"[{self.timestamp}]  {self.expression} = {fmt(self.result)}"


def fmt(value: float) -> str:
    """Format a float cleanly — no trailing zeros for whole numbers."""
    if value == int(value) and not math.isinf(value):
        return str(int(value))
    return f"{value:.10g}"


def build_expression(a: float, symbol: str, b: Optional[float], result: float) -> str:
    if b is None:
        return f"{symbol}({fmt(a)}) = {fmt(result)}"
    return f"{fmt(a)} {symbol} {fmt(b)} = {fmt(result)}"
