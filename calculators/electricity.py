"""Electricity calculators."""
import math
from .base import Calculator, CalcResult, InputField, fmt


class ResistanceCalc(Calculator):
    id = "elec_resistance"
    name = "Resistance"
    category = "Electricity"
    description = "R = V / I (Ohm's law)"
    icon = "🛡️"
    example = "12 V, 2 A → 6 Ω"

    def get_inputs(self):
        return [
            InputField("v", "Voltage (V)", "number", 12),
            InputField("i", "Current (A)", "number", 2),
        ]

    def calculate(self, values):
        v, i = self.num(values, "v"), self.num(values, "i")
        if i == 0:
            raise ValueError("Current cannot be zero")
        r = v / i
        p = v * i
        return [
            CalcResult("Resistance", f"{fmt(r, 4)} Ω", "R = V/I"),
            CalcResult("Power dissipated", f"{fmt(p, 4)} W", "P = V×I"),
        ]


class VoltageCalc(Calculator):
    id = "elec_voltage"
    name = "Voltage"
    category = "Electricity"
    description = "V = I × R (Ohm's law)"
    icon = "⚡"
    example = "2 A × 6 Ω = 12 V"

    def get_inputs(self):
        return [
            InputField("i", "Current (A)", "number", 2),
            InputField("r", "Resistance (Ω)", "number", 6),
        ]

    def calculate(self, values):
        i, r = self.num(values, "i"), self.num(values, "r")
        v = i * r
        p = v * i
        return [
            CalcResult("Voltage", f"{fmt(v, 4)} V", "V = I×R"),
            CalcResult("Power", f"{fmt(p, 4)} W", "P = V×I"),
        ]


class CurrentCalc(Calculator):
    id = "elec_current"
    name = "Current"
    category = "Electricity"
    description = "I = V / R (Ohm's law)"
    icon = "🔌"
    example = "12 V, 6 Ω → 2 A"

    def get_inputs(self):
        return [
            InputField("v", "Voltage (V)", "number", 12),
            InputField("r", "Resistance (Ω)", "number", 6),
        ]

    def calculate(self, values):
        v, r = self.num(values, "v"), self.num(values, "r")
        if r == 0:
            raise ValueError("Resistance cannot be zero")
        i = v / r
        return [
            CalcResult("Current", f"{fmt(i, 4)} A", "I = V/R"),
            CalcResult("In mA", f"{fmt(i * 1000, 2)} mA"),
        ]


class FrequencyCalc(Calculator):
    id = "elec_frequency"
    name = "Frequency"
    category = "Electricity"
    description = "f = 1 / T"
    icon = "〰️"
    example = "Period 0.02 s → 50 Hz"

    def get_inputs(self):
        return [
            InputField("t", "Period (seconds)", "number", 0.02),
        ]

    def calculate(self, values):
        t = self.num(values, "t")
        if t == 0:
            raise ValueError("Period cannot be zero")
        f = 1 / t
        return [
            CalcResult("Frequency", f"{fmt(f, 4)} Hz", "f = 1/T"),
            CalcResult("Angular frequency", f"{fmt(2 * math.pi * f, 4)} rad/s"),
        ]


class WavelengthCalc(Calculator):
    id = "elec_wavelength"
    name = "Wavelength"
    category = "Electricity"
    description = "λ = v / f"
    icon = "🌊"
    example = "Speed 343 m/s, 1000 Hz → 0.343 m"

    def get_inputs(self):
        return [
            InputField("v", "Wave speed (m/s)", "number", 343),
            InputField("f", "Frequency (Hz)", "number", 1000),
        ]

    def calculate(self, values):
        v, f = self.num(values, "v"), self.num(values, "f")
        if f == 0:
            raise ValueError("Frequency cannot be zero")
        lam = v / f
        return [
            CalcResult("Wavelength", f"{fmt(lam, 6)} m", "λ = v/f"),
            CalcResult("In cm", f"{fmt(lam * 100, 4)} cm"),
            CalcResult("In nm", f"{fmt(lam * 1e9, 2)} nm"),
        ]


class PowerCalcElectricity(Calculator):
    id = "elec_power"
    name = "Electrical Power"
    category = "Electricity"
    description = "P = V × I"
    icon = "💡"
    example = "12 V, 2 A → 24 W"

    def get_inputs(self):
        return [
            InputField("v", "Voltage (V)", "number", 12),
            InputField("i", "Current (A)", "number", 2),
        ]

    def calculate(self, values):
        v, i = self.num(values, "v"), self.num(values, "i")
        p = v * i
        r = v / i if i else 0
        return [
            CalcResult("Power", f"{fmt(p, 4)} W", "P = V×I"),
            CalcResult("Resistance", f"{fmt(r, 4)} Ω", "R = V/I"),
            CalcResult("Energy per hour", f"{fmt(p / 1000, 4)} kWh/h"),
        ]


class EnergyCalcElectricity(Calculator):
    id = "elec_energy"
    name = "Electrical Energy"
    category = "Electricity"
    description = "E = P × t"
    icon = "🔋"
    example = "100 W for 5 hours = 0.5 kWh"

    def get_inputs(self):
        return [
            InputField("p", "Power (W)", "number", 100),
            InputField("t", "Time (hours)", "number", 5),
        ]

    def calculate(self, values):
        p, t = self.num(values, "p"), self.num(values, "t")
        wh = p * t
        kwh = wh / 1000
        joules = wh * 3600
        return [
            CalcResult("Energy", f"{fmt(kwh, 4)} kWh", "P × t / 1000"),
            CalcResult("In watt-hours", f"{fmt(wh, 2)} Wh"),
            CalcResult("In joules", f"{fmt(joules, 2)} J"),
        ]


class PowerFactorCalc(Calculator):
    id = "elec_pf"
    name = "Power Factor"
    category = "Electricity"
    description = "Power factor = cos(phase angle)"
    icon = "📐"
    example = "Phase angle 30° → PF 0.866"

    def get_inputs(self):
        return [
            InputField("angle", "Phase angle (degrees)", "number", 30),
        ]

    def calculate(self, values):
        angle = self.num(values, "angle")
        pf = math.cos(math.radians(angle))
        return [
            CalcResult("Power factor", f"{fmt(pf, 4)}", "cos(φ)"),
            CalcResult("Reactive factor", f"{fmt(math.sin(math.radians(angle)), 4)}"),
        ]


class SeriesParallelResistanceCalc(Calculator):
    id = "elec_series_parallel"
    name = "Series / Parallel Resistance"
    category = "Electricity"
    description = "Equivalent resistance of resistors"
    icon = "🔗"
    example = "R1=10, R2=20 → series 30, parallel 6.67"

    def get_inputs(self):
        return [
            InputField("r1", "Resistor 1 (Ω)", "number", 10),
            InputField("r2", "Resistor 2 (Ω)", "number", 20),
        ]

    def calculate(self, values):
        r1, r2 = self.num(values, "r1"), self.num(values, "r2")
        series = r1 + r2
        parallel = (r1 * r2) / (r1 + r2) if (r1 + r2) else 0
        return [
            CalcResult("Series resistance", f"{fmt(series, 4)} Ω", "R₁ + R₂"),
            CalcResult("Parallel resistance", f"{fmt(parallel, 4)} Ω", "(R₁×R₂)/(R₁+R₂)"),
        ]


class WireGaugeCalc(Calculator):
    id = "elec_wire_gauge"
    name = "Wire Gauge"
    category = "Electricity"
    description = "Voltage drop in a wire"
    icon = "🧵"
    example = "10 A, 0.5 Ω → 5 V drop"

    def get_inputs(self):
        return [
            InputField("i", "Current (A)", "number", 10),
            InputField("r", "Wire resistance (Ω)", "number", 0.5),
        ]

    def calculate(self, values):
        i, r = self.num(values, "i"), self.num(values, "r")
        drop = i * r
        p_loss = drop * i
        return [
            CalcResult("Voltage drop", f"{fmt(drop, 4)} V", "V = I×R"),
            CalcResult("Power loss", f"{fmt(p_loss, 4)} W", "P = V×I"),
        ]
