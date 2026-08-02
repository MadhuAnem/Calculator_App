"""Household calculators."""
import math
from .base import Calculator, CalcResult, InputField, fmt, money


class ElectricityBillCalc(Calculator):
    id = "house_electricity"
    name = "Electricity Bill"
    category = "Household"
    description = "Estimate electricity cost from usage"
    icon = "💡"
    example = "300 kWh at $0.15 = $45"

    def get_inputs(self):
        return [
            InputField("kwh", "Electricity used (kWh)", "number", 300),
            InputField("rate", "Rate per kWh", "number", 0.15),
            InputField("fixed", "Fixed charges", "number", 0, required=False),
        ]

    def calculate(self, values):
        kwh, rate = self.num(values, "kwh"), self.num(values, "rate")
        fixed = self.num(values, "fixed")
        energy = kwh * rate
        total = energy + fixed
        return [
            CalcResult("Energy charge", money(energy)),
            CalcResult("Fixed charges", money(fixed)),
            CalcResult("Total bill", money(total)),
            CalcResult("Average per day (30d)", money(total / 30)),
        ]


class WaterBillCalc(Calculator):
    id = "house_water"
    name = "Water Bill"
    category = "Household"
    description = "Water usage cost"
    icon = "🚰"
    example = "20,000 L at $0.002/L = $40"

    def get_inputs(self):
        return [
            InputField("litres", "Water used (litres)", "number", 20000),
            InputField("rate", "Rate per 1000 L", "number", 2),
        ]

    def calculate(self, values):
        litres, rate = self.num(values, "litres"), self.num(values, "rate")
        units = litres / 1000
        cost = units * rate
        return [
            CalcResult("Units (kL)", f"{fmt(units, 2)} kL"),
            CalcResult("Water bill", money(cost)),
        ]


class GasConsumptionCalc(Calculator):
    id = "house_gas"
    name = "Gas Consumption"
    category = "Household"
    description = "Gas cylinder/appliance usage cost"
    icon = "🔥"
    example = "10 kg at $1.2/kg = $12"

    def get_inputs(self):
        return [
            InputField("kg", "Gas used (kg)", "number", 10),
            InputField("rate", "Rate per kg", "number", 1.2),
        ]

    def calculate(self, values):
        kg, rate = self.num(values, "kg"), self.num(values, "rate")
        cost = kg * rate
        return [
            CalcResult("Gas cost", money(cost)),
            CalcResult("Days of usage (0.5 kg/day)", f"{fmt(kg / 0.5, 0)} days"),
        ]


class CookingMeasurementsCalc(Calculator):
    id = "house_cooking_measure"
    name = "Cooking Measurements"
    category = "Household"
    description = "Convert cooking measurement units"
    icon = "🥄"
    example = "1 cup = 16 tablespoons = 48 teaspoons"

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From", "select", "Cup", options=[
                "Teaspoon", "Tablespoon", "Fluid ounce", "Cup", "Pint", "Quart", "Milliliter",
            ]),
            InputField("to", "To", "select", "Tablespoon", options=[
                "Teaspoon", "Tablespoon", "Fluid ounce", "Cup", "Pint", "Quart", "Milliliter",
            ]),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = values.get("from", "Cup")
        t = values.get("to", "Tablespoon")
        to_ml = {
            "Teaspoon": 4.92892, "Tablespoon": 14.7868, "Fluid ounce": 29.5735,
            "Cup": 236.588, "Pint": 473.176, "Quart": 946.353, "Milliliter": 1,
        }
        result = value * to_ml[f] / to_ml[t]
        return [CalcResult(f"{fmt(value)} {f} = {fmt(result, 4)} {t}", result)]


class RecipeScalingCalc(Calculator):
    id = "house_recipe"
    name = "Recipe Scaling"
    category = "Household"
    description = "Scale recipe ingredients"
    icon = "🍲"
    example = "Recipe for 4 → 6 servings = ×1.5"

    def get_inputs(self):
        return [
            InputField("servings", "Original servings", "number", 4),
            InputField("target", "Desired servings", "number", 6),
            InputField("ingredients", "Ingredient amounts (comma sep.)", "text", "2,1.5,0.5"),
        ]

    def calculate(self, values):
        orig, target = self.num(values, "servings"), self.num(values, "target")
        if orig <= 0:
            raise ValueError("Original servings must be positive")
        factor = target / orig
        try:
            amounts = [float(x.strip()) for x in str(values.get("ingredients", "")).split(",") if x.strip()]
        except ValueError:
            raise ValueError("Enter valid amounts separated by commas")
        if not amounts:
            raise ValueError("Enter ingredient amounts")
        scaled = [a * factor for a in amounts]
        return [
            CalcResult("Scale factor", f"{fmt(factor, 3)}×", "target ÷ original"),
            CalcResult("Scaled amounts", ", ".join(fmt(a, 2) for a in scaled)),
            CalcResult("Original amounts", ", ".join(fmt(a, 2) for a in amounts)),
        ]


class RoomAreaCalc(Calculator):
    id = "house_room_area"
    name = "Room Area"
    category = "Household"
    description = "Area and paint/tile estimates for a room"
    icon = "🛋️"
    example = "4×5 m room = 20 m²"

    def get_inputs(self):
        return [
            InputField("length", "Length (m)", "number", 4),
            InputField("width", "Width (m)", "number", 5),
        ]

    def calculate(self, values):
        l, w = self.num(values, "length"), self.num(values, "width")
        area = l * w
        perimeter = 2 * (l + w)
        return [
            CalcResult("Room area", f"{fmt(area, 2)} m²"),
            CalcResult("In square feet", f"{fmt(area * 10.7639, 2)} ft²"),
            CalcResult("Perimeter", f"{fmt(perimeter, 2)} m"),
            CalcResult("Flooring cost @$10/m²", money(area * 10)),
        ]


class ACCapacityCalc(Calculator):
    id = "house_ac"
    name = "AC Capacity"
    category = "Household"
    description = "Recommended AC cooling capacity (BTU)"
    icon = "❄️"
    example = "20 m² room → ~10000 BTU / 1 ton"

    def get_inputs(self):
        return [
            InputField("area", "Room area (m²)", "number", 20),
            InputField("people", "People normally in room", "number", 2, required=False),
            InputField("sunny", "Sunny exposure?", "select", "No", options=["Yes", "No"]),
        ]

    def calculate(self, values):
        area = self.num(values, "area")
        people = self.num(values, "people")
        sunny = 1.1 if values.get("sunny", "No") == "Yes" else 1.0
        base = area * 500  # BTU per m²
        person_heat = (max(people - 1, 0)) * 600
        btu = (base + person_heat) * sunny
        tons = btu / 12000
        return [
            CalcResult("Cooling capacity", f"{fmt(btu, 0)} BTU/hr"),
            CalcResult("In tons (approx)", f"{fmt(tons, 2)} tons"),
            CalcResult("Recommended size", f"{round(tons * 2) / 2} tons (rounded)"),
        ]
