"""Calculator registry — collects every calculator from all category modules."""
from typing import Dict, List, Optional

from .base import Calculator, InputField, CalcResult, fmt, money

# Import category modules (they self-register via REGISTRY)
from . import (
    math_calc,
    financial,
    health,
    education,
    datetime_calc,
    engineering,
    physics,
    electricity,
    chemistry,
    construction,
    business,
    statistics,
    computer_science,
    unit_conversion,
    travel,
    agriculture,
    shopping,
    household,
    astronomy,
    probability,
    miscellaneous,
)

CATEGORIES: Dict[str, List[Calculator]] = {}


def _collect(module, category_label: str) -> None:
    """Collect Calculator subclasses defined in a module (not the base class)."""
    lst = []
    for name in dir(module):
        obj = getattr(module, name)
        if (
            isinstance(obj, type)
            and issubclass(obj, Calculator)
            and obj is not Calculator
            and getattr(obj, "id", "")
        ):
            lst.append(obj())
    lst.sort(key=lambda c: c.name)
    if lst:
        CATEGORIES[category_label] = lst


_collect(math_calc, "Basic Mathematics")
_collect(financial, "Financial Calculations")
_collect(health, "Health & Fitness")
_collect(education, "Education")
_collect(datetime_calc, "Date & Time")
_collect(engineering, "Engineering")
_collect(physics, "Physics")
_collect(electricity, "Electricity")
_collect(chemistry, "Chemistry")
_collect(construction, "Construction")
_collect(business, "Business")
_collect(statistics, "Statistics")
_collect(computer_science, "Computer Science")
_collect(unit_conversion, "Unit Conversion")
_collect(travel, "Travel")
_collect(agriculture, "Agriculture")
_collect(shopping, "Shopping")
_collect(household, "Household")
_collect(astronomy, "Astronomy")
_collect(probability, "Probability & Games")
_collect(miscellaneous, "Miscellaneous")

ALL_CALCULATORS: Dict[str, Calculator] = {}
for cat, lst in CATEGORIES.items():
    for c in lst:
        ALL_CALCULATORS[c.id] = c


def get_calculator(calc_id: str) -> Optional[Calculator]:
    return ALL_CALCULATORS.get(calc_id)


def total_count() -> int:
    return len(ALL_CALCULATORS)
