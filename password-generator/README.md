# 🔐 Password Generator

A feature-rich command-line password generator built with Python. Generate strong, cryptographically secure passwords with full control over length, character sets, and complexity — all from your terminal.

> **Zero external dependencies** — uses Python standard library only.

---

## 📁 Project Structure

```
password-generator/
│
├── src/
│   ├── app.py        # Main application & user interaction loop
│   ├── engine.py     # Password generation, strength analysis & character sets
│   └── ui.py         # Terminal UI, colour helpers & display functions
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

```bash
# 1. Clone the repository
git clone https://github.com/your-username/password-generator.git
cd password-generator

# 2. No installation needed — just run it!
python src/app.py
```

> Requires **Python 3.7+**. No pip install needed.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🎛 6 Presets | Basic, Strong, Max, PIN, Memorable, Custom |
| 📏 Custom Length | Choose any length from 1 to 512 characters |
| 🔢 Batch Generate | Generate up to 50 passwords at once |
| 📊 Strength Analyser | Score, entropy (bits), checklist & suggestions |
| 🔍 Check Any Password | Analyse the strength of an existing password |
| 📜 Session History | View all passwords generated during the session |
| 🔒 Cryptographically Secure | Uses Python's `secrets` module |

---

## 🎛 Presets

| # | Preset | Character Sets | Default Length |
|---|---|---|---|
| 1 | Basic | A–Z, a–z, 0–9 | 12 |
| 2 | Strong | A–Z, a–z, 0–9, Symbols | 16 |
| 3 | Max | All characters | 20 |
| 4 | PIN | Numbers only | 6 |
| 5 | Memorable | All, no ambiguous chars (0, O, l, I) | 16 |
| 6 | Custom | You choose | 16 |

---

## 📊 Strength Analysis

Every generated password is automatically analysed across:

- ✔ Presence of uppercase, lowercase, digits, and symbols
- ✔ Password length (≥12 and ≥16 thresholds)
- ✔ Entropy in bits (calculated from character pool size × length)
- ✔ Overall score out of 100 with label: Very Weak → Very Strong

---

## 🖥 Preview

```
  ╔══════════════════════════════════════════════════════╗
  ║  🔐  PASSWORD GENERATOR                             ║
  ╚══════════════════════════════════════════════════════╝

  MAIN MENU
  ──────────────────────────────────────────────────────
  1  Generate Password
  2  Generate Multiple Passwords
  3  Check Password Strength
  4  View Session History
  0  Exit
  ──────────────────────────────────────────────────────

  ┌──────────────────────────────────────┐
  │  VbSui=6IuNFCIch!Bp}j               │
  └──────────────────────────────────────┘

  STRENGTH ANALYSIS
  ──────────────────────────────────────────────────────
  [████████████████████]  100/100  Very Strong

  ✔  Uppercase letters       ✔  Length ≥ 12
  ✔  Lowercase letters       ✔  Length ≥ 16
  ✔  Numbers                 Entropy: 129.2 bits
  ✔  Symbols
```

---

## 🛠 Tech Stack

- **Python 3.7+** — standard library only
- `secrets` — cryptographically secure random generation
- `random.SystemRandom` — secure shuffle
- `math` — entropy calculation
- `string` — character set constants
- ANSI escape codes — coloured terminal output

---

## 💡 How It Works

1. User selects a preset or builds a custom character set
2. User specifies the desired password length
3. Engine guarantees at least one character from each enabled set
4. Remaining characters are filled from the full pool using `secrets.choice()`
5. The list is shuffled using `random.SystemRandom()` to prevent pattern bias
6. Strength is analysed via entropy calculation and checklist scoring

---

## 👤 Author

Built as part of a Python Development Internship project.
