# AllCalc - 206 Calculators in One Application

A comprehensive multi-calculator desktop application built with **Python + Tkinter**.
It uses only the Python standard library - no third-party dependencies required.

## How to Run

**Double-click** `Run_AllCalc.bat` - or run from a terminal:

```
python app.py
```

Requires **Python 3.8+** with Tkinter (included by default on Windows installs).

## What's Inside

| Category               | # Calculators |
|------------------------|---------------|
| Basic Mathematics      | 18            |
| Financial Calculations | 25            |
| Health & Fitness       | 12            |
| Education              | 8             |
| Date & Time            | 10            |
| Engineering            | 15            |
| Physics                | 6             |
| Electricity            | 10            |
| Chemistry              | 8             |
| Construction           | 9             |
| Business               | 10            |
| Statistics             | 9             |
| Computer Science       | 8             |
| Unit Conversion        | 13            |
| Travel                 | 7             |
| Agriculture            | 6             |
| Shopping               | 6             |
| Household              | 7             |
| Astronomy              | 4             |
| Probability & Games    | 5             |
| Miscellaneous          | 10            |
| **Total**              | **206**       |

## Features

- **Instant search** - find any calculator by name in the sidebar or from the home screen
- **21 categories** with cards on the home screen
- **Live forms** - each calculator generates its own input form dynamically
- **Rich results** - values shown with formulas and explanations
- **Validation** - friendly error messages for invalid inputs (division by zero, bad dates, etc.)
- **Modern dark UI** with a cyan/amber accent theme
- **Scrollable** sidebar and body for small screens
- **Everyday & niche calculators**: BMI, EMI, SIP, tax, concrete, GPA, currency, password strength, love %, and much more

## Project Structure

```
Calculator_App/
|-- app.py                    # Main Tkinter GUI (entry point)
|-- Run_AllCalc.bat           # Double-click launcher
|-- README.md
|-- calculators/              # Calculator engine (data-driven)
    |-- __init__.py           # Registry - auto-collects all calculators
    |-- base.py               # InputField / CalcResult / Calculator base classes
    |-- math_calc.py          # Basic Mathematics (18)
    |-- financial.py          # Financial Calculations (25)
    |-- health.py             # Health & Fitness (12)
    |-- education.py          # Education (8)
    |-- datetime_calc.py      # Date & Time (10)
    |-- engineering.py        # Engineering (15)
    |-- physics.py            # Physics (6)
    |-- electricity.py        # Electricity (10)
    |-- chemistry.py          # Chemistry (8)
    |-- construction.py       # Construction (9)
    |-- business.py           # Business (10)
    |-- statistics.py         # Statistics (9)
    |-- computer_science.py   # Computer Science (8)
    |-- unit_conversion.py    # Unit Conversion (13)
    |-- travel.py             # Travel (7)
    |-- agriculture.py        # Agriculture (6)
    |-- shopping.py           # Shopping (6)
    |-- household.py          # Household (7)
    |-- astronomy.py          # Astronomy (4)
    |-- probability.py        # Probability & Games (5)
    |-- miscellaneous.py      # Miscellaneous (10)
```

## Adding a New Calculator

Every calculator is a Python class extending `Calculator` in a category module. It self-registers automatically:

```python
class MyCalc(Calculator):
    id = "my_calc"                 # unique id
    name = "My Calculator"
    category = "Basic Mathematics"
    description = "What it does"
    icon = "="
    example = "Sample input -> result"

    def get_inputs(self):
        return [
            InputField("a", "First number", "number", 100),
            InputField("mode", "Mode", "select", "Auto", options=["Auto", "Manual"]),
        ]

    def calculate(self, values):
        a = self.num(values, "a")
        return [CalcResult("Result", a * 2, "a x 2")]
```

## Verification

Run the built-in validation suite:

```
python check_syntax.py
```

It verifies every module compiles, counts all registered calculators, and tests each calculator's `calculate()` method with default inputs.

---

**Note:** Financial, health, tax, and other results are **estimates** for general reference only - always confirm with a licensed professional or official source.

