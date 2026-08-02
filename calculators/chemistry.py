"""Chemistry calculators."""
import math
from .base import Calculator, CalcResult, InputField, fmt


class MolarityCalc(Calculator):
    id = "chem_molarity"
    name = "Molarity"
    category = "Chemistry"
    description = "M = moles / volume (litres)"
    icon = "🧪"
    example = "0.5 mol in 0.25 L → 2 M"

    def get_inputs(self):
        return [
            InputField("moles", "Moles of solute", "number", 0.5),
            InputField("volume", "Volume (litres)", "number", 0.25),
        ]

    def calculate(self, values):
        moles, volume = self.num(values, "moles"), self.num(values, "volume")
        if volume == 0:
            raise ValueError("Volume cannot be zero")
        m = moles / volume
        return [
            CalcResult("Molarity", f"{fmt(m, 4)} M", "M = moles/L"),
            CalcResult("In mmol/mL", f"{fmt(m, 4)} mmol/mL"),
        ]


class NormalityCalc(Calculator):
    id = "chem_normality"
    name = "Normality"
    category = "Chemistry"
    description = "N = Molarity × n-factor"
    icon = "⚗️"
    example = "2 M H₂SO₄ (n=2) → 4 N"

    def get_inputs(self):
        return [
            InputField("molarity", "Molarity (M)", "number", 2),
            InputField("n_factor", "n-factor (equivalents/mol)", "number", 2),
        ]

    def calculate(self, values):
        m, nf = self.num(values, "molarity"), self.num(values, "n_factor")
        n = m * nf
        return [
            CalcResult("Normality", f"{fmt(n, 4)} N", "N = M × n-factor"),
        ]


class MolesCalc(Calculator):
    id = "chem_moles"
    name = "Moles"
    category = "Chemistry"
    description = "moles = mass / molar mass"
    icon = "🧮"
    example = "18 g water (18 g/mol) → 1 mol"

    def get_inputs(self):
        return [
            InputField("mass", "Mass (g)", "number", 18),
            InputField("molar_mass", "Molar mass (g/mol)", "number", 18),
        ]

    def calculate(self, values):
        mass, mm = self.num(values, "mass"), self.num(values, "molar_mass")
        if mm == 0:
            raise ValueError("Molar mass cannot be zero")
        moles = mass / mm
        molecules = moles * 6.022e23
        return [
            CalcResult("Moles", f"{fmt(moles, 4)} mol", "n = mass/molar mass"),
            CalcResult("Number of molecules", f"{molecules:.3e}", "n × Avogadro"),
        ]


class MolecularWeightCalc(Calculator):
    id = "chem_mol_weight"
    name = "Molecular Weight"
    category = "Chemistry"
    description = "Sum of atomic weights × counts"
    icon = "⚖️"
    example = "H₂O = 18.015 g/mol"

    def get_inputs(self):
        return [
            InputField("formula", "Formula (e.g., H2O, CO2, NaCl)", "text", "H2O"),
        ]

    def calculate(self, values):
        formula = str(values.get("formula", "")).strip()
        if not formula:
            raise ValueError("Enter a chemical formula")
        weights = {
            "H": 1.008, "He": 4.003, "Li": 6.94, "Be": 9.012, "B": 10.81,
            "C": 12.011, "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180,
            "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.085, "P": 30.974,
            "S": 32.06, "Cl": 35.45, "Ar": 39.948, "K": 39.098, "Ca": 40.078,
            "Fe": 55.845, "Cu": 63.546, "Zn": 65.38, "Ag": 107.868, "I": 126.904,
            "Ba": 137.327, "Au": 196.967, "Hg": 200.592, "Pb": 207.2,
        }
        total = 0
        i = 0
        breakdown = []
        while i < len(formula):
            if formula[i].isupper():
                sym = formula[i]
                j = i + 1
                while j < len(formula) and formula[j].islower():
                    sym += formula[j]
                    j += 1
                count = ""
                while j < len(formula) and formula[j].isdigit():
                    count += formula[j]
                    j += 1
                n = int(count) if count else 1
                if sym not in weights:
                    raise ValueError(f"Unknown element: {sym}")
                w = weights[sym] * n
                total += w
                breakdown.append(f"{sym}{n if n > 1 else ''}: {fmt(w, 3)}")
                i = j
            else:
                raise ValueError(f"Invalid formula near '{formula[i:]}'")
        return [
            CalcResult("Molecular weight", f"{fmt(total, 4)} g/mol"),
            CalcResult("Breakdown", ", ".join(breakdown)),
        ]


class pHCalc(Calculator):
    id = "chem_ph"
    name = "pH"
    category = "Chemistry"
    description = "pH from [H+] concentration"
    icon = "💧"
    example = "[H+]=1e-7 → pH 7"

    def get_inputs(self):
        return [
            InputField("h", "H⁺ concentration (mol/L)", "number", 0.0000001),
        ]

    def calculate(self, values):
        h = self.num(values, "h")
        if h <= 0:
            raise ValueError("Concentration must be positive")
        ph = -math.log10(h)
        if ph < 0:
            cat = "Very acidic"
        elif ph < 7:
            cat = "Acidic"
        elif ph == 7:
            cat = "Neutral"
        elif ph <= 14:
            cat = "Basic / Alkaline"
        else:
            cat = "Very basic"
        pOH = 14 - ph
        return [
            CalcResult("pH", f"{fmt(ph, 2)}", "pH = −log₁₀[H⁺]"),
            CalcResult("Category", cat),
            CalcResult("pOH", f"{fmt(pOH, 2)}", "pOH = 14 − pH"),
        ]


class DilutionCalc(Calculator):
    id = "chem_dilution"
    name = "Dilution"
    category = "Chemistry"
    description = "C₁V₁ = C₂V₂"
    icon = "🫗"
    example = "5 M × 10 mL → 1 M in 50 mL"

    def get_inputs(self):
        return [
            InputField("c1", "Initial concentration (C₁)", "number", 5),
            InputField("v1", "Initial volume (V₁)", "number", 10),
            InputField("c2", "Final concentration (C₂)", "number", 1),
        ]

    def calculate(self, values):
        c1, v1, c2 = self.num(values, "c1"), self.num(values, "v1"), self.num(values, "c2")
        if c2 == 0:
            raise ValueError("Final concentration cannot be zero")
        v2 = c1 * v1 / c2
        water = v2 - v1
        return [
            CalcResult("Final volume (V₂)", f"{fmt(v2, 4)} mL", "C₁V₁/C₂"),
            CalcResult("Solvent to add", f"{fmt(water, 4)} mL", "V₂ − V₁"),
        ]


class ConcentrationCalc(Calculator):
    id = "chem_concentration"
    name = "Concentration"
    category = "Chemistry"
    description = "Percent concentration by mass"
    icon = "🧂"
    example = "10 g solute in 90 g solvent → 10%"

    def get_inputs(self):
        return [
            InputField("solute", "Solute mass (g)", "number", 10),
            InputField("solvent", "Solvent mass (g)", "number", 90),
        ]

    def calculate(self, values):
        solute, solvent = self.num(values, "solute"), self.num(values, "solvent")
        total = solute + solvent
        pct = solute / total * 100 if total else 0
        ppm = solute / total * 1e6 if total else 0
        return [
            CalcResult("Concentration", f"{fmt(pct, 4)}% (w/w)", "solute/total × 100"),
            CalcResult("In ppm", f"{fmt(ppm, 2)} ppm"),
        ]


class ReactionYieldCalc(Calculator):
    id = "chem_yield"
    name = "Reaction Yield"
    category = "Chemistry"
    description = "Percent yield = actual/theoretical × 100"
    icon = "⚗️"
    example = "Actual 8 g, theoretical 10 g → 80%"

    def get_inputs(self):
        return [
            InputField("actual", "Actual yield (g)", "number", 8),
            InputField("theoretical", "Theoretical yield (g)", "number", 10),
        ]

    def calculate(self, values):
        actual, theoretical = self.num(values, "actual"), self.num(values, "theoretical")
        if theoretical == 0:
            raise ValueError("Theoretical yield cannot be zero")
        pct = actual / theoretical * 100
        loss = theoretical - actual
        return [
            CalcResult("Percent yield", f"{fmt(pct, 2)}%", "actual/theoretical × 100"),
            CalcResult("Loss", f"{fmt(loss, 4)} g", "theoretical − actual"),
        ]
