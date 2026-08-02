"""Engineering calculators."""
import math
from .base import Calculator, CalcResult, InputField, fmt


class AreaCalc(Calculator):
    id = "eng_area"
    name = "Area"
    category = "Engineering"
    description = "Area of common shapes"
    icon = "📐"
    example = "Rectangle 5×4 = 20"

    def get_inputs(self):
        return [
            InputField("shape", "Shape", "select", "Rectangle", options=[
                "Rectangle", "Square", "Triangle", "Circle", "Trapezoid", "Parallelogram", "Ellipse", "Ring",
            ]),
            InputField("a", "Dimension a", "number", 5),
            InputField("b", "Dimension b (if needed)", "number", 4, required=False),
            InputField("c", "Dimension c (if needed)", "number", 0, required=False),
        ]

    def calculate(self, values):
        shape = values.get("shape", "Rectangle")
        a, b, c = self.num(values, "a"), self.num(values, "b"), self.num(values, "c")
        formulas = {
            "Rectangle": lambda: a * b,
            "Square": lambda: a * a,
            "Triangle": lambda: 0.5 * a * b,
            "Circle": lambda: math.pi * a * a,
            "Trapezoid": lambda: 0.5 * (a + b) * c,
            "Parallelogram": lambda: a * b,
            "Ellipse": lambda: math.pi * a * b,
            "Ring": lambda: math.pi * (a * a - b * b),
        }
        area = formulas[shape]()
        return [
            CalcResult("Area", f"{fmt(area, 4)}", f"{shape} formula"),
            CalcResult("Bounding square units", f"{fmt(math.sqrt(area), 4)} × {fmt(math.sqrt(area), 4)}"),
        ]


class PerimeterCalc(Calculator):
    id = "eng_perimeter"
    name = "Perimeter"
    category = "Engineering"
    description = "Perimeter of common shapes"
    icon = "➰"
    example = "Rectangle 5×4 → 18"

    def get_inputs(self):
        return [
            InputField("shape", "Shape", "select", "Rectangle", options=[
                "Rectangle", "Square", "Triangle", "Circle", "Trapezoid", "Parallelogram", "Ellipse",
            ]),
            InputField("a", "Dimension a", "number", 5),
            InputField("b", "Dimension b (if needed)", "number", 4, required=False),
            InputField("c", "Dimension c (if needed)", "number", 3, required=False),
            InputField("d", "Dimension d (if needed)", "number", 3, required=False),
        ]

    def calculate(self, values):
        shape = values.get("shape", "Rectangle")
        a, b, c, d = (self.num(values, k) for k in ("a", "b", "c", "d"))
        formulas = {
            "Rectangle": lambda: 2 * (a + b),
            "Square": lambda: 4 * a,
            "Triangle": lambda: a + b + c,
            "Circle": lambda: 2 * math.pi * a,
            "Trapezoid": lambda: a + b + c + d,
            "Parallelogram": lambda: 2 * (a + b),
            "Ellipse": lambda: math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b))),
        }
        p = formulas[shape]()
        return [CalcResult("Perimeter", f"{fmt(p, 4)}", f"{shape} formula")]


class VolumeCalc(Calculator):
    id = "eng_volume"
    name = "Volume"
    category = "Engineering"
    description = "Volume of 3D solids"
    icon = "🧊"
    example = "Cube 3×3×3 = 27"

    def get_inputs(self):
        return [
            InputField("shape", "Shape", "select", "Cube", options=[
                "Cube", "Cuboid", "Cylinder", "Cone", "Sphere", "Hemisphere", "Pyramid", "Torus", "Prism",
            ]),
            InputField("a", "Dimension a", "number", 3),
            InputField("b", "Dimension b (if needed)", "number", 4, required=False),
            InputField("c", "Height (if needed)", "number", 5, required=False),
        ]

    def calculate(self, values):
        shape = values.get("shape", "Cube")
        a, b, c = self.num(values, "a"), self.num(values, "b"), self.num(values, "c")
        formulas = {
            "Cube": lambda: a ** 3,
            "Cuboid": lambda: a * b * c,
            "Cylinder": lambda: math.pi * a * a * c,
            "Cone": lambda: math.pi * a * a * c / 3,
            "Sphere": lambda: 4 * math.pi * a ** 3 / 3,
            "Hemisphere": lambda: 2 * math.pi * a ** 3 / 3,
            "Pyramid": lambda: a * b * c / 3,
            "Torus": lambda: 2 * math.pi * math.pi * a * b * b,
            "Prism": lambda: 0.5 * a * b * c,
        }
        vol = formulas[shape]()
        return [
            CalcResult("Volume", f"{fmt(vol, 4)}", f"{shape} formula"),
            CalcResult("Surface area look-up", "see Surface Area calculator"),
        ]


class SurfaceAreaCalc(Calculator):
    id = "eng_surf_area"
    name = "Surface Area"
    category = "Engineering"
    description = "Surface area of 3D solids"
    icon = "🎯"
    example = "Cube 3×3×3 = 54"

    def get_inputs(self):
        return [
            InputField("shape", "Shape", "select", "Cube", options=[
                "Cube", "Cuboid", "Cylinder", "Cone", "Sphere", "Hemisphere",
            ]),
            InputField("a", "Dimension a", "number", 3),
            InputField("b", "Dimension b (if needed)", "number", 4, required=False),
            InputField("c", "Height (if needed)", "number", 5, required=False),
        ]

    def calculate(self, values):
        shape = values.get("shape", "Cube")
        a, b, c = self.num(values, "a"), self.num(values, "b"), self.num(values, "c")
        formulas = {
            "Cube": lambda: 6 * a * a,
            "Cuboid": lambda: 2 * (a * b + b * c + a * c),
            "Cylinder": lambda: 2 * math.pi * a * (a + c),
            "Cone": lambda: math.pi * a * (a + math.sqrt(a * a + c * c)),
            "Sphere": lambda: 4 * math.pi * a * a,
            "Hemisphere": lambda: 3 * math.pi * a * a,
        }
        sa = formulas[shape]()
        return [CalcResult("Surface area", f"{fmt(sa, 4)}", f"{shape} formula")]


class ForceCalc(Calculator):
    id = "eng_force"
    name = "Force"
    category = "Engineering"
    description = "F = m × a"
    icon = "💪"
    example = "10 kg × 2 m/s² = 20 N"

    def get_inputs(self):
        return [
            InputField("m", "Mass (kg)", "number", 10),
            InputField("a", "Acceleration (m/s²)", "number", 2),
        ]

    def calculate(self, values):
        m, a = self.num(values, "m"), self.num(values, "a")
        f = m * a
        g = m * 9.81
        return [
            CalcResult("Force", f"{fmt(f, 3)} N", "F = m × a"),
            CalcResult("Force due to gravity", f"{fmt(g, 3)} N", "m × 9.81"),
            CalcResult("Weight", f"{fmt(g, 3)} N"),
        ]


class PressureCalc(Calculator):
    id = "eng_pressure"
    name = "Pressure"
    category = "Engineering"
    description = "P = F / A"
    icon = "🌀"
    example = "100 N on 2 m² = 50 Pa"

    def get_inputs(self):
        return [
            InputField("f", "Force (N)", "number", 100),
            InputField("a", "Area (m²)", "number", 2),
        ]

    def calculate(self, values):
        f, a = self.num(values, "f"), self.num(values, "a")
        if a == 0:
            raise ValueError("Area cannot be zero")
        p = f / a
        return [
            CalcResult("Pressure", f"{fmt(p, 4)} Pa", "P = F/A"),
            CalcResult("In kPa", f"{fmt(p / 1000, 4)} kPa"),
            CalcResult("In bar", f"{fmt(p / 100000, 6)} bar"),
            CalcResult("In psi", f"{fmt(p * 0.000145038, 6)} psi"),
        ]


class TorqueCalc(Calculator):
    id = "eng_torque"
    name = "Torque"
    category = "Engineering"
    description = "τ = F × r × sin(θ)"
    icon = "🔧"
    example = "50 N at 0.3 m at 90° = 15 N·m"

    def get_inputs(self):
        return [
            InputField("f", "Force (N)", "number", 50),
            InputField("r", "Lever arm (m)", "number", 0.3),
            InputField("theta", "Angle between (degrees)", "number", 90),
        ]

    def calculate(self, values):
        f, r = self.num(values, "f"), self.num(values, "r")
        theta = self.num(values, "theta")
        torque = f * r * math.sin(math.radians(theta))
        return [
            CalcResult("Torque", f"{fmt(torque, 4)} N·m", "τ = F × r × sin(θ)"),
            CalcResult("With angle 90°", f"{fmt(f * r, 4)} N·m"),
        ]


class VelocityCalc(Calculator):
    id = "eng_velocity"
    name = "Velocity"
    category = "Engineering"
    description = "v = d / t"
    icon = "🚀"
    example = "100 m in 10 s = 10 m/s"

    def get_inputs(self):
        return [
            InputField("d", "Distance (m)", "number", 100),
            InputField("t", "Time (s)", "number", 10),
        ]

    def calculate(self, values):
        d, t = self.num(values, "d"), self.num(values, "t")
        if t == 0:
            raise ValueError("Time cannot be zero")
        v = d / t
        return [
            CalcResult("Velocity", f"{fmt(v, 4)} m/s", "v = d/t"),
            CalcResult("In km/h", f"{fmt(v * 3.6, 4)} km/h"),
            CalcResult("In mph", f"{fmt(v * 2.23694, 4)} mph"),
        ]


class AccelerationCalc(Calculator):
    id = "eng_acceleration"
    name = "Acceleration"
    category = "Engineering"
    description = "a = (v-u) / t"
    icon = "📈"
    example = "0→20 m/s in 5 s = 4 m/s²"

    def get_inputs(self):
        return [
            InputField("vi", "Initial velocity (m/s)", "number", 0),
            InputField("vf", "Final velocity (m/s)", "number", 20),
            InputField("t", "Time (s)", "number", 5),
        ]

    def calculate(self, values):
        vi, vf, t = self.num(values, "vi"), self.num(values, "vf"), self.num(values, "t")
        if t == 0:
            raise ValueError("Time cannot be zero")
        a = (vf - vi) / t
        return [
            CalcResult("Acceleration", f"{fmt(a, 4)} m/s²", "a = (v₂−v₁)/t"),
            CalcResult("In g-force", f"{fmt(a / 9.81, 4)} g"),
        ]


class PowerCalc(Calculator):
    id = "eng_power"
    name = "Power"
    category = "Engineering"
    description = "P = W / t"
    icon = "⚡"
    example = "500 J in 10 s = 50 W"

    def get_inputs(self):
        return [
            InputField("w", "Work/Energy (J)", "number", 500),
            InputField("t", "Time (s)", "number", 10),
        ]

    def calculate(self, values):
        w, t = self.num(values, "w"), self.num(values, "t")
        if t == 0:
            raise ValueError("Time cannot be zero")
        p = w / t
        return [
            CalcResult("Power", f"{fmt(p, 4)} W", "P = W/t"),
            CalcResult("In kW", f"{fmt(p / 1000, 4)} kW"),
            CalcResult("In horsepower", f"{fmt(p / 745.7, 4)} hp"),
        ]


class EnergyCalc(Calculator):
    id = "eng_energy"
    name = "Energy / Work"
    category = "Engineering"
    description = "E = F × d"
    icon = "🔋"
    example = "50 N over 10 m = 500 J"

    def get_inputs(self):
        return [
            InputField("f", "Force (N)", "number", 50),
            InputField("d", "Distance (m)", "number", 10),
        ]

    def calculate(self, values):
        f, d = self.num(values, "f"), self.num(values, "d")
        e = f * d
        return [
            CalcResult("Energy / Work", f"{fmt(e, 4)} J", "E = F × d"),
            CalcResult("In kWh", f"{fmt(e / 3600000, 8)} kWh"),
            CalcResult("In calories", f"{fmt(e / 4.184, 4)} cal"),
        ]


class EfficiencyCalc(Calculator):
    id = "eng_efficiency"
    name = "Efficiency"
    category = "Engineering"
    description = "η = Output / Input × 100"
    icon = "⚙️"
    example = "Output 80 W, input 100 W → 80%"

    def get_inputs(self):
        return [
            InputField("out", "Useful output", "number", 80),
            InputField("inp", "Total input", "number", 100),
        ]

    def calculate(self, values):
        o, i = self.num(values, "out"), self.num(values, "inp")
        if i == 0:
            raise ValueError("Input cannot be zero")
        eff = o / i * 100
        loss = 100 - eff
        return [
            CalcResult("Efficiency", f"{fmt(eff, 4)}%", "η = output/input × 100"),
            CalcResult("Loss", f"{fmt(loss, 4)}%"),
        ]


class LoadCalc(Calculator):
    id = "eng_load"
    name = "Load / Capacity"
    category = "Engineering"
    description = "Safe load capacity with safety factor"
    icon = "🚚"
    example = "Rated 10000, SF 2 → safe load 5000"

    def get_inputs(self):
        return [
            InputField("rated", "Rated/ultimate capacity", "number", 10000),
            InputField("sf", "Safety factor", "number", 2),
        ]

    def calculate(self, values):
        rated, sf = self.num(values, "rated"), self.num(values, "sf")
        if sf <= 0:
            raise ValueError("Safety factor must be positive")
        safe = rated / sf
        return [
            CalcResult("Safe working load", f"{fmt(safe, 2)}", "Rated ÷ safety factor"),
            CalcResult("Design margin", f"{fmt((sf - 1) / sf * 100, 2)}%"),
        ]


class StressCalc(Calculator):
    id = "eng_stress"
    name = "Stress"
    category = "Engineering"
    description = "σ = F / A"
    icon = "🧱"
    example = "5000 N on 0.01 m² = 500 kPa"

    def get_inputs(self):
        return [
            InputField("f", "Force (N)", "number", 5000),
            InputField("a", "Cross-section area (m²)", "number", 0.01),
        ]

    def calculate(self, values):
        f, a = self.num(values, "f"), self.num(values, "a")
        if a == 0:
            raise ValueError("Area cannot be zero")
        stress = f / a
        return [
            CalcResult("Stress", f"{fmt(stress, 4)} Pa", "σ = F/A"),
            CalcResult("In MPa", f"{fmt(stress / 1e6, 6)} MPa"),
            CalcResult("In kPa", f"{fmt(stress / 1e3, 4)} kPa"),
        ]


class StrainCalc(Calculator):
    id = "eng_strain"
    name = "Strain"
    category = "Engineering"
    description = "ε = ΔL / L"
    icon = "🏹"
    example = "1 mm stretch over 1000 mm = 0.001"

    def get_inputs(self):
        return [
            InputField("dl", "Change in length", "number", 1),
            InputField("l", "Original length", "number", 1000),
        ]

    def calculate(self, values):
        dl, l = self.num(values, "dl"), self.num(values, "l")
        if l == 0:
            raise ValueError("Original length cannot be zero")
        strain = dl / l
        return [
            CalcResult("Strain", f"{fmt(strain, 6)}", "ε = ΔL/L (dimensionless)"),
            CalcResult("As percentage", f"{fmt(strain * 100, 4)}%"),
            CalcResult("Microstrain", f"{fmt(strain * 1e6, 2)} με"),
        ]
