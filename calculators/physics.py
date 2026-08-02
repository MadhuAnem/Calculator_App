"""Physics calculators."""
import math
from .base import Calculator, CalcResult, InputField, fmt


class MotionCalc(Calculator):
    id = "phys_motion"
    name = "Motion Equations"
    category = "Physics"
    description = "SUVAT — solve for final velocity given initial velocity, acceleration, time"
    icon = "🏃"
    example = "u=0, a=9.8, t=3 → v=29.4 m/s"

    def get_inputs(self):
        return [
            InputField("u", "Initial velocity u (m/s)", "number", 0),
            InputField("a", "Acceleration a (m/s²)", "number", 9.8),
            InputField("t", "Time t (s)", "number", 3),
        ]

    def calculate(self, values):
        u, a, t = self.num(values, "u"), self.num(values, "a"), self.num(values, "t")
        v = u + a * t
        s = u * t + 0.5 * a * t * t
        s2 = (v * v - u * u) / (2 * a) if a else 0
        return [
            CalcResult("Final velocity (v = u+at)", f"{fmt(v, 3)} m/s"),
            CalcResult("Displacement (s = ut+½at²)", f"{fmt(s, 3)} m"),
            CalcResult("Displacement (v²−u²=2as)", f"{fmt(s2, 3)} m"),
        ]


class ProjectileCalc(Calculator):
    id = "phys_projectile"
    name = "Projectile Motion"
    category = "Physics"
    description = "Range, max height, time of flight for a projectile"
    icon = "🎯"
    example = "50 m/s at 45° → range 254.8 m"

    def get_inputs(self):
        return [
            InputField("v", "Launch velocity (m/s)", "number", 50),
            InputField("theta", "Launch angle (degrees)", "number", 45),
        ]

    def calculate(self, values):
        v = self.num(values, "v")
        theta = math.radians(self.num(values, "theta"))
        g = 9.81
        rng = v * v * math.sin(2 * theta) / g
        hmax = v * v * math.sin(theta) ** 2 / (2 * g)
        tof = 2 * v * math.sin(theta) / g
        return [
            CalcResult("Range", f"{fmt(rng, 3)} m", "v²sin(2θ)/g"),
            CalcResult("Maximum height", f"{fmt(hmax, 3)} m", "v²sin²θ/(2g)"),
            CalcResult("Time of flight", f"{fmt(tof, 3)} s", "2v sinθ/g"),
        ]


class GravityCalc(Calculator):
    id = "phys_gravity"
    name = "Gravity"
    category = "Physics"
    description = "Force of gravity between two masses"
    icon = "🌍"
    example = "m1=100, m2=100, r=1 → 6.674e-7 N"

    def get_inputs(self):
        return [
            InputField("m1", "Mass 1 (kg)", "number", 100),
            InputField("m2", "Mass 2 (kg)", "number", 100),
            InputField("r", "Distance (m)", "number", 1),
        ]

    def calculate(self, values):
        m1, m2 = self.num(values, "m1"), self.num(values, "m2")
        r = self.num(values, "r")
        if r == 0:
            raise ValueError("Distance cannot be zero")
        G = 6.674e-11
        f = G * m1 * m2 / (r * r)
        return [
            CalcResult("Gravitational force", f"{fmt(f, 6)} N", "F = Gm₁m₂/r²"),
            CalcResult("Weight of m1", f"{fmt(m1 * 9.81, 3)} N"),
        ]


class MomentumCalc(Calculator):
    id = "phys_momentum"
    name = "Momentum"
    category = "Physics"
    description = "p = m × v"
    icon = "🎳"
    example = "10 kg at 5 m/s = 50 kg·m/s"

    def get_inputs(self):
        return [
            InputField("m", "Mass (kg)", "number", 10),
            InputField("v", "Velocity (m/s)", "number", 5),
        ]

    def calculate(self, values):
        m, v = self.num(values, "m"), self.num(values, "v")
        p = m * v
        ke = 0.5 * m * v * v
        return [
            CalcResult("Momentum", f"{fmt(p, 3)} kg·m/s", "p = m×v"),
            CalcResult("Kinetic energy", f"{fmt(ke, 3)} J", "KE = ½mv²"),
        ]


class KineticEnergyCalc(Calculator):
    id = "phys_ke"
    name = "Kinetic Energy"
    category = "Physics"
    description = "KE = ½ × m × v²"
    icon = "💨"
    example = "10 kg at 5 m/s = 125 J"

    def get_inputs(self):
        return [
            InputField("m", "Mass (kg)", "number", 10),
            InputField("v", "Velocity (m/s)", "number", 5),
        ]

    def calculate(self, values):
        m, v = self.num(values, "m"), self.num(values, "v")
        ke = 0.5 * m * v * v
        return [
            CalcResult("Kinetic energy", f"{fmt(ke, 3)} J", "KE = ½mv²"),
            CalcResult("Momentum", f"{fmt(m * v, 3)} kg·m/s"),
        ]


class PotentialEnergyCalc(Calculator):
    id = "phys_pe"
    name = "Potential Energy"
    category = "Physics"
    description = "PE = m × g × h"
    icon = "⛰️"
    example = "10 kg at 5 m = 490.5 J"

    def get_inputs(self):
        return [
            InputField("m", "Mass (kg)", "number", 10),
            InputField("h", "Height (m)", "number", 5),
        ]

    def calculate(self, values):
        m, h = self.num(values, "m"), self.num(values, "h")
        pe = m * 9.81 * h
        return [
            CalcResult("Gravitational PE", f"{fmt(pe, 3)} J", "PE = mgh"),
            CalcResult("Velocity if dropped (v=√(2gh))", f"{fmt(math.sqrt(2 * 9.81 * h), 3)} m/s"),
        ]
