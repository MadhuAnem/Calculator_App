"""Unit Conversion calculators."""
import math
from .base import Calculator, CalcResult, InputField, fmt, unit_option, option_key


class LengthConversionCalc(Calculator):
    id = "unit_length"
    name = "Length Conversion"
    category = "Unit Conversion"
    description = "Convert between length units"
    icon = "📏"
    example = "1 m = 100 cm = 3.28 ft"

    def _options(self):
        return [
            unit_option("Millimeter", "0.001 m"),
            unit_option("Centimeter", "0.01 m"),
            unit_option("Meter", "1 m"),
            unit_option("Kilometer", "1000 m"),
            unit_option("Inch", "0.0254 m"),
            unit_option("Foot", "0.3048 m"),
            unit_option("Yard", "0.9144 m"),
            unit_option("Mile", "1609.344 m"),
        ]

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From", "select", unit_option("Meter", "1 m"), options=self._options()),
            InputField("to", "To", "select", unit_option("Centimeter", "0.01 m"), options=self._options()),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = option_key(values.get("from", unit_option("Meter", "1 m")))
        t = option_key(values.get("to", unit_option("Centimeter", "0.01 m")))
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

    def _options(self):
        return [
            unit_option("Milligram", "0.000001 kg"),
            unit_option("Gram", "0.001 kg"),
            unit_option("Kilogram", "1 kg"),
            unit_option("Metric ton", "1000 kg"),
            unit_option("Ounce", "0.02835 kg"),
            unit_option("Pound", "0.45359 kg"),
            unit_option("Stone", "6.35029 kg"),
        ]

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From", "select", unit_option("Kilogram", "1 kg"), options=self._options()),
            InputField("to", "To", "select", unit_option("Pound", "0.45359 kg"), options=self._options()),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = option_key(values.get("from", unit_option("Kilogram", "1 kg")))
        t = option_key(values.get("to", unit_option("Pound", "0.45359 kg")))
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

    def _options(self):
        return [
            unit_option("Celsius", "°C (reference)"),
            unit_option("Fahrenheit", "°F = C×9/5+32"),
            unit_option("Kelvin", "K = C+273.15"),
        ]

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 100),
            InputField("from", "From", "select", unit_option("Celsius", "°C (reference)"), options=self._options()),
            InputField("to", "To", "select", unit_option("Fahrenheit", "°F = C×9/5+32"), options=self._options()),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = option_key(values.get("from", unit_option("Celsius", "°C (reference)")))
        t = option_key(values.get("to", unit_option("Fahrenheit", "°F = C×9/5+32")))
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

    def _options(self):
        return [
            unit_option("m/s", "1 m/s"),
            unit_option("km/h", "0.2778 m/s"),
            unit_option("mph", "0.44704 m/s"),
            unit_option("knots", "0.51444 m/s"),
        ]

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 100),
            InputField("from", "From", "select", unit_option("km/h", "0.2778 m/s"), options=self._options()),
            InputField("to", "To", "select", unit_option("mph", "0.44704 m/s"), options=self._options()),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = option_key(values.get("from", unit_option("km/h", "0.2778 m/s")))
        t = option_key(values.get("to", unit_option("mph", "0.44704 m/s")))
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

    def _options(self):
        return [
            unit_option("Square meter", "1 m²"),
            unit_option("Square kilometer", "1,000,000 m²"),
            unit_option("Square foot", "0.092903 m²"),
            unit_option("Square yard", "0.836127 m²"),
            unit_option("Acre", "4046.86 m²"),
            unit_option("Hectare", "10,000 m²"),
        ]

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From", "select", unit_option("Acre", "4046.86 m²"), options=self._options()),
            InputField("to", "To", "select", unit_option("Square meter", "1 m²"), options=self._options()),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = option_key(values.get("from", unit_option("Acre", "4046.86 m²")))
        t = option_key(values.get("to", unit_option("Square meter", "1 m²")))
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

    def _options(self):
        return [
            unit_option("Milliliter", "0.001 L"),
            unit_option("Liter", "1 L"),
            unit_option("Cubic meter", "1000 L"),
            unit_option("Teaspoon", "0.004929 L"),
            unit_option("Tablespoon", "0.014787 L"),
            unit_option("Fluid ounce", "0.029574 L"),
            unit_option("Cup", "0.236588 L"),
            unit_option("Pint", "0.473176 L"),
            unit_option("Quart", "0.946353 L"),
            unit_option("Gallon", "3.78541 L"),
        ]

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From", "select", unit_option("Liter", "1 L"), options=self._options()),
            InputField("to", "To", "select", unit_option("Fluid ounce", "0.029574 L"), options=self._options()),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = option_key(values.get("from", unit_option("Liter", "1 L")))
        t = option_key(values.get("to", unit_option("Fluid ounce", "0.029574 L")))
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

    def _options(self):
        return [
            unit_option("Pascal", "1 Pa"),
            unit_option("kPa", "1000 Pa"),
            unit_option("Bar", "100,000 Pa"),
            unit_option("Atmosphere", "101,325 Pa"),
            unit_option("psi", "6894.76 Pa"),
            unit_option("mmHg", "133.322 Pa"),
        ]

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From", "select", unit_option("Atmosphere", "101,325 Pa"), options=self._options()),
            InputField("to", "To", "select", unit_option("kPa", "1000 Pa"), options=self._options()),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = option_key(values.get("from", unit_option("Atmosphere", "101,325 Pa")))
        t = option_key(values.get("to", unit_option("kPa", "1000 Pa")))
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

    def _options(self):
        return [
            unit_option("Joule", "1 J"),
            unit_option("Kilojoule", "1000 J"),
            unit_option("Calorie", "4.184 J"),
            unit_option("kWh", "3,600,000 J"),
            unit_option("BTU", "1055.06 J"),
        ]

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From", "select", unit_option("kWh", "3,600,000 J"), options=self._options()),
            InputField("to", "To", "select", unit_option("Joule", "1 J"), options=self._options()),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = option_key(values.get("from", unit_option("kWh", "3,600,000 J")))
        t = option_key(values.get("to", unit_option("Joule", "1 J")))
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

    def _options(self):
        return [
            unit_option("Watt", "1 W"),
            unit_option("kW", "1000 W"),
            unit_option("MW", "1,000,000 W"),
            unit_option("Horsepower", "745.7 W"),
        ]

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From", "select", unit_option("Horsepower", "745.7 W"), options=self._options()),
            InputField("to", "To", "select", unit_option("Watt", "1 W"), options=self._options()),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = option_key(values.get("from", unit_option("Horsepower", "745.7 W")))
        t = option_key(values.get("to", unit_option("Watt", "1 W")))
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

    def _options(self):
        return [
            unit_option("L/100km", "litres per 100 km"),
            unit_option("km/L", "km per litre"),
            unit_option("mpg (US)", "miles per US gallon"),
        ]

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 10),
            InputField("from", "From", "select", unit_option("L/100km", "litres per 100 km"), options=self._options()),
            InputField("to", "To", "select", unit_option("mpg (US)", "miles per US gallon"), options=self._options()),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = option_key(values.get("from", unit_option("L/100km", "litres per 100 km")))
        t = option_key(values.get("to", unit_option("mpg (US)", "miles per US gallon")))
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

    def _options(self):
        return [
            unit_option("Bit", "0.125 byte"),
            unit_option("Byte", "1 byte"),
            unit_option("KB", "1024 bytes"),
            unit_option("MB", "1,048,576 bytes"),
            unit_option("GB", "1,073,741,824 bytes"),
            unit_option("TB", "1,099,511,627,776 bytes"),
        ]

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From", "select", unit_option("GB", "1,073,741,824 bytes"), options=self._options()),
            InputField("to", "To", "select", unit_option("MB", "1,048,576 bytes"), options=self._options()),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = option_key(values.get("from", unit_option("GB", "1,073,741,824 bytes")))
        t = option_key(values.get("to", unit_option("MB", "1,048,576 bytes")))
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

    def _options(self):
        return [
            unit_option("Second", "1 s"),
            unit_option("Minute", "60 s"),
            unit_option("Hour", "3600 s"),
            unit_option("Day", "86,400 s"),
            unit_option("Week", "604,800 s"),
            unit_option("Year", "31,536,000 s"),
        ]

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From", "select", unit_option("Day", "86,400 s"), options=self._options()),
            InputField("to", "To", "select", unit_option("Hour", "3600 s"), options=self._options()),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = option_key(values.get("from", unit_option("Day", "86,400 s")))
        t = option_key(values.get("to", unit_option("Hour", "3600 s")))
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

    def _options(self):
        return [
            unit_option("Degrees", "1° (reference)"),
            unit_option("Radians", "57.2958°"),
            unit_option("Gradians", "0.9°"),
        ]

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 180),
            InputField("from", "From", "select", unit_option("Degrees", "1° (reference)"), options=self._options()),
            InputField("to", "To", "select", unit_option("Radians", "57.2958°"), options=self._options()),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = option_key(values.get("from", unit_option("Degrees", "1° (reference)")))
        t = option_key(values.get("to", unit_option("Radians", "57.2958°")))
        to_deg = {"Degrees": 1, "Radians": 180 / math.pi, "Gradians": 0.9}
        result = value * to_deg[f] / to_deg[t]
        return [CalcResult(f"{fmt(value)} {f} = {fmt(result, 6)} {t}", result)]

