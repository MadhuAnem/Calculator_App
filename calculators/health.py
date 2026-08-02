"""Health & Fitness calculators."""
import math
from .base import Calculator, CalcResult, InputField, fmt


class BMICalc(Calculator):
    id = "health_bmi"
    name = "BMI"
    category = "Health & Fitness"
    description = "Body Mass Index = weight / height²"
    icon = "⚖️"
    example = "70kg, 1.75m → BMI 22.9"

    def get_inputs(self):
        return [
            InputField("weight", "Weight (kg)", "number", 70),
            InputField("height", "Height (cm)", "number", 175),
        ]

    def calculate(self, values):
        w = self.num(values, "weight")
        h_cm = self.num(values, "height")
        if h_cm <= 0:
            raise ValueError("Height must be positive")
        h = h_cm / 100
        bmi = w / (h ** 2)
        if bmi < 18.5:
            cat = "Underweight"
        elif bmi < 25:
            cat = "Normal weight"
        elif bmi < 30:
            cat = "Overweight"
        else:
            cat = "Obese"
        return [
            CalcResult("BMI", f"{fmt(bmi, 2)}", "weight / height²"),
            CalcResult("Category", cat),
            CalcResult("Ideal weight range (BMI 18.5-25)", f"{fmt(18.5 * h * h, 1)} – {fmt(25 * h * h, 1)} kg"),
        ]


class BMRCalc(Calculator):
    id = "health_bmr"
    name = "BMR"
    category = "Health & Fitness"
    description = "Basal Metabolic Rate (Mifflin-St Jeor)"
    icon = "🔥"
    example = "70kg, 175cm, 30y, male → ~1683 kcal"

    def get_inputs(self):
        return [
            InputField("weight", "Weight (kg)", "number", 70),
            InputField("height", "Height (cm)", "number", 175),
            InputField("age", "Age (years)", "number", 30),
            InputField("gender", "Gender", "select", "Male", options=["Male", "Female"]),
            InputField("activity", "Activity level", "select", "Moderate", options=[
                "Sedentary", "Light", "Moderate", "Active", "Very active",
            ]),
        ]

    def calculate(self, values):
        w = self.num(values, "weight")
        h = self.num(values, "height")
        age = self.num(values, "age")
        gender = values.get("gender", "Male")
        s = 5 if gender == "Male" else -161
        bmr = 10 * w + 6.25 * h - 5 * age + s
        mult = {
            "Sedentary": 1.2, "Light": 1.375, "Moderate": 1.55,
            "Active": 1.725, "Very active": 1.9,
        }
        amr = bmr * mult[values.get("activity", "Moderate")]
        return [
            CalcResult("BMR", f"{fmt(bmr, 0)} kcal/day", "Mifflin-St Jeor equation"),
            CalcResult("AMR (maintenance calories)", f"{fmt(amr, 0)} kcal/day", "BMR × activity factor"),
            CalcResult("Lose weight (−500 cal)", f"{fmt(amr - 500, 0)} kcal/day"),
            CalcResult("Gain weight (+500 cal)", f"{fmt(amr + 500, 0)} kcal/day"),
        ]


class DailyCaloriesCalc(Calculator):
    id = "health_calories"
    name = "Daily Calorie Needs"
    category = "Health & Fitness"
    description = "Calories to maintain/lose/gain weight (Harris-Benedict)"
    icon = "🍎"
    example = "70kg, 175cm, 30y, active male → ~2900 kcal"

    def get_inputs(self):
        return [
            InputField("weight", "Weight (kg)", "number", 70),
            InputField("height", "Height (cm)", "number", 175),
            InputField("age", "Age (years)", "number", 30),
            InputField("gender", "Gender", "select", "Male", options=["Male", "Female"]),
            InputField("activity", "Activity level", "select", "Moderate (3-5 days/week)", options=[
                "Sedentary (little/no exercise)", "Light (1-3 days/week)",
                "Moderate (3-5 days/week)", "Active (6-7 days/week)", "Very active (athlete)",
            ]),
        ]

    def calculate(self, values):
        w = self.num(values, "weight")
        h = self.num(values, "height")
        age = self.num(values, "age")
        gender = values.get("gender", "Male")
        # Revised Harris-Benedict
        if gender == "Male":
            bmr = 88.362 + 13.397 * w + 4.799 * h - 5.677 * age
        else:
            bmr = 447.593 + 9.247 * w + 3.098 * h - 4.330 * age
        mult = {
            "Sedentary (little/no exercise)": 1.2,
            "Light (1-3 days/week)": 1.375,
            "Moderate (3-5 days/week)": 1.55,
            "Active (6-7 days/week)": 1.725,
            "Very active (athlete)": 1.9,
        }
        tdee = bmr * mult[values.get("activity", "Moderate (3-5 days/week)")]
        return [
            CalcResult("Maintain weight", f"{fmt(tdee, 0)} kcal/day"),
            CalcResult("Mild weight loss (0.5 kg/week)", f"{fmt(tdee - 500, 0)} kcal/day"),
            CalcResult("Weight loss (1 kg/week)", f"{fmt(tdee - 1000, 0)} kcal/day"),
            CalcResult("Mild weight gain (0.5 kg/week)", f"{fmt(tdee + 500, 0)} kcal/day"),
        ]


class BodyFatCalc(Calculator):
    id = "health_bodyfat"
    name = "Body Fat Percentage"
    category = "Health & Fitness"
    description = "Estimate body fat % from measurements (US Navy method)"
    icon = "📏"
    example = "Male: waist 85cm, neck 38cm, height 175cm"

    def get_inputs(self):
        return [
            InputField("gender", "Gender", "select", "Male", options=["Male", "Female"]),
            InputField("waist", "Waist (cm)", "number", 85),
            InputField("neck", "Neck (cm)", "number", 38),
            InputField("hip", "Hip (cm) — women only", "number", 0, required=False),
            InputField("height", "Height (cm)", "number", 175),
        ]

    def calculate(self, values):
        gender = values.get("gender", "Male")
        waist = self.num(values, "waist")
        neck = self.num(values, "neck")
        hip = self.num(values, "hip")
        height = self.num(values, "height")
        if gender == "Male":
            bf = 495 / (1.0324 - 0.19077 * math.log10(waist - neck) + 0.15456 * math.log10(height)) - 450
        else:
            bf = 495 / (1.29579 - 0.35004 * math.log10(waist + hip - neck) + 0.22100 * math.log10(height)) - 450
        if bf < 0:
            bf = 0
        if bf < 6:
            cat = "Essential fat"
        elif bf < 14:
            cat = "Athletic"
        elif bf < 18:
            cat = "Fitness"
        elif bf < 25:
            cat = "Average"
        else:
            cat = "Obese"
        return [
            CalcResult("Body fat %", f"{fmt(bf, 1)}%", "US Navy circumference method"),
            CalcResult("Category", cat),
        ]


class LeanBodyMassCalc(Calculator):
    id = "health_lean_body"
    name = "Lean Body Mass"
    category = "Health & Fitness"
    description = "LBM = weight × (1 - body fat%)"
    icon = "💪"
    example = "70kg at 20% BF → LBM 56 kg"

    def get_inputs(self):
        return [
            InputField("weight", "Weight (kg)", "number", 70),
            InputField("bodyfat", "Body fat percentage (%)", "number", 20),
        ]

    def calculate(self, values):
        w = self.num(values, "weight")
        bf = self.num(values, "bodyfat") / 100
        lbm = w * (1 - bf)
        return [
            CalcResult("Lean body mass", f"{fmt(lbm, 1)} kg"),
            CalcResult("Fat mass", f"{fmt(w - lbm, 1)} kg"),
            CalcResult("LBM % of body weight", f"{fmt((1 - bf) * 100, 1)}%"),
        ]


class WaterIntakeCalc(Calculator):
    id = "health_water"
    name = "Water Intake"
    category = "Health & Fitness"
    description = "Daily water intake recommendation"
    icon = "💧"
    example = "70kg, 30min exercise → ~3.2 L/day"

    def get_inputs(self):
        return [
            InputField("weight", "Weight (kg)", "number", 70),
            InputField("exercise", "Exercise (minutes/day)", "number", 30, required=False),
        ]

    def calculate(self, values):
        w = self.num(values, "weight")
        exercise = self.num(values, "exercise")
        base_l = w * 0.033
        extra = (exercise // 30) * 0.35
        total = base_l + extra
        return [
            CalcResult("Daily water intake", f"{fmt(total, 2)} litres"),
            CalcResult("In cups (250ml)", f"{fmt(total * 4, 0)} cups"),
            CalcResult("Base requirement", f"{fmt(base_l, 2)} L"),
            CalcResult("Extra for exercise", f"{fmt(extra, 2)} L"),
        ]


class HeartRateZonesCalc(Calculator):
    id = "health_hr_zones"
    name = "Heart Rate Zones"
    category = "Health & Fitness"
    description = "Training heart rate zones"
    icon = "❤️"
    example = "Age 30 → zones 95–190 bpm"

    def get_inputs(self):
        return [
            InputField("age", "Age (years)", "number", 30),
        ]

    def calculate(self, values):
        age = self.num(values, "age")
        max_hr = 220 - age
        zones = [
            ("Zone 1 — Very light", 50, 60),
            ("Zone 2 — Light (fat burn)", 60, 70),
            ("Zone 3 — Moderate (aerobic)", 70, 80),
            ("Zone 4 — Hard (anaerobic)", 80, 90),
            ("Zone 5 — Maximum", 90, 100),
        ]
        results = [
            CalcResult("Max heart rate", f"{max_hr} bpm", "220 − age"),
            CalcResult("Resting heart rate range", "60–100 bpm", "Normal adult range"),
        ]
        for label, lo, hi in zones:
            results.append(CalcResult(label, f"{round(max_hr * lo / 100)} – {round(max_hr * hi / 100)} bpm"))
        return results


class TargetHeartRateCalc(Calculator):
    id = "health_target_hr"
    name = "Target Heart Rate"
    category = "Health & Fitness"
    description = "Karvonen target heart rate for training"
    icon = "🎯"
    example = "Age 30, resting 70, 70% intensity → 154 bpm"

    def get_inputs(self):
        return [
            InputField("age", "Age (years)", "number", 30),
            InputField("resting", "Resting heart rate (bpm)", "number", 70),
            InputField("intensity", "Intensity (%)", "number", 70),
        ]

    def calculate(self, values):
        age = self.num(values, "age")
        resting = self.num(values, "resting")
        intensity = self.num(values, "intensity") / 100
        max_hr = 220 - age
        thr = resting + (max_hr - resting) * intensity
        return [
            CalcResult("Max heart rate", f"{max_hr} bpm", "220 − age"),
            CalcResult("Heart rate reserve", f"{max_hr - resting} bpm"),
            CalcResult("Target heart rate", f"{round(thr)} bpm", "Karvonen formula"),
        ]


class PregnancyDueDateCalc(Calculator):
    id = "health_due_date"
    name = "Pregnancy Due Date"
    category = "Health & Fitness"
    description = "Estimated due date from LMP (Naegele's rule)"
    icon = "🤰"
    example = "LMP 2024-01-01 → due 2024-10-07"

    def get_inputs(self):
        return [
            InputField("lmp", "First day of last menstrual period", "date", "2024-01-01"),
        ]

    def calculate(self, values):
        from datetime import datetime, timedelta
        lmp_raw = values.get("lmp", "")
        try:
            lmp = datetime.strptime(str(lmp_raw), "%Y-%m-%d")
        except (ValueError, TypeError):
            raise ValueError("Enter a valid date (YYYY-MM-DD)")
        due = lmp + timedelta(days=280)
        today = datetime.now()
        if today > due:
            progress = "past"
        else:
            progress = (due - today).days
        weeks = (due - lmp).days / 7
        if today >= lmp:
            current_week = (today - lmp).days / 7
            trimester = "1st" if current_week < 13 else "2nd" if current_week < 27 else "3rd"
        else:
            current_week = 0
            trimester = "—"
        return [
            CalcResult("Estimated due date", due.strftime("%B %d, %Y"), "LMP + 280 days (Naegele's rule)"),
            CalcResult("Current week of pregnancy", f"{fmt(current_week, 1)} weeks"),
            CalcResult("Current trimester", trimester),
            CalcResult("Days remaining", progress if isinstance(progress, int) else 0),
        ]


class OvulationCalc(Calculator):
    id = "health_ovulation"
    name = "Ovulation Calculator"
    category = "Health & Fitness"
    description = "Fertile window and ovulation date"
    icon = "🩺"
    example = "Cycle 28 days, period 2024-01-01"

    def get_inputs(self):
        return [
            InputField("period_start", "First day of last period", "date", "2024-01-01"),
            InputField("cycle", "Cycle length (days)", "number", 28),
        ]

    def calculate(self, values):
        from datetime import datetime, timedelta
        raw = values.get("period_start", "")
        try:
            start = datetime.strptime(str(raw), "%Y-%m-%d")
        except (ValueError, TypeError):
            raise ValueError("Enter a valid date (YYYY-MM-DD)")
        cycle = int(self.num(values, "cycle"))
        ovulation = start + timedelta(days=cycle - 14)
        fertile_start = ovulation - timedelta(days=5)
        fertile_end = ovulation + timedelta(days=1)
        next_period = start + timedelta(days=cycle)
        return [
            CalcResult("Ovulation date", ovulation.strftime("%B %d, %Y")),
            CalcResult("Fertile window", f"{fertile_start.strftime('%b %d')} – {fertile_end.strftime('%b %d, %Y')}"),
            CalcResult("Next expected period", next_period.strftime("%B %d, %Y")),
        ]


class MedicationDosageCalc(Calculator):
    id = "health_dosage"
    name = "Medication Dosage"
    category = "Health & Fitness"
    description = "Pediatric dosage by weight (general reference — always confirm with a doctor)"
    icon = "💊"
    example = "15 mg/kg for 20 kg = 300 mg"

    def get_inputs(self):
        return [
            InputField("weight", "Weight (kg)", "number", 20),
            InputField("dose", "Dose per kg (mg/kg)", "number", 15),
            InputField("freq", "Doses per day", "number", 3),
        ]

    def calculate(self, values):
        w = self.num(values, "weight")
        dose = self.num(values, "dose")
        freq = self.num(values, "freq")
        per_dose = w * dose
        daily = per_dose * freq
        return [
            CalcResult("Dose per administration", f"{fmt(per_dose, 2)} mg", f"{w} kg × {dose} mg/kg"),
            CalcResult("Total daily dose", f"{fmt(daily, 2)} mg", f"{per_dose} × {freq}/day"),
            CalcResult("Disclaimer", "For reference only — always follow medical advice"),
        ]


class BloodAlcoholCalc(Calculator):
    id = "health_bac"
    name = "Blood Alcohol Estimation"
    category = "Health & Fitness"
    description = "Estimate BAC (Widmark formula)"
    icon = "🍺"
    example = "2 drinks, 70kg male, 2 hours → ~0.04%"

    def get_inputs(self):
        return [
            InputField("drinks", "Number of standard drinks", "number", 2),
            InputField("weight", "Weight (kg)", "number", 70),
            InputField("gender", "Gender", "select", "Male", options=["Male", "Female"]),
            InputField("hours", "Hours since first drink", "number", 2),
        ]

    def calculate(self, values):
        drinks = self.num(values, "drinks")
        w = self.num(values, "weight")
        gender = values.get("gender", "Male")
        hours = self.num(values, "hours")
        # Standard drink = 14g alcohol. Widmark r: male 0.68, female 0.55
        r = 0.68 if gender == "Male" else 0.55
        grams = drinks * 14
        bac = (grams * 100) / (w * 1000 * r) - (0.015 * hours)
        bac = max(bac, 0)
        if bac >= 0.08:
            status = "Above legal driving limit (0.08%)"
        elif bac >= 0.05:
            status = "Impaired — avoid driving"
        elif bac > 0:
            status = "Below 0.08 limit, but caution advised"
        else:
            status = "Estimated zero"
        return [
            CalcResult("Estimated BAC", f"{fmt(bac * 100, 3)}%", "Widmark formula"),
            CalcResult("Status", status),
            CalcResult("Hours to sober (0.02%)", f"{fmt(max((bac - 0.02) / 0.015, 0), 1)} hours"),
            CalcResult("Disclaimer", "Estimate only — not for legal/medical use"),
        ]
