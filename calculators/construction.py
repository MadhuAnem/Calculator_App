"""Construction calculators."""
import math
from .base import Calculator, CalcResult, InputField, fmt


class ConcreteCalc(Calculator):
    id = "const_concrete"
    name = "Concrete Quantity"
    category = "Construction"
    description = "Concrete volume needed for a slab"
    icon = "🏗️"
    example = "10×5m slab, 0.15m thick → 7.5 m³"

    def get_inputs(self):
        return [
            InputField("length", "Length (m)", "number", 10),
            InputField("width", "Width (m)", "number", 5),
            InputField("thickness", "Thickness (m)", "number", 0.15),
        ]

    def calculate(self, values):
        l, w, t = self.num(values, "length"), self.num(values, "width"), self.num(values, "thickness")
        vol = l * w * t
        return [
            CalcResult("Concrete volume", f"{fmt(vol, 3)} m³"),
            CalcResult("In cubic feet", f"{fmt(vol * 35.3147, 2)} ft³"),
            CalcResult("In cubic yards", f"{fmt(vol * 1.30795, 3)} yd³"),
        ]


class CementBagsCalc(Calculator):
    id = "const_cement"
    name = "Cement Bags"
    category = "Construction"
    description = "Cement bags needed for concrete mix"
    icon = "🧱"
    example = "7.5 m³ M15 (1:2:4) → 45 bags"

    def get_inputs(self):
        return [
            InputField("volume", "Concrete volume (m³)", "number", 7.5),
            InputField("mix", "Mix ratio", "select", "M15 (1:2:4)", options=[
                "M10 (1:3:6)", "M15 (1:2:4)", "M20 (1:1.5:3)", "M25 (1:1:2)",
            ]),
        ]

    def calculate(self, values):
        vol = self.num(values, "volume")
        mix = values.get("mix", "M15 (1:2:4)")
        ratios = {"M10 (1:3:6)": 10, "M15 (1:2:4)": 7, "M20 (1:1.5:3)": 5.5, "M25 (1:1:2)": 4}
        r = ratios.get(mix, 7)
        # dry volume ~1.54× wet volume; cement share = 1/r; 1 bag = 0.0347 m³
        dry = vol * 1.54
        cement_vol = dry / r
        bags = cement_vol / 0.0347
        return [
            CalcResult("Dry volume", f"{fmt(dry, 3)} m³", "Wet × 1.54"),
            CalcResult("Cement volume", f"{fmt(cement_vol, 3)} m³"),
            CalcResult("Cement bags (50kg)", f"{fmt(math.ceil(bags), 0)} bags"),
            CalcResult("Cement weight", f"{fmt(bags * 50, 0)} kg"),
        ]


class SandQuantityCalc(Calculator):
    id = "const_sand"
    name = "Sand Quantity"
    category = "Construction"
    description = "Sand and aggregate needed for concrete"
    icon = "🏖️"
    example = "M15 for 7.5 m³ → sand 2.2 m³"

    def get_inputs(self):
        return [
            InputField("volume", "Concrete volume (m³)", "number", 7.5),
            InputField("mix", "Mix ratio", "select", "M15 (1:2:4)", options=[
                "M10 (1:3:6)", "M15 (1:2:4)", "M20 (1:1.5:3)", "M25 (1:1:2)",
            ]),
        ]

    def calculate(self, values):
        vol = self.num(values, "volume")
        mix = values.get("mix", "M15 (1:2:4)")
        parts = {
            "M10 (1:3:6)": (1, 3, 6),
            "M15 (1:2:4)": (1, 2, 4),
            "M20 (1:1.5:3)": (1, 1.5, 3),
            "M25 (1:1:2)": (1, 1, 2),
        }
        c, s, agg = parts.get(mix, (1, 2, 4))
        total = c + s + agg
        dry = vol * 1.54
        sand = dry * s / total
        agg_qty = dry * agg / total
        return [
            CalcResult("Sand quantity", f"{fmt(sand, 3)} m³"),
            CalcResult("Sand weight", f"{fmt(sand * 1600, 0)} kg", "@1600 kg/m³"),
            CalcResult("Aggregate quantity", f"{fmt(agg_qty, 3)} m³"),
            CalcResult("Aggregate weight", f"{fmt(agg_qty * 1450, 0)} kg", "@1450 kg/m³"),
        ]


class SteelWeightCalc(Calculator):
    id = "const_steel"
    name = "Steel Weight"
    category = "Construction"
    description = "Weight of steel bars"
    icon = "🔩"
    example = "12mm bar, 10m → 8.88 kg"

    def get_inputs(self):
        return [
            InputField("dia", "Bar diameter (mm)", "number", 12),
            InputField("length", "Total length (m)", "number", 10),
            InputField("bars", "Number of bars", "number", 1, required=False),
        ]

    def calculate(self, values):
        dia = self.num(values, "dia")
        length = self.num(values, "length")
        bars = self.num(values, "bars") or 1
        unit_w = dia * dia / 162  # kg per meter
        total = unit_w * length * bars
        return [
            CalcResult("Unit weight", f"{fmt(unit_w, 3)} kg/m", "d²/162"),
            CalcResult("Total steel weight", f"{fmt(total, 2)} kg"),
            CalcResult("In tons", f"{fmt(total / 1000, 4)} t"),
        ]


class BrickCountCalc(Calculator):
    id = "const_brick"
    name = "Brick Count"
    category = "Construction"
    description = "Number of bricks for a wall"
    icon = "🧱"
    example = "Wall 10×3m, 0.23m thick → ~5400 bricks"

    def get_inputs(self):
        return [
            InputField("length", "Wall length (m)", "number", 10),
            InputField("height", "Wall height (m)", "number", 3),
            InputField("thickness", "Wall thickness (m)", "number", 0.23),
            InputField("waste", "Wastage (%)", "number", 5, required=False),
        ]

    def calculate(self, values):
        l, h, t = self.num(values, "length"), self.num(values, "height"), self.num(values, "thickness")
        waste = self.num(values, "waste") / 100
        # standard brick 0.19 × 0.09 × 0.09 m; with mortar 0.2 × 0.1 × 0.1
        brick_vol = 0.2 * 0.1 * 0.1
        wall_vol = l * h * t
        bricks = wall_vol / brick_vol
        total = bricks * (1 + waste)
        return [
            CalcResult("Wall volume", f"{fmt(wall_vol, 3)} m³"),
            CalcResult("Bricks needed", f"{fmt(math.ceil(total), 0)}"),
            CalcResult("With 5% wastage", f"{fmt(math.ceil(bricks * 1.05), 0)}"),
        ]


class TileCountCalc(Calculator):
    id = "const_tile"
    name = "Tile Count"
    category = "Construction"
    description = "Number of tiles for flooring"
    icon = "🟦"
    example = "Room 5×4m, 60×60cm tiles → 56 tiles"

    def get_inputs(self):
        return [
            InputField("length", "Room length (m)", "number", 5),
            InputField("width", "Room width (m)", "number", 4),
            InputField("tile", "Tile size (cm)", "select", "60×60", options=[
                "30×30", "45×45", "60×60", "80×80",
            ]),
            InputField("waste", "Wastage (%)", "number", 10, required=False),
        ]

    def calculate(self, values):
        l, w = self.num(values, "length"), self.num(values, "width")
        tile = values.get("tile", "60×60")
        t = int(tile.split("×")[0]) / 100
        area = l * w
        tile_area = t * t
        count = area / tile_area
        total = count * (1 + self.num(values, "waste") / 100)
        return [
            CalcResult("Room area", f"{fmt(area, 2)} m²"),
            CalcResult("Tiles needed", f"{fmt(math.ceil(total), 0)}"),
            CalcResult("Boxes (4 tiles/box)", f"{fmt(math.ceil(total / 4), 0)}"),
        ]


class PaintRequiredCalc(Calculator):
    id = "const_paint"
    name = "Paint Required"
    category = "Construction"
    description = "Paint litres needed for walls"
    icon = "🖌️"
    example = "Room 10×8×3m → ~4.3 L (1 coat)"

    def get_inputs(self):
        return [
            InputField("length", "Room length (m)", "number", 10),
            InputField("width", "Room width (m)", "number", 8),
            InputField("height", "Ceiling height (m)", "number", 3),
            InputField("coats", "Number of coats", "number", 1, required=False),
            InputField("doors_windows", "Door/window area (m²)", "number", 6, required=False),
        ]

    def calculate(self, values):
        l, w, h = self.num(values, "length"), self.num(values, "width"), self.num(values, "height")
        coats = self.num(values, "coats") or 1
        dw = self.num(values, "doors_windows") or 0
        wall_area = 2 * (l + w) * h - dw
        ceiling = l * w
        # coverage ~10 m²/L per coat
        litres_wall = wall_area * coats / 10
        litres_ceiling = ceiling * coats / 10
        return [
            CalcResult("Wall area", f"{fmt(wall_area, 2)} m²"),
            CalcResult("Ceiling area", f"{fmt(ceiling, 2)} m²"),
            CalcResult("Paint for walls", f"{fmt(litres_wall, 2)} L", "@10 m²/L"),
            CalcResult("Paint for ceiling", f"{fmt(litres_ceiling, 2)} L"),
            CalcResult("Total paint", f"{fmt(litres_wall + litres_ceiling, 2)} L"),
        ]


class FlooringAreaCalc(Calculator):
    id = "const_flooring"
    name = "Flooring Area"
    category = "Construction"
    description = "Flooring area and materials cost"
    icon = "🏠"
    example = "Room 5×4m = 20 m²"

    def get_inputs(self):
        return [
            InputField("length", "Length (m)", "number", 5),
            InputField("width", "Width (m)", "number", 4),
            InputField("price", "Material price per m²", "number", 0, required=False),
        ]

    def calculate(self, values):
        l, w = self.num(values, "length"), self.num(values, "width")
        area = l * w
        price = self.num(values, "price")
        results = [
            CalcResult("Flooring area", f"{fmt(area, 2)} m²"),
            CalcResult("In square feet", f"{fmt(area * 10.7639, 2)} ft²"),
        ]
        if price > 0:
            results.append(CalcResult("Material cost", f"${fmt(area * price, 2)}"))
        return results


class RoofingMaterialsCalc(Calculator):
    id = "const_roofing"
    name = "Roofing Materials"
    category = "Construction"
    description = "Roof area and material estimate"
    icon = "🏠"
    example = "10×8m roof at 30° slope → 92.4 m²"

    def get_inputs(self):
        return [
            InputField("length", "Length (m)", "number", 10),
            InputField("width", "Width (m)", "number", 8),
            InputField("pitch", "Roof pitch (degrees)", "number", 30),
        ]

    def calculate(self, values):
        l, w = self.num(values, "length"), self.num(values, "width")
        pitch = math.radians(self.num(values, "pitch"))
        flat = l * w
        sloped = flat / math.cos(pitch) if math.cos(pitch) > 0 else flat
        return [
            CalcResult("Flat area", f"{fmt(flat, 2)} m²"),
            CalcResult("Sloped roof area", f"{fmt(sloped, 2)} m²"),
            CalcResult("Sheets (2.4×0.9m)", f"{fmt(math.ceil(sloped / 2.16), 0)}"),
        ]
