"""Core framework for calculator definitions."""
import math
from typing import Any, Dict, List, Optional


def fmt(x: Any, dp: int = 6) -> str:
    """Format a number nicely: trim trailing zeros, use commas for big ints."""
    try:
        f = float(x)
    except (TypeError, ValueError):
        return str(x)
    if math.isnan(f) or math.isinf(f):
        return "Invalid"
    if abs(f) >= 1e12 or (abs(f) < 1e-9 and f != 0):
        return f"{f:.6e}"
    if f == int(f) and abs(f) < 1e12:
        return f"{int(f):,}"
    s = f"{f:,.{dp}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


def money(x: Any, currency: str = "$") -> str:
    """Format as currency."""
    try:
        f = float(x)
    except (TypeError, ValueError):
        return str(x)
    return f"{currency}{fmt(f, 2)}"


class InputField:
    """Definition of one input field for a calculator form."""

    def __init__(
        self,
        key: str,
        label: str,
        field_type: str = "number",
        default: Any = None,
        options: Optional[List[str]] = None,
        unit: str = "",
        required: bool = True,
        minimum: Optional[float] = None,
        maximum: Optional[float] = None,
        hint: str = "",
    ):
        self.key = key
        self.label = label
        self.field_type = field_type  # number, select, date, text
        self.default = default
        self.options = options or []
        self.unit = unit
        self.required = required
        self.minimum = minimum
        self.maximum = maximum
        self.hint = hint


class CalcResult:
    """A single result line shown to the user."""

    def __init__(self, label: str, value: Any, formula: str = "", group: str = ""):
        self.label = label
        self.value = value
        self.formula = formula
        self.group = group


class Calculator:
    """Base class for all calculators."""

    id: str = ""
    name: str = ""
    category: str = ""
    description: str = ""
    inputs: List[InputField] = []
    example: str = ""
    icon: str = "🧮"

    def calculate(self, values: Dict[str, Any]) -> List[CalcResult]:
        raise NotImplementedError

    def get_inputs(self) -> List[InputField]:
        return self.inputs

    # -- convenience helpers for subclass calculate() ----------------
    def num(self, values: Dict[str, Any], key: str) -> float:
        """Safely read a numeric input."""
        return float(values.get(key, 0.0))

    def result(self, label: str, value: Any, formula: str = "", group: str = "") -> CalcResult:
        return CalcResult(label, value, formula, group)
