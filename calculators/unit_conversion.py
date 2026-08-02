"""Unit Conversion calculators."""
import math
from .base import Calculator, CalcResult, InputField, fmt


class LengthConversionCalc(Calculator):
    id = "unit_length"
    name = "Length Conversion"
    category = "Unit Conversion"
    description = "Convert between length units"
    icon = "📏"
    example = "1 m = 100 cm = 3.28 ft"

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From", "select", "Meter", options=[
                "Millimeter", "Centimeter", "Meter", "Kilometer", "Inch", "Foot", "Yard", "Mile",
            ]),
            InputField("to", "To", "select", "Centimeter", options=[
                "Millimeter", "Centimeter", "Meter", "Kilometer", "Inch", "Foot", "Yard", "Mile",
            ]),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = values.get("from", "Meter")
        t = values.get("to", "Centimeter")
        to_m = {
            "Millimeter": 0.001, "Centimeter": 0.01, "Meter": 1, "Kilometer": 1000,
            "Inch": 0.0254, "Foot": 0.3048, "Yard": 0.9144, "Mile": 1609.344,
        }
        result = value * to_m[f] / to_m[t]
        return [CalcResult(f"{fmt(value)} {f} = {fmt(result, 6)} {t}", result)]


class WeightConversionCalc(Calculator):
    id = "unit_weight"
    name = "Weight Conversion"
    category = "Unit Conversion"
    description = "Convert between weight/mass units"
    icon = "⚖️"
    example = "1 kg = 2.2046 lb"

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From", "select", "Kilogram", options=[
                "Milligram", "Gram", "Kilogram", "Metric ton", "Ounce", "Pound", "Stone",
            ]),
            InputField("to", "To", "select", "Pound", options=[
                "Milligram", "Gram", "Kilogram", "Metric ton", "Ounce", "Pound", "Stone",
            ]),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = values.get("from", "Kilogram")
        t = values.get("to", "Pound")
        to_kg = {
            "Milligram": 1e-6, "Gram": 0.001, "Kilogram": 1, "Metric ton": 1000,
            "Ounce": 0.0283495, "Pound": 0.453592, "Stone": 6.35029,
        }
        result = value * to_kg[f] / to_kg[t]
        return [CalcResult(f"{fmt(value)} {f} = {fmt(result, 6)} {t}", result)]


class TemperatureConversionCalc(Calculator):
    id = "unit_temp"
    name = "Temperature Conversion"
    category = "Unit Conversion"
    description = "Convert between °C, °F, K"
    icon = "🌡️"
    example = "100°C = 212°F = 373.15 K"

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 100),
            InputField("from", "From", "select", "Celsius", options=["Celsius", "Fahrenheit", "Kelvin"]),
            InputField("to", "To", "select", "Fahrenheit", options=["Celsius", "Fahrenheit", "Kelvin"]),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = values.get("from", "Celsius")
        t = values.get("to", "Fahrenheit")
        # to Celsius first
        if f == "Celsius":
            c = value
        elif f == "Fahrenheit":
            c = (value - 32) * 5 / 9
        else:
            c = value - 273.15
        if t == "Celsius":
            result = c
        elif t == "Fahrenheit":
            result = c * 9 / 5 + 32
        else:
            result = c + 273.15
        return [CalcResult(f"{fmt(value)}° {f} = {fmt(result, 4)}° {t}", result)]


class SpeedConversionCalc(Calculator):
    id = "unit_speed"
    name = "Speed Conversion"
    category = "Unit Conversion"
    description = "Convert between speed units"
    icon = "🚗"
    example = "100 km/h = 62.1 mph"

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 100),
            InputField("from", "From", "select", "km/h", options=["m/s", "km/h", "mph", "knots"]),
            InputField("to", "To", "select", "mph", options=["m/s", "km/h", "mph", "knots"]),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = values.get("from", "km/h")
        t = values.get("to", "mph")
        to_ms = {"m/s": 1, "km/h": 1 / 3.6, "mph": 0.44704, "knots": 0.514444}
        result = value * to_ms[f] / to_ms[t]
        return [CalcResult(f"{fmt(value)} {f} = {fmt(result, 4)} {t}", result)]


class AreaConversionCalc(Calculator):
    id = "unit_area"
    name = "Area Conversion"
    category = "Unit Conversion"
    description = "Convert between area units"
    icon = "📐"
    example = "1 acre = 4046.86 m²"

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From", "select", "Acre", options=[
                "Square meter", "Square kilometer", "Square foot", "Square yard", "Acre", "Hectare",
            ]),
            InputField("to", "To", "select", "Square meter", options=[
                "Square meter", "Square kilometer", "Square foot", "Square yard", "Acre", "Hectare",
            ]),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = values.get("from", "Acre")
        t = values.get("to", "Square meter")
        to_sqm = {
            "Square meter": 1, "Square kilometer": 1e6, "Square foot": 0.092903,
            "Square yard": 0.836127, "Acre": 4046.86, "Hectare": 10000,
        }
        result = value * to_sqm[f] / to_sqm[t]
        return [CalcResult(f"{fmt(value)} {f} = {fmt(result, 6)} {t}", result)]


class VolumeConversionCalc(Calculator):
    id = "unit_volume"
    name = "Volume Conversion"
    category = "Unit Conversion"
    description = "Convert between volume units"
    icon = "🧪"
    example = "1 L = 33.8 fl oz"

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From", "select", "Liter", options=[
                "Milliliter", "Liter", "Cubic meter", "Teaspoon", "Tablespoon", "Fluid ounce", "Cup", "Pint", "Quart", "Gallon",
            ]),
            InputField("to", "To", "select", "Fluid ounce", options=[
                "Milliliter", "Liter", "Cubic meter", "Teaspoon", "Tablespoon", "Fluid ounce", "Cup", "Pint", "Quart", "Gallon",
            ]),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = values.get("from", "Liter")
        t = values.get("to", "Fluid ounce")
        to_l = {
            "Milliliter": 0.001, "Liter": 1, "Cubic meter": 1000,
            "Teaspoon": 0.00492892, "Tablespoon": 0.0147868, "Fluid ounce": 0.0295735,
            "Cup": 0.236588, "Pint": 0.473176, "Quart": 0.946353, "Gallon": 3.78541,
        }
        result = value * to_l[f] / to_l[t]
        return [CalcResult(f"{fmt(value)} {f} = {fmt(result, 6)} {t}", result)]


class PressureConversionCalc(Calculator):
    id = "unit_pressure"
    name = "Pressure Conversion"
    category = "Unit Conversion"
    description = "Convert between pressure units"
    icon = "🌀"
    example = "1 atm = 101.325 kPa"

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From", "select", "Atmosphere", options=["Pascal", "kPa", "Bar", "Atmosphere", "psi", "mmHg"]),
            InputField("to", "To", "select", "kPa", options=["Pascal", "kPa", "Bar", "Atmosphere", "psi", "mmHg"]),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = values.get("from", "Atmosphere")
        t = values.get("to", "kPa")
        to_pa = {
            "Pascal": 1, "kPa": 1000, "Bar": 100000,
            "Atmosphere": 101325, "psi": 6894.76, "mmHg": 133.322,
        }
        result = value * to_pa[f] / to_pa[t]
        return [CalcResult(f"{fmt(value)} {f} = {fmt(result, 6)} {t}", result)]


class EnergyConversionCalc(Calculator):
    id = "unit_energy"
    name = "Energy Conversion"
    category = "Unit Conversion"
    description = "Convert between energy units"
    icon = "⚡"
    example = "1 kWh = 3.6 MJ"

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From", "select", "kWh", options=["Joule", "Kilojoule", "Calorie", "kWh", "BTU"]),
            InputField("to", "To", "select", "Joule", options=["Joule", "Kilojoule", "Calorie", "kWh", "BTU"]),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = values.get("from", "kWh")
        t = values.get("to", "Joule")
        to_j = {
            "Joule": 1, "Kilojoule": 1000, "Calorie": 4.184, "kWh": 3.6e6, "BTU": 1055.06,
        }
        result = value * to_j[f] / to_j[t]
        return [CalcResult(f"{fmt(value)} {f} = {fmt(result, 6)} {t}", result)]


class PowerConversionCalc(Calculator):
    id = "unit_power"
    name = "Power Conversion"
    category = "Unit Conversion"
    description = "Convert between power units"
    icon = "🔌"
    example = "1 hp = 745.7 W"

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From", "select", "Horsepower", options=["Watt", "kW", "MW", "Horsepower"]),
            InputField("to", "To", "select", "Watt", options=["Watt", "kW", "MW", "Horsepower"]),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = values.get("from", "Horsepower")
        t = values.get("to", "Watt")
        to_w = {"Watt": 1, "kW": 1000, "MW": 1e6, "Horsepower": 745.7}
        result = value * to_w[f] / to_w[t]
        return [CalcResult(f"{fmt(value)} {f} = {fmt(result, 6)} {t}", result)]


class FuelEconomyCalc(Calculator):
    id = "unit_fuel_economy"
    name = "Fuel Economy"
    category = "Unit Conversion"
    description = "Convert fuel economy units"
    icon = "⛽"
    example = "10 L/100km = 23.5 mpg"

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 10),
            InputField("from", "From", "select", "L/100km", options=["L/100km", "km/L", "mpg (US)"]),
            InputField("to", "To", "select", "mpg (US)", options=["L/100km", "km/L", "mpg (US)"]),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = values.get("from", "L/100km")
        t = values.get("to", "mpg (US)")
        if f == "L/100km":
            lp100 = value
        elif f == "km/L":
            lp100 = 100 / value if value else 0
        else:
            lp100 = 235.215 / value if value else 0
        if t == "L/100km":
            result = lp100
        elif t == "km/L":
            result = 100 / lp100 if lp100 else 0
        else:
            result = 235.215 / lp100 if lp100 else 0
        return [CalcResult(f"{fmt(value)} {f} = {fmt(result, 4)} {t}", result)]


class DataStorageConversionCalc(Calculator):
    id = "unit_data_storage"
    name = "Data Storage"
    category = "Unit Conversion"
    description = "Convert data storage units"
    icon = "💽"
    example = "1 GB = 1024 MB"

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From", "select", "GB", options=["Bit", "Byte", "KB", "MB", "GB", "TB"]),
            InputField("to", "To", "select", "MB", options=["Bit", "Byte", "KB", "MB", "GB", "TB"]),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = values.get("from", "GB")
        t = values.get("to", "MB")
        units = {"Bit": 1 / 8, "Byte": 1, "KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3, "TB": 1024 ** 4}
        result = value * units[f] / units[t]
        return [CalcResult(f"{fmt(value)} {f} = {fmt(result, 6)} {t}", result)]


class TimeConversionCalc(Calculator):
    id = "unit_time"
    name = "Time Conversion"
    category = "Unit Conversion"
    description = "Convert between time units"
    icon = "⏱️"
    example = "1 day = 24 h = 1440 min"

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From", "select", "Day", options=["Second", "Minute", "Hour", "Day", "Week", "Year"]),
            InputField("to", "To", "select", "Hour", options=["Second", "Minute", "Hour", "Day", "Week", "Year"]),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = values.get("from", "Day")
        t = values.get("to", "Hour")
        to_s = {"Second": 1, "Minute": 60, "Hour": 3600, "Day": 86400, "Week": 604800, "Year": 31536000}
        result = value * to_s[f] / to_s[t]
        return [CalcResult(f"{fmt(value)} {f} = {fmt(result, 6)} {t}", result)]


class AngleConversionCalc(Calculator):
    id = "unit_angle"
    name = "Angle Conversion"
    category = "Unit Conversion"
    description = "Convert between angle units"
    icon = "📐"
    example = "180° = π rad"

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 180),
            InputField("from", "From", "select", "Degrees", options=["Degrees", "Radians", "Gradians"]),
            InputField("to", "To", "select", "Radians", options=["Degrees", "Radians", "Gradians"]),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = values.get("from", "Degrees")
        t = values.get("to", "Radians")
        to_deg = {"Degrees": 1, "Radians": 180 / math.pi, "Gradians": 0.9}
        result = value * to_deg[f] / to_deg[t]
        return [CalcResult(f"{fmt(value)} {f} = {fmt(result, 6)} {t}", result)]
