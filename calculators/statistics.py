"""Statistics calculators."""
import math
from statistics import mean, median, mode, pstdev, pvariance, stdev, variance
from .base import Calculator, CalcResult, InputField, fmt


class MeanCalc(Calculator):
    id = "stat_mean"
    name = "Mean"
    category = "Statistics"
    description = "Arithmetic mean of a dataset"
    icon = "🔢"
    example = "2,4,6,8 → mean 5"

    def get_inputs(self):
        return [
            InputField("data", "Numbers (comma separated)", "text", "2,4,6,8"),
        ]

    def calculate(self, values):
        try:
            data = [float(x.strip()) for x in str(values.get("data", "")).split(",") if x.strip()]
        except ValueError:
            raise ValueError("Enter valid numbers separated by commas")
        if not data:
            raise ValueError("Enter at least one number")
        return [
            CalcResult("Mean", fmt(mean(data)), "Σx / n"),
            CalcResult("Sum", fmt(sum(data))),
            CalcResult("Count", len(data)),
        ]


class MedianCalc(Calculator):
    id = "stat_median"
    name = "Median"
    category = "Statistics"
    description = "Middle value of a dataset"
    icon = "🎯"
    example = "3,1,9,5,7 → median 5"

    def get_inputs(self):
        return [
            InputField("data", "Numbers (comma separated)", "text", "3,1,9,5,7"),
        ]

    def calculate(self, values):
        try:
            data = [float(x.strip()) for x in str(values.get("data", "")).split(",") if x.strip()]
        except ValueError:
            raise ValueError("Enter valid numbers separated by commas")
        if not data:
            raise ValueError("Enter at least one number")
        return [
            CalcResult("Median", fmt(median(data))),
            CalcResult("Sorted data", ", ".join(fmt(x) for x in sorted(data))),
        ]


class ModeCalc(Calculator):
    id = "stat_mode"
    name = "Mode"
    category = "Statistics"
    description = "Most frequent value(s) in a dataset"
    icon = "🔁"
    example = "1,2,2,3,3,3 → mode 3"

    def get_inputs(self):
        return [
            InputField("data", "Numbers (comma separated)", "text", "1,2,2,3,3,3"),
        ]

    def calculate(self, values):
        try:
            data = [float(x.strip()) for x in str(values.get("data", "")).split(",") if x.strip()]
        except ValueError:
            raise ValueError("Enter valid numbers separated by commas")
        if not data:
            raise ValueError("Enter at least one number")
        from collections import Counter
        counts = Counter(data)
        max_count = max(counts.values())
        modes = [k for k, v in counts.items() if v == max_count]
        return [
            CalcResult("Mode", ", ".join(fmt(m) for m in modes)),
            CalcResult("Frequency", f"{max_count} time(s)"),
            CalcResult("Distinct values", len(counts)),
        ]


class VarianceCalc(Calculator):
    id = "stat_variance"
    name = "Variance"
    category = "Statistics"
    description = "Sample and population variance"
    icon = "📊"
    example = "2,4,6,8 → sample var 6.67"

    def get_inputs(self):
        return [
            InputField("data", "Numbers (comma separated)", "text", "2,4,6,8"),
        ]

    def calculate(self, values):
        try:
            data = [float(x.strip()) for x in str(values.get("data", "")).split(",") if x.strip()]
        except ValueError:
            raise ValueError("Enter valid numbers separated by commas")
        if len(data) < 2:
            raise ValueError("Need at least 2 numbers")
        return [
            CalcResult("Sample variance", fmt(variance(data), 4)),
            CalcResult("Population variance", fmt(pvariance(data), 4)),
            CalcResult("Mean", fmt(mean(data))),
        ]


class StdDevCalc(Calculator):
    id = "stat_stddev"
    name = "Standard Deviation"
    category = "Statistics"
    description = "Sample and population standard deviation"
    icon = "📉"
    example = "2,4,6,8 → sample σ 2.58"

    def get_inputs(self):
        return [
            InputField("data", "Numbers (comma separated)", "text", "2,4,6,8"),
        ]

    def calculate(self, values):
        try:
            data = [float(x.strip()) for x in str(values.get("data", "")).split(",") if x.strip()]
        except ValueError:
            raise ValueError("Enter valid numbers separated by commas")
        if len(data) < 2:
            raise ValueError("Need at least 2 numbers")
        s = stdev(data)
        p = pstdev(data)
        m = mean(data)
        return [
            CalcResult("Sample std dev", fmt(s, 4)),
            CalcResult("Population std dev", fmt(p, 4)),
            CalcResult("Mean", fmt(m)),
            CalcResult("Coefficient of variation", f"{fmt(s / m * 100 if m else 0, 2)}%"),
        ]


class ProbabilityCalc(Calculator):
    id = "stat_probability"
    name = "Probability"
    category = "Statistics"
    description = "Probability of an event"
    icon = "🎲"
    example = "3 favorable of 10 → 0.3 (30%)"

    def get_inputs(self):
        return [
            InputField("favorable", "Favorable outcomes", "number", 3),
            InputField("total", "Total outcomes", "number", 10),
        ]

    def calculate(self, values):
        fav, total = self.num(values, "favorable"), self.num(values, "total")
        if total <= 0:
            raise ValueError("Total outcomes must be positive")
        p = fav / total
        return [
            CalcResult("Probability", fmt(p, 6), "favourable/total"),
            CalcResult("As percentage", f"{fmt(p * 100, 2)}%"),
            CalcResult("Odds", f"{fmt(fav,0)} : {fmt(total - fav,0)}"),
        ]


class CorrelationCalc(Calculator):
    id = "stat_correlation"
    name = "Correlation"
    category = "Statistics"
    description = "Pearson correlation coefficient"
    icon = "📈"
    example = "x=1,2,3 y=2,4,6 → r=1.0"

    def get_inputs(self):
        return [
            InputField("x", "X values (comma separated)", "text", "1,2,3"),
            InputField("y", "Y values (comma separated)", "text", "2,4,6"),
        ]

    def calculate(self, values):
        try:
            xs = [float(x.strip()) for x in str(values.get("x", "")).split(",") if x.strip()]
            ys = [float(y.strip()) for y in str(values.get("y", "")).split(",") if y.strip()]
        except ValueError:
            raise ValueError("Enter valid numbers separated by commas")
        if len(xs) != len(ys) or len(xs) < 2:
            raise ValueError("X and Y must have the same length (min 2)")
        n = len(xs)
        mx, my = mean(xs), mean(ys)
        num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
        r = num / den if den else 0
        if abs(r) >= 0.8:
            strength = "Strong"
        elif abs(r) >= 0.5:
            strength = "Moderate"
        elif abs(r) >= 0.3:
            strength = "Weak"
        else:
            strength = "Negligible"
        direction = "positive" if r >= 0 else "negative"
        return [
            CalcResult("Correlation (r)", fmt(r, 4)),
            CalcResult("Strength", f"{strength} ({direction})"),
            CalcResult("r² (coefficient of determination)", fmt(r * r, 4)),
        ]


class RegressionCalc(Calculator):
    id = "stat_regression"
    name = "Linear Regression"
    category = "Statistics"
    description = "Fit y = mx + b to data"
    icon = "📐"
    example = "x=1,2,3,4 y=2,4,5,7 → slope 1.6"

    def get_inputs(self):
        return [
            InputField("x", "X values (comma separated)", "text", "1,2,3,4"),
            InputField("y", "Y values (comma separated)", "text", "2,4,5,7"),
        ]

    def calculate(self, values):
        try:
            xs = [float(x.strip()) for x in str(values.get("x", "")).split(",") if x.strip()]
            ys = [float(y.strip()) for y in str(values.get("y", "")).split(",") if y.strip()]
        except ValueError:
            raise ValueError("Enter valid numbers separated by commas")
        if len(xs) != len(ys) or len(xs) < 2:
            raise ValueError("X and Y must have the same length (min 2)")
        n = len(xs)
        mx, my = mean(xs), mean(ys)
        num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        den = sum((x - mx) ** 2 for x in xs)
        m = num / den if den else 0
        b = my - m * mx
        preds = [m * x + b for x in xs]
        sse = sum((y - p) ** 2 for y, p in zip(ys, preds))
        sst = sum((y - my) ** 2 for y in ys)
        r2 = 1 - sse / sst if sst else 0
        return [
            CalcResult("Equation", f"y = {fmt(m, 4)}x + {fmt(b, 4)}"),
            CalcResult("Slope (m)", fmt(m, 4)),
            CalcResult("Intercept (b)", fmt(b, 4)),
            CalcResult("R²", fmt(r2, 4)),
        ]


class PercentilesCalc(Calculator):
    id = "stat_percentile"
    name = "Percentiles"
    category = "Statistics"
    description = "Value at a given percentile"
    icon = "📊"
    example = "1,2,3,4,5 → P50 = 3"

    def get_inputs(self):
        return [
            InputField("data", "Numbers (comma separated)", "text", "1,2,3,4,5"),
            InputField("p", "Percentile (0-100)", "number", 50),
        ]

    def calculate(self, values):
        try:
            data = sorted(float(x.strip()) for x in str(values.get("data", "")).split(",") if x.strip())
        except ValueError:
            raise ValueError("Enter valid numbers separated by commas")
        if not data:
            raise ValueError("Enter at least one number")
        p = self.num(values, "p")
        if not 0 <= p <= 100:
            raise ValueError("Percentile must be between 0 and 100")
        k = (len(data) - 1) * p / 100
        lo = int(math.floor(k))
        hi = int(math.ceil(k))
        if lo == hi:
            val = data[lo]
        else:
            frac = k - lo
            val = data[lo] + frac * (data[hi] - data[lo])
        return [
            CalcResult(f"P{p:g}", fmt(val, 4)),
            CalcResult("Min", fmt(data[0])),
            CalcResult("Max", fmt(data[-1])),
            CalcResult("Range", fmt(data[-1] - data[0])),
        ]
