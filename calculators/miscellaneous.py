"""Miscellaneous calculators."""
import math
import random
import secrets
from datetime import date, datetime, timedelta
from .base import Calculator, CalcResult, InputField, fmt, money


class LovePercentageCalc(Calculator):
    id = "misc_love"
    name = "Love Percentage (Fun)"
    category = "Miscellaneous"
    description = "Fun compatibility score based on names"
    icon = "💕"
    example = "Enter two names for a fun score"

    def get_inputs(self):
        return [
            InputField("name1", "Your name", "text", "Alex"),
            InputField("name2", "Partner's name", "text", "Sam"),
        ]

    def calculate(self, values):
        n1 = str(values.get("name1", "")).strip().lower()
        n2 = str(values.get("name2", "")).strip().lower()
        if not n1 or not n2:
            raise ValueError("Enter both names")
        combined = n1 + n2
        # Deterministic pseudo-random from names
        seed_val = sum(ord(c) for c in combined) + len(combined) * 13
        random.seed(seed_val)
        score = random.randint(50, 99)
        random.seed()
        if score >= 90:
            msg = "Perfect match! 💖"
        elif score >= 75:
            msg = "Great compatibility! ❤️"
        elif score >= 60:
            msg = "Good vibes! 💘"
        else:
            msg = "Needs a little work 💔"
        return [
            CalcResult("Compatibility score", f"{score}%"),
            CalcResult("Verdict", msg),
            CalcResult("Disclaimer", "Just for fun — not scientific!"),
        ]


class CompatibilityScoreCalc(Calculator):
    id = "misc_compatibility"
    name = "Compatibility Score"
    category = "Miscellaneous"
    description = "Fun compatibility between two people"
    icon = "🤝"
    example = "Based on names and interests"

    def get_inputs(self):
        return [
            InputField("name1", "Person 1", "text", "Alex"),
            InputField("name2", "Person 2", "text", "Sam"),
            InputField("interests", "Shared interests (comma sep.)", "text", "Music,Travel"),
        ]

    def calculate(self, values):
        n1 = str(values.get("name1", "")).strip()
        n2 = str(values.get("name2", "")).strip()
        interests = [x.strip() for x in str(values.get("interests", "")).split(",") if x.strip()]
        base = (len(n1) + len(n2)) * 5 % 40 + 50
        interest_bonus = min(len(interests) * 8, 30)
        score = min(base + interest_bonus, 99)
        if score >= 85:
            verdict = "Extremely compatible"
        elif score >= 70:
            verdict = "Very compatible"
        elif score >= 55:
            verdict = "Compatible"
        else:
            verdict = "Less compatible"
        return [
            CalcResult("Compatibility score", f"{score}%"),
            CalcResult("Verdict", verdict),
            CalcResult("Shared interests count", len(interests)),
        ]


class RandomNumberCalc(Calculator):
    id = "misc_random"
    name = "Random Number Generator"
    category = "Miscellaneous"
    description = "Generate random numbers in a range"
    icon = "🎲"
    example = "1-100, 5 numbers"

    def get_inputs(self):
        return [
            InputField("min", "Minimum", "number", 1),
            InputField("max", "Maximum", "number", 100),
            InputField("count", "How many", "number", 5),
        ]

    def calculate(self, values):
        lo, hi = int(self.num(values, "min")), int(self.num(values, "max"))
        count = int(self.num(values, "count"))
        if lo > hi:
            raise ValueError("Minimum cannot exceed maximum")
        if count < 1 or count > 100:
            raise ValueError("Count must be between 1 and 100")
        nums = [secrets.randbelow(hi - lo + 1) + lo for _ in range(count)]
        return [
            CalcResult("Random numbers", ", ".join(str(n) for n in nums)),
            CalcResult("Range", f"{lo} – {hi}"),
            CalcResult("Sorted", ", ".join(str(n) for n in sorted(nums))),
        ]


class PasswordStrengthCalc(Calculator):
    id = "misc_password"
    name = "Password Strength"
    category = "Miscellaneous"
    description = "Estimate password strength"
    icon = "🔐"
    example = "Length, character variety, entropy"

    def get_inputs(self):
        return [
            InputField("password", "Password", "text", "P@ssw0rd123"),
        ]

    def calculate(self, values):
        pw = str(values.get("password", ""))
        length = len(pw)
        has_lower = any(c.islower() for c in pw)
        has_upper = any(c.isupper() for c in pw)
        has_digit = any(c.isdigit() for c in pw)
        has_sym = any(not c.isalnum() for c in pw)
        pool = 0
        if has_lower:
            pool += 26
        if has_upper:
            pool += 26
        if has_digit:
            pool += 10
        if has_sym:
            pool += 32
        entropy = length * math.log2(pool) if pool else 0
        if length < 6 or (length < 8 and pool < 36):
            strength = "Very Weak"
        elif length < 8 or entropy < 40:
            strength = "Weak"
        elif length < 10 or entropy < 60:
            strength = "Medium"
        elif length < 12 or entropy < 80:
            strength = "Strong"
        else:
            strength = "Very Strong"
        return [
            CalcResult("Strength", strength),
            CalcResult("Entropy", f"{fmt(entropy, 1)} bits"),
            CalcResult("Length", length),
            CalcResult("Character types", f"{sum([has_lower, has_upper, has_digit, has_sym])}/4"),
            CalcResult("Time to crack (offline)", f"~{fmt(2 ** max(entropy - 3, 0) / 1e10, 0)} seconds" if entropy else "—"),
        ]


class TipCalculatorCalc(Calculator):
    id = "misc_tip"
    name = "Tip Calculator"
    category = "Miscellaneous"
    description = "Tip amount and total bill"
    icon = "🍽️"
    example = "$50 at 18% tip = $59"

    def get_inputs(self):
        return [
            InputField("bill", "Bill amount", "number", 50),
            InputField("tip_pct", "Tip (%)", "number", 18),
        ]

    def calculate(self, values):
        bill, tip_pct = self.num(values, "bill"), self.num(values, "tip_pct")
        tip = bill * tip_pct / 100
        total = bill + tip
        return [
            CalcResult("Tip amount", money(tip)),
            CalcResult("Total bill", money(total)),
            CalcResult("Per person (2-way)", money(total / 2)),
            CalcResult("Per person (3-way)", money(total / 3)),
        ]


class BillSplittingCalc(Calculator):
    id = "misc_bill_split"
    name = "Bill Splitting"
    category = "Miscellaneous"
    description = "Split a bill among people"
    icon = "🧾"
    example = "$100 among 4 = $25 each"

    def get_inputs(self):
        return [
            InputField("total", "Total bill", "number", 100),
            InputField("people", "Number of people", "number", 4),
            InputField("tip_pct", "Tip (%)", "number", 0, required=False),
        ]

    def calculate(self, values):
        total = self.num(values, "total")
        people = self.num(values, "people")
        tip_pct = self.num(values, "tip_pct")
        if people <= 0:
            raise ValueError("People must be positive")
        tip = total * tip_pct / 100
        grand = total + tip
        per = grand / people
        return [
            CalcResult("Tip amount", money(tip)),
            CalcResult("Total with tip", money(grand)),
            CalcResult("Per person", money(per)),
        ]


class CountdownTimersCalc(Calculator):
    id = "misc_countdown"
    name = "Countdown Timer"
    category = "Miscellaneous"
    description = "Time remaining until a target time today"
    icon = "⏳"
    example = "Target 18:00 → time remaining"

    def get_inputs(self):
        return [
            InputField("target", "Target time (HH:MM)", "text", "18:00"),
        ]

    def calculate(self, values):
        parts = str(values.get("target", "18:00")).split(":")
        try:
            target_h = int(parts[0])
            target_m = int(parts[1]) if len(parts) > 1 else 0
        except (ValueError, IndexError):
            raise ValueError("Enter time as HH:MM")
        now = datetime.now()
        target = now.replace(hour=target_h, minute=target_m, second=0, microsecond=0)
        diff = (target - now).total_seconds()
        if diff < 0:
            target = target + timedelta(days=1)
            diff = (target - now).total_seconds()
        h = int(diff // 3600)
        m = int((diff % 3600) // 60)
        s = int(diff % 60)
        return [
            CalcResult("Time remaining", f"{h:02d}:{m:02d}:{s:02d}"),
            CalcResult("In seconds", fmt(int(diff))),
            CalcResult("Target time", target.strftime("%I:%M %p")),
        ]


class AgeYearsMonthsDaysCalc(Calculator):
    id = "misc_age_ymd"
    name = "Age in Years, Months, Days"
    category = "Miscellaneous"
    description = "Exact age breakdown"
    icon = "🎂"
    example = "Born 1990-01-15"

    def get_inputs(self):
        return [
            InputField("dob", "Date of birth", "date", "1990-01-15"),
        ]

    def calculate(self, values):
        raw = str(values.get("dob", ""))
        try:
            dob = datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Enter a valid date (YYYY-MM-DD)")
        today = date.today()
        if dob > today:
            raise ValueError("Date of birth cannot be in the future")
        years = today.year - dob.year
        months = today.month - dob.month
        days = today.day - dob.day
        if days < 0:
            months -= 1
            prev = today.replace(day=1) - timedelta(days=1)
            days += prev.day
        if months < 0:
            years -= 1
            months += 12
        total_days = (today - dob).days
        return [
            CalcResult("Age", f"{years} years, {months} months, {days} days"),
            CalcResult("Total days", fmt(total_days)),
            CalcResult("Next birthday in", self._next_bday(dob, today)),
        ]

    def _next_bday(self, dob, today):
        try:
            nb = dob.replace(year=today.year)
        except ValueError:
            nb = dob.replace(year=today.year, day=28)
        if nb < today:
            try:
                nb = dob.replace(year=today.year + 1)
            except ValueError:
                nb = dob.replace(year=today.year + 1, day=28)
        return f"{fmt((nb - today).days)} days"


class LifeExpectancyCalc(Calculator):
    id = "misc_life_expect"
    name = "Life Expectancy"
    category = "Miscellaneous"
    description = "Rough life expectancy estimate"
    icon = "🌳"
    example = "Age, gender, lifestyle factors"

    def get_inputs(self):
        return [
            InputField("age", "Current age", "number", 30),
            InputField("gender", "Gender", "select", "Male", options=["Male", "Female"]),
            InputField("smoker", "Smoker?", "select", "No", options=["Yes", "No"]),
            InputField("exercise", "Exercise (days/week)", "number", 3),
        ]

    def calculate(self, values):
        age = self.num(values, "age")
        gender = values.get("gender", "Male")
        base = 78 if gender == "Male" else 82
        base -= 8 if values.get("smoker", "No") == "Yes" else 0
        base += min(int(self.num(values, "exercise")) * 1, 5)
        remaining = max(base - age, 0)
        death_year = date.today().year + int(remaining)
        return [
            CalcResult("Estimated life expectancy", f"{base} years"),
            CalcResult("Years remaining (approx)", f"{fmt(remaining, 1)} years"),
            CalcResult("Estimated year of passing", str(death_year)),
            CalcResult("Disclaimer", "Rough estimate — many factors affect longevity"),
        ]


class CarbonFootprintCalc(Calculator):
    id = "misc_carbon"
    name = "Carbon Footprint"
    category = "Miscellaneous"
    description = "Annual carbon footprint estimate"
    icon = "🌍"
    example = "Electricity, driving, flights, diet"

    def get_inputs(self):
        return [
            InputField("electricity", "Monthly electricity (kWh)", "number", 300),
            InputField("driving", "Annual driving (km)", "number", 12000),
            InputField("flights", "Flights per year", "number", 2),
            InputField("diet", "Diet type", "select", "Mixed", options=["Vegan", "Vegetarian", "Mixed", "Meat-heavy"]),
        ]

    def calculate(self, values):
        elec = self.num(values, "electricity") * 12 * 0.5  # kg CO2 per kWh (varies)
        driving = self.num(values, "driving") * 0.17  # kg CO2 per km
        flights = self.num(values, "flights") * 1500  # avg short-haul
        diet_factors = {"Vegan": 900, "Vegetarian": 1100, "Mixed": 1600, "Meat-heavy": 2400}
        diet = diet_factors.get(values.get("diet", "Mixed"), 1600)
        total = elec + driving + flights + diet
        return [
            CalcResult("Electricity footprint", f"{fmt(elec, 0)} kg CO₂/yr"),
            CalcResult("Driving footprint", f"{fmt(driving, 0)} kg CO₂/yr"),
            CalcResult("Flights footprint", f"{fmt(flights, 0)} kg CO₂/yr"),
            CalcResult("Diet footprint", f"{fmt(diet, 0)} kg CO₂/yr"),
            CalcResult("Total carbon footprint", f"{fmt(total, 0)} kg CO₂/yr"),
            CalcResult("Trees needed to offset", f"{fmt(total / 21, 0)} trees/yr"),
        ]
