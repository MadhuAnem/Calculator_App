"""Agriculture calculators."""
import math
from .base import Calculator, CalcResult, InputField, fmt, unit_option, option_key


class SeedRateCalc(Calculator):
    id = "agri_seed"
    name = "Seed Rate"
    category = "Agriculture"
    description = "Seed required per acre/hectare"
    icon = "🌱"
    example = "100 kg/ha × 2 ha = 200 kg"

    def get_inputs(self):
        return [
            InputField("rate", "Seed rate (kg per ha)", "number", 100),
            InputField("area", "Area (hectares)", "number", 2),
        ]

    def calculate(self, values):
        rate, area = self.num(values, "rate"), self.num(values, "area")
        total = rate * area
        return [
            CalcResult("Total seed required", f"{fmt(total, 2)} kg"),
            CalcResult("In bags (50kg)", f"{fmt(total / 50, 2)} bags"),
            CalcResult("Per acre equivalent", f"{fmt(rate * 0.404686, 2)} kg/acre"),
        ]


class FertilizerCalc(Calculator):
    id = "agri_fertilizer"
    name = "Fertilizer Requirement"
    category = "Agriculture"
    description = "Fertilizer needed based on NPK recommendation"
    icon = "🧪"
    example = "20-10-10 for 1 ha at 100 kg/ha"

    def get_inputs(self):
        return [
            InputField("area", "Area (ha)", "number", 1),
            InputField("n_rate", "N rate (kg/ha)", "number", 100),
            InputField("p_rate", "P₂O₅ rate (kg/ha)", "number", 50),
            InputField("k_rate", "K₂O rate (kg/ha)", "number", 50),
            InputField("npk", "Fertilizer grade (N-P-K)", "text", "20-10-10"),
        ]

    def calculate(self, values):
        area = self.num(values, "area")
        n_r = self.num(values, "n_rate")
        p_r = self.num(values, "p_rate")
        k_r = self.num(values, "k_rate")
        try:
            grade = [float(x) for x in str(values.get("npk", "20-10-10")).split("-")]
        except ValueError:
            raise ValueError("Enter grade like 20-10-10")
        if len(grade) != 3 or any(g <= 0 for g in grade):
            raise ValueError("Grade must have 3 positive numbers")
        n_fert = n_r / grade[0] * 100
        p_fert = p_r / grade[1] * 100
        k_fert = k_r / grade[2] * 100
        total = n_fert + p_fert + k_fert
        return [
            CalcResult(f"Urea-equivalent N fertilizer", f"{fmt(n_fert * area, 2)} kg"),
            CalcResult(f"P fertilizer", f"{fmt(p_fert * area, 2)} kg"),
            CalcResult(f"K fertilizer", f"{fmt(k_fert * area, 2)} kg"),
            CalcResult("Total fertilizer", f"{fmt(total * area, 2)} kg"),
        ]


class IrrigationCalc(Calculator):
    id = "agri_irrigation"
    name = "Irrigation Needs"
    category = "Agriculture"
    description = "Water required for a crop"
    icon = "💧"
    example = "1 ha, 5 mm/day → 50,000 L/day"

    def get_inputs(self):
        return [
            InputField("area", "Area (ha)", "number", 1),
            InputField("depth", "Water depth (mm/day)", "number", 5),
        ]

    def calculate(self, values):
        area = self.num(values, "area")
        depth = self.num(values, "depth")
        # 1 ha × 1 mm = 10,000 L
        litres = area * depth * 10000
        return [
            CalcResult("Daily water requirement", f"{fmt(litres, 0)} L"),
            CalcResult("In cubic meters", f"{fmt(litres / 1000, 2)} m³"),
            CalcResult("Pump time @10000 L/h", f"{fmt(litres / 10000, 2)} hours"),
        ]


class CropYieldCalc(Calculator):
    id = "agri_yield"
    name = "Crop Yield"
    category = "Agriculture"
    description = "Crop yield per hectare"
    icon = "🌾"
    example = "3000 kg from 0.5 ha = 6000 kg/ha"

    def get_inputs(self):
        return [
            InputField("produce", "Total produce (kg)", "number", 3000),
            InputField("area", "Area (ha)", "number", 0.5),
        ]

    def calculate(self, values):
        produce, area = self.num(values, "produce"), self.num(values, "area")
        if area == 0:
            raise ValueError("Area cannot be zero")
        yield_ha = produce / area
        return [
            CalcResult("Yield per hectare", f"{fmt(yield_ha, 2)} kg/ha"),
            CalcResult("Yield per acre", f"{fmt(yield_ha * 0.404686, 2)} kg/acre"),
            CalcResult("In quintals", f"{fmt(yield_ha / 100, 2)} q/ha"),
        ]


class LandAreaCalc(Calculator):
    id = "agri_land"
    name = "Land Area"
    category = "Agriculture"
    description = "Convert land area units"
    icon = "🗺️"
    example = "1 acre = 0.4047 ha = 4046.86 m²"

    def _options(self):
        return [
            unit_option("Acre", "4046.86 m²"),
            unit_option("Hectare", "10,000 m²"),
            unit_option("Square meter", "1 m²"),
            unit_option("Square feet", "0.092903 m²"),
            unit_option("Guntha", "101.171 m²"),
        ]

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From", "select", unit_option("Acre", "4046.86 m²"), options=self._options()),
            InputField("to", "To", "select", unit_option("Hectare", "10,000 m²"), options=self._options()),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = option_key(values.get("from", unit_option("Acre", "4046.86 m²")))
        t = option_key(values.get("to", unit_option("Hectare", "10,000 m²")))
        to_sqm = {"Acre": 4046.86, "Hectare": 10000, "Square meter": 1, "Square feet": 0.092903, "Guntha": 101.171}
        result = value * to_sqm[f] / to_sqm[t]
        return [CalcResult(f"{fmt(value)} {f} = {fmt(result, 4)} {t}", result)]


class LivestockFeedCalc(Calculator):
    id = "agri_livestock"
    name = "Livestock Feed"
    category = "Agriculture"
    description = "Daily feed requirement for livestock"
    icon = "🐄"
    example = "Cow 400 kg → 10 kg dry matter/day"

    def get_inputs(self):
        return [
            InputField("weight", "Animal weight (kg)", "number", 400),
            InputField("type", "Animal type", "select", "Cow", options=["Cow", "Buffalo", "Sheep", "Goat", "Horse"]),
        ]

    def calculate(self, values):
        w = self.num(values, "weight")
        animal = values.get("type", "Cow")
        pct = {"Cow": 0.025, "Buffalo": 0.03, "Sheep": 0.035, "Goat": 0.035, "Horse": 0.02}[animal]
        dm = w * pct
        green = dm * 0.6
        dry = dm * 0.4
        return [
            CalcResult("Dry matter intake", f"{fmt(dm, 1)} kg/day", f"{pct*100:g}% of body weight"),
            CalcResult("Green fodder (~60%)", f"{fmt(green, 1)} kg/day"),
            CalcResult("Dry fodder (~40%)", f"{fmt(dry, 1)} kg/day"),
            CalcResult("Monthly feed", f"{fmt(dm * 30, 1)} kg/month"),
        ]
