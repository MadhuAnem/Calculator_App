# AllCalc ΓÇö 206 Calculators in One Application

A comprehensive multi-calculator desktop application built with **Python + Tkinter** (standard library only, no third-party dependencies).

## Γû╢∩╕Å How to Run

**Double-click** `Run_AllCalc.bat` ΓÇö or run from a terminal:

```
cd C:\Madhu
python app.py
```

Requires **Python 3.8+** with Tkinter (included by default on Windows installs).

## ≡ƒôª What's Inside

| Category | # Calculators |
|---------------------------|----|
| Basic Mathematics | 18 |
| Financial Calculations | 25 |
| Health & Fitness | 12 |
| Education | 8 |
| Date & Time | 10 |
| Engineering | 15 |
| Physics | 6 |
| Electricity | 10 |
| Chemistry | 8 |
| Construction | 9 |
| Business | 10 |
| Statistics | 9 |
| Computer Science | 8 |
| Unit Conversion | 13 |
| Travel | 7 |
| Agriculture | 6 |
| Shopping | 6 |
| Household | 7 |
| Astronomy | 4 |
| Probability & Games | 5 |
| Miscellaneous | 10 |
| **Total** | **206** |

## Γ£¿ Features

- ≡ƒöì **Instant search** ΓÇö find any calculator by name in the sidebar or from the home screen
- ≡ƒùé∩╕Å **21 categories** with color-coded cards on the home screen
- ≡ƒô¥ **Live forms** ΓÇö each calculator generates its own input form dynamically
- ≡ƒôè **Rich results** ΓÇö values shown with formulas and explanations
- ΓÜá∩╕Å **Validation** ΓÇö friendly error messages for invalid inputs (division by zero, bad dates, etc.)
- ≡ƒÄ¿ **Modern dark UI** with a cyan/amber accent theme
- ≡ƒû▒∩╕Å **Scrollable** sidebar and body for small screens
- ≡ƒº« **Everyday & niche calculators**: BMI, EMI, SIP, tax, concrete, GPA, currency, password strength, love %, and much more

## ≡ƒùé∩╕Å Project Structure

```
C:\Madhu\
Γö£ΓöÇΓöÇ app.py                    # Main Tkinter GUI (entry point)
Γö£ΓöÇΓöÇ Run_AllCalc.bat           # Double-click launcher
Γö£ΓöÇΓöÇ README.md
Γö£ΓöÇΓöÇ check_syntax.py           # Syntax validation utility
ΓööΓöÇΓöÇ calculators\              # Calculator engine (data-driven)
    Γö£ΓöÇΓöÇ __init__.py           # Registry ΓÇö auto-collects all calculators
    Γö£ΓöÇΓöÇ base.py               # InputField / CalcResult / Calculator base classes
    Γö£ΓöÇΓöÇ math_calc.py          # Basic Mathematics (18)
    Γö£ΓöÇΓöÇ financial.py          # Financial Calculations (25)
    Γö£ΓöÇΓöÇ health.py             # Health & Fitness (12)
    Γö£ΓöÇΓöÇ education.py          # Education (8)
    Γö£ΓöÇΓöÇ datetime_calc.py      # Date & Time (10)
    Γö£ΓöÇΓöÇ engineering.py        # Engineering (15)
    Γö£ΓöÇΓöÇ physics.py            # Physics (6)
    Γö£ΓöÇΓöÇ electricity.py        # Electricity (10)
    Γö£ΓöÇΓöÇ chemistry.py          # Chemistry (8)
    Γö£ΓöÇΓöÇ construction.py       # Construction (9)
    Γö£ΓöÇΓöÇ business.py           # Business (10)
    Γö£ΓöÇΓöÇ statistics.py         # Statistics (9)
    Γö£ΓöÇΓöÇ computer_science.py   # Computer Science (8)
    Γö£ΓöÇΓöÇ unit_conversion.py    # Unit Conversion (13)
    Γö£ΓöÇΓöÇ travel.py             # Travel (7)
    Γö£ΓöÇΓöÇ agriculture.py        # Agriculture (6)
    Γö£ΓöÇΓöÇ shopping.py           # Shopping (6)
    Γö£ΓöÇΓöÇ household.py          # Household (7)
    Γö£ΓöÇΓöÇ astronomy.py          # Astronomy (4)
    Γö£ΓöÇΓöÇ probability.py        # Probability & Games (5)
    ΓööΓöÇΓöÇ miscellaneous.py      # Miscellaneous (10)
```

## ≡ƒöº Adding a New Calculator

Every calculator is a Python class extending `Calculator` in a category module. It self-registers automatically:

```python
class MyCalc(Calculator):
    id = "my_calc"                 # unique id
    name = "My Calculator"
    category = "Basic Mathematics"
    description = "What it does"
    icon = "≡ƒº«"
    example = "Sample input ΓåÆ result"

    def get_inputs(self):
        return [
            InputField("a", "First number", "number", 100),
            InputField("mode", "Mode", "select", "Auto", options=["Auto", "Manual"]),
        ]

    def calculate(self, values):
        a = self.num(values, "a")
        return [CalcResult("Result", a * 2, "a ├ù 2")]
```

## Γ£à Verification

Run the built-in validation suite:

```
python check_syntax.py
```

It verifies every module compiles, counts all registered calculators, and tests each calculator's `calculate()` method with default inputs.

---

**Note:** Financial, health, tax, and other results are **estimates** for general reference only ΓÇö always confirm with a licensed professional or official source.

