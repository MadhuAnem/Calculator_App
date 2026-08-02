"""Basic Mathematics calculators."""
import math
from typing import Dict, List

from .base import Calculator, CalcResult, InputField, fmt


class AddCalc(Calculator):
    id = "math_add"
    name = "Addition"
    category = "Basic Mathematics"
    description = "Add two or more numbers together"
    icon = "➕"
    example = "12 + 7 = 19"

    def get_inputs(self):
        return [
            InputField("nums", "Numbers (comma separated)", "text", "1,2,3"),
        ]

    def calculate(self, values):
        try:
            nums = [float(x.strip()) for x in str(values.get("nums", "")).split(",") if x.strip()]
        except ValueError:
            raise ValueError("Please enter valid numbers separated by commas")
        if not nums:
            raise ValueError("Please enter at least one number")
        total = sum(nums)
        return [
            CalcResult("Sum", total, "Sum = " + " + ".join(f"{fmt(n)}" for n in nums)),
            CalcResult("Count of numbers", len(nums)),
        ]


class SubtractCalc(Calculator):
    id = "math_subtract"
    name = "Subtraction"
    category = "Basic Mathematics"
    description = "Subtract the second number from the first"
    icon = "➖"
    example = "15 - 8 = 7"

    def get_inputs(self):
        return [
            InputField("a", "First number (minuend)", "number", 15),
            InputField("b", "Second number (subtrahend)", "number", 8),
        ]

    def calculate(self, values):
        a, b = self.num(values, "a"), self.num(values, "b")
        return [CalcResult("Difference", a - b, f"{fmt(a)} - {fmt(b)} = {fmt(a - b)}")]


class MultiplyCalc(Calculator):
    id = "math_multiply"
    name = "Multiplication"
    category = "Basic Mathematics"
    description = "Multiply two or more numbers"
    icon = "✖️"
    example = "6 × 7 = 42"

    def get_inputs(self):
        return [
            InputField("nums", "Numbers (comma separated)", "text", "6,7"),
        ]

    def calculate(self, values):
        try:
            nums = [float(x.strip()) for x in str(values.get("nums", "")).split(",") if x.strip()]
        except ValueError:
            raise ValueError("Please enter valid numbers separated by commas")
        if not nums:
            raise ValueError("Please enter at least one number")
        prod = 1
        for n in nums:
            prod *= n
        return [
            CalcResult("Product", prod, "Product = " + " × ".join(f"{fmt(n)}" for n in nums)),
            CalcResult("Count of numbers", len(nums)),
        ]


class DivideCalc(Calculator):
    id = "math_divide"
    name = "Division"
    category = "Basic Mathematics"
    description = "Divide the first number by the second"
    icon = "➗"
    example = "20 ÷ 5 = 4"

    def get_inputs(self):
        return [
            InputField("a", "Dividend", "number", 20),
            InputField("b", "Divisor", "number", 5),
        ]

    def calculate(self, values):
        a, b = self.num(values, "a"), self.num(values, "b")
        if b == 0:
            raise ValueError("Cannot divide by zero")
        q = a / b
        r = a % b
        return [
            CalcResult("Quotient", q, f"{fmt(a)} ÷ {fmt(b)} = {fmt(q)}"),
            CalcResult("Remainder", r, f"{fmt(a)} mod {fmt(b)} = {fmt(r)}"),
        ]


class PercentageCalc(Calculator):
    id = "math_percent"
    name = "Percentage"
    category = "Basic Mathematics"
    description = "Calculate a percentage of a value"
    icon = "％"
    example = "20% of 250 = 50"

    def get_inputs(self):
        return [
            InputField("pct", "Percentage (%)", "number", 20),
            InputField("value", "Value", "number", 250),
        ]

    def calculate(self, values):
        pct, value = self.num(values, "pct"), self.num(values, "value")
        result = (pct / 100) * value
        return [
            CalcResult("Result", result, f"{fmt(pct)}% of {fmt(value)} = {fmt(result)}"),
            CalcResult("Percentage as decimal", pct / 100),
        ]


class PercentOfCalc(Calculator):
    id = "math_percent_of"
    name = "Percentage (Part of Whole)"
    category = "Basic Mathematics"
    description = "What percent is one number of another?"
    icon = "🔄"
    example = "50 is 25% of 200"

    def get_inputs(self):
        return [
            InputField("part", "Part", "number", 50),
            InputField("whole", "Whole", "number", 200),
        ]

    def calculate(self, values):
        part, whole = self.num(values, "part"), self.num(values, "whole")
        if whole == 0:
            raise ValueError("Whole cannot be zero")
        pct = (part / whole) * 100
        return [
            CalcResult("Percentage", f"{fmt(pct, 4)}%", f"{fmt(part)} is {fmt(pct, 4)}% of {fmt(whole)}"),
        ]


class PercentChangeCalc(Calculator):
    id = "math_percent_change"
    name = "Percentage Change"
    category = "Basic Mathematics"
    description = "Increase/decrease between two values as a percentage"
    icon = "📈"
    example = "From 80 to 100 = +25%"

    def get_inputs(self):
        return [
            InputField("old", "Original value", "number", 80),
            InputField("new", "New value", "number", 100),
        ]

    def calculate(self, values):
        old, new = self.num(values, "old"), self.num(values, "new")
        if old == 0:
            raise ValueError("Original value cannot be zero")
        change = ((new - old) / old) * 100
        direction = "increase" if change >= 0 else "decrease"
        return [
            CalcResult("Percentage change", f"{fmt(change, 4)}%", f"{direction} from {fmt(old)} to {fmt(new)}"),
            CalcResult("Absolute change", new - old),
        ]


class AverageCalc(Calculator):
    id = "math_average"
    name = "Average (Mean)"
    category = "Basic Mathematics"
    description = "Mean of a list of numbers"
    icon = "⚖️"
    example = "Average of 2, 4, 6 = 4"

    def get_inputs(self):
        return [
            InputField("nums", "Numbers (comma separated)", "text", "2,4,6"),
        ]

    def calculate(self, values):
        try:
            nums = [float(x.strip()) for x in str(values.get("nums", "")).split(",") if x.strip()]
        except ValueError:
            raise ValueError("Please enter valid numbers separated by commas")
        if not nums:
            raise ValueError("Please enter at least one number")
        mean = sum(nums) / len(nums)
        return [
            CalcResult("Average (Mean)", mean, f"Sum ({fmt(sum(nums))}) ÷ Count ({len(nums)})"),
            CalcResult("Sum", sum(nums)),
            CalcResult("Count", len(nums)),
        ]


class RatioCalc(Calculator):
    id = "math_ratio"
    name = "Ratio"
    category = "Basic Mathematics"
    description = "Simplify a ratio of two numbers"
    icon = "➗"
    example = "10 : 15 = 2 : 3"

    def get_inputs(self):
        return [
            InputField("a", "First term", "number", 10),
            InputField("b", "Second term", "number", 15),
        ]

    def calculate(self, values):
        a, b = int(self.num(values, "a")), int(self.num(values, "b"))
        if a == 0 and b == 0:
            raise ValueError("Both terms cannot be zero")
        g = math.gcd(a, b)
        if g == 0:
            g = 1
        return [
            CalcResult("Simplified ratio", f"{a // g} : {b // g}", f"GCD = {g}"),
            CalcResult("GCD", g),
            CalcResult("As decimal", a / b if b else "Undefined"),
        ]


class ProportionCalc(Calculator):
    id = "math_proportion"
    name = "Proportion (Solve for x)"
    category = "Basic Mathematics"
    description = "Solve a/b = c/d for an unknown value"
    icon = "🔗"
    example = "2/4 = x/8  →  x = 4"

    def get_inputs(self):
        return [
            InputField("a", "a (known)", "number", 2),
            InputField("b", "b (known)", "number", 4),
            InputField("c", "c (known)", "number", None),
            InputField("x", "x — the unknown in a/b = x/d", "number", 8),
        ]

    def calculate(self, values):
        a, b = self.num(values, "a"), self.num(values, "b")
        c, x = values.get("c"), values.get("x")
        # If c is filled, solve for x = a*d/b (d unknown)... keep simple:
        # a/b = c/d -> if user gives a,b,c -> find d
        # a/b = x/d -> if user gives a,b,d -> find x
        results = []
        if c is not None and str(c).strip() != "":
            c = float(c)
            if b == 0:
                raise ValueError("b cannot be zero")
            d = (c * b) / a if a else 0
            results.append(CalcResult("d (unknown)", d, f"{fmt(a)}/{fmt(b)} = {fmt(c)}/{fmt(d)}"))
        if x is not None and str(x).strip() != "":
            x = float(x)
            if b == 0:
                raise ValueError("b cannot be zero")
            d = (x * b) / a if a else 0
            results.append(CalcResult("d (from x)", d, f"{fmt(a)}/{fmt(b)} = {fmt(x)}/{fmt(d)}"))
            results.append(CalcResult("Cross check (a·d)", a * d))
            results.append(CalcResult("Cross check (b·x)", b * x))
        if not results:
            raise ValueError("Fill either c or x")
        return results


class FractionCalc(Calculator):
    id = "math_fraction"
    name = "Fraction to Decimal"
    category = "Basic Mathematics"
    description = "Convert a fraction to decimal and percentage"
    icon = "🍕"
    example = "3/4 = 0.75 = 75%"

    def get_inputs(self):
        return [
            InputField("num", "Numerator", "number", 3),
            InputField("den", "Denominator", "number", 4),
        ]

    def calculate(self, values):
        n, d = self.num(values, "num"), self.num(values, "den")
        if d == 0:
            raise ValueError("Denominator cannot be zero")
        dec = n / d
        g = math.gcd(int(n), int(d))
        return [
            CalcResult("Decimal", dec, f"{fmt(n)} ÷ {fmt(d)}"),
            CalcResult("Percentage", f"{fmt(dec * 100, 4)}%"),
            CalcResult("Simplified fraction", f"{int(n)//g}/{int(d)//g}" if g else "n/a"),
        ]


class DecimalCalc(Calculator):
    id = "math_decimal"
    name = "Decimal to Fraction"
    category = "Basic Mathematics"
    description = "Convert a decimal to a simplified fraction"
    icon = "🔢"
    example = "0.75 = 3/4"

    def get_inputs(self):
        return [
            InputField("dec", "Decimal number", "number", 0.75),
        ]

    def calculate(self, values):
        d = self.num(values, "dec")
        frac = d.as_integer_ratio()
        g = math.gcd(frac[0], frac[1])
        return [
            CalcResult("Fraction", f"{frac[0] // g} / {frac[1] // g}", f"Exact ratio: {frac[0]}/{frac[1]}"),
        ]


class PowersCalc(Calculator):
    id = "math_powers"
    name = "Powers & Roots"
    category = "Basic Mathematics"
    description = "Raise a number to a power or take its root"
    icon = "🔺"
    example = "2^10 = 1024"

    def get_inputs(self):
        return [
            InputField("base", "Base", "number", 2),
            InputField("exp", "Exponent", "number", 10),
        ]

    def calculate(self, values):
        base, exp = self.num(values, "base"), self.num(values, "exp")
        return [
            CalcResult("Power", base ** exp, f"{fmt(base)}^{fmt(exp)}"),
            CalcResult("Square", base ** 2),
            CalcResult("Cube", base ** 3),
            CalcResult("Square root", math.sqrt(base) if base >= 0 else "Invalid"),
            CalcResult("Cube root", base ** (1 / 3) if base >= 0 else -((-base) ** (1 / 3))),
        ]


class LogarithmsCalc(Calculator):
    id = "math_log"
    name = "Logarithms"
    category = "Basic Mathematics"
    description = "Compute log, ln, and log base 10"
    icon = "📉"
    example = "log10(1000) = 3"

    def get_inputs(self):
        return [
            InputField("x", "Number", "number", 1000),
            InputField("base", "Log base", "number", None, required=False, hint="Leave blank to compute log10 and ln"),
        ]

    def calculate(self, values):
        x = self.num(values, "x")
        if x <= 0:
            raise ValueError("Number must be positive")
        results = [CalcResult("log10", math.log10(x), "log₁₀(x)"), CalcResult("ln (natural log)", math.log(x), "ln(x)")]
        base = values.get("base")
        if base is not None and str(base).strip() != "":
            base = float(base)
            if base <= 0 or base == 1:
                raise ValueError("Base must be positive and not equal to 1")
            results.append(CalcResult(f"log base {fmt(base)}", math.log(x, base)))
        return results


class ExponentCalc(Calculator):
    id = "math_exponent"
    name = "Exponential Growth"
    category = "Basic Mathematics"
    description = "Exponential growth/decay: A = P·e^(rt)"
    icon = "🌱"
    example = "P=100, r=5%, t=10 years → A=164.87"

    def get_inputs(self):
        return [
            InputField("p", "Initial amount (P)", "number", 100),
            InputField("r", "Rate per period (%)", "number", 5),
            InputField("t", "Number of periods (t)", "number", 10),
        ]

    def calculate(self, values):
        p, r, t = self.num(values, "p"), self.num(values, "r"), self.num(values, "t")
        rate = r / 100
        a = p * math.exp(rate * t)
        return [
            CalcResult("Final amount (A)", a, "A = P·e^(rt)"),
            CalcResult("Growth factor", math.exp(rate * t)),
            CalcResult("Total change", a - p),
        ]


class FactorialCalc(Calculator):
    id = "math_factorial"
    name = "Factorial"
    category = "Basic Mathematics"
    description = "n! = n × (n-1) × ... × 1"
    icon = "❗"
    example = "5! = 120"

    def get_inputs(self):
        return [
            InputField("n", "n (0-170)", "number", 5, minimum=0, maximum=170),
        ]

    def calculate(self, values):
        n = int(self.num(values, "n"))
        if n < 0:
            raise ValueError("Factorial of a negative number is undefined")
        if n > 170:
            raise ValueError("n must be 170 or less")
        return [CalcResult("n!", math.factorial(n), f"{n}! = {math.factorial(n)}")]


class GCDCalc(Calculator):
    id = "math_gcd"
    name = "GCD / HCF"
    category = "Basic Mathematics"
    description = "Greatest common divisor of two numbers"
    icon = "🧩"
    example = "GCD(48, 36) = 12"

    def get_inputs(self):
        return [
            InputField("a", "First number", "number", 48),
            InputField("b", "Second number", "number", 36),
        ]

    def calculate(self, values):
        a, b = int(self.num(values, "a")), int(self.num(values, "b"))
        g = math.gcd(a, b)
        return [
            CalcResult("GCD / HCF", g, f"gcd({a}, {b})"),
            CalcResult("LCM (derived)", abs(a * b) // g if g else 0),
        ]


class LCMCalc(Calculator):
    id = "math_lcm"
    name = "LCM"
    category = "Basic Mathematics"
    description = "Least common multiple of two numbers"
    icon = "🟰"
    example = "LCM(4, 6) = 12"

    def get_inputs(self):
        return [
            InputField("a", "First number", "number", 4),
            InputField("b", "Second number", "number", 6),
        ]

    def calculate(self, values):
        a, b = int(self.num(values, "a")), int(self.num(values, "b"))
        if a == 0 or b == 0:
            raise ValueError("Numbers cannot be zero")
        lcm = abs(a * b) // math.gcd(a, b)
        return [
            CalcResult("LCM", lcm, f"lcm({a}, {b})"),
            CalcResult("GCD (derived)", math.gcd(a, b)),
        ]
