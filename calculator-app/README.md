# 🧮 Python Calculator

A feature-rich command-line calculator built with Python. Supports 10 arithmetic operations, chained calculations, and a full session history — all from your terminal.

> **Zero external dependencies** — uses Python standard library only.

---

## 📁 Project Structure

```
calculator-app/
│
├── src/
│   ├── app.py        # Main application & user interaction loop
│   ├── engine.py     # All arithmetic operations & history model
│   └── ui.py         # Terminal UI, colour helpers & display functions
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

```bash
# 1. Clone the repository
git clone https://github.com/your-username/calculator-app.git
cd calculator-app

# 2. No installation needed — just run it!
python src/app.py
```

> Requires **Python 3.7+**. No pip install needed.

---

## 🚀 Features

| Feature | Description |
|---|---|
| ➕ 10 Operations | Basic and advanced arithmetic |
| 🔗 Chained Calculations | Use the previous result as input for the next |
| 📜 Session History | View all calculations from the current session |
| 🧹 Clear History | Reset the session history at any time |
| ⚠️ Error Handling | Graceful messages for division by zero, invalid input, negative square roots |
| 🎨 Coloured Output | Clean, readable terminal interface with ANSI colours |

---

## 🔢 Operations

| # | Symbol | Operation | Inputs |
|---|---|---|---|
| 1 | `+` | Addition | Two numbers |
| 2 | `-` | Subtraction | Two numbers |
| 3 | `×` | Multiplication | Two numbers |
| 4 | `÷` | Division | Two numbers |
| 5 | `^` | Power / Exponent | Two numbers |
| 6 | `%` | Modulo (remainder) | Two numbers |
| 7 | `//` | Floor Division | Two numbers |
| 8 | `√` | Square Root | One number |
| 9 | `%of` | Percentage (a% of b) | Two numbers |
| 10 | `\|x\|` | Absolute Value | One number |

---

## 🖥 Preview

```
  ╔══════════════════════════════════════════════════╗
  ║              🧮  PYTHON CALCULATOR               ║
  ╚══════════════════════════════════════════════════╝

  OPERATIONS
  ──────────────────────────────────────────────────
   1  +  Addition               6  %   Modulo
   2  -  Subtraction            7  //  Floor Division
   3  ×  Multiplication         8  √   Square Root
   4  ÷  Division               9  %of Percentage
   5  ^  Power                 10  |x| Absolute Value
  ──────────────────────────────────────────────────
  H  History    C  Clear History    0  Exit
  ──────────────────────────────────────────────────

  ┌──────────────────────────────────────────────────┐
  │  Result                                          │
  │  22 × 7                                          │
  │  = 154                                           │
  └──────────────────────────────────────────────────┘
```

---

## 🛠 Tech Stack

- **Python 3.7+** — standard library only
- `math` — square root and numeric utilities
- `datetime` — timestamped history entries
- ANSI escape codes — coloured terminal output

---

## 💡 How It Works

1. User selects an operation by number (1–10)
2. Enters one or two numbers depending on the operation
3. Result is displayed in a styled result box
4. User can chain the result into the next calculation
5. Full session history is accessible at any time with `H`

---

## 👤 Author

Built as part of a Python Development Internship project.
