"""Computer Science calculators."""
import math
from .base import Calculator, CalcResult, InputField, fmt


class BinaryConversionCalc(Calculator):
    id = "cs_binary"
    name = "Binary Conversion"
    category = "Computer Science"
    description = "Decimal to binary, octal, hex"
    icon = "0️⃣1️⃣"
    example = "255 → 11111111, 377, FF"

    def get_inputs(self):
        return [
            InputField("dec", "Decimal number", "number", 255),
        ]

    def calculate(self, values):
        dec = int(self.num(values, "dec"))
        if dec < 0:
            raise ValueError("Enter a non-negative integer")
        return [
            CalcResult("Decimal", fmt(dec)),
            CalcResult("Binary", bin(dec)[2:]),
            CalcResult("Octal", oct(dec)[2:]),
            CalcResult("Hexadecimal", hex(dec)[2:].upper()),
        ]


class HexadecimalConversionCalc(Calculator):
    id = "cs_hex"
    name = "Hexadecimal Conversion"
    category = "Computer Science"
    description = "Hex to decimal, binary, octal"
    icon = "🔢"
    example = "FF → 255, 11111111, 377"

    def get_inputs(self):
        return [
            InputField("hex", "Hexadecimal value", "text", "FF"),
        ]

    def calculate(self, values):
        h = str(values.get("hex", "")).strip()
        try:
            dec = int(h, 16)
        except ValueError:
            raise ValueError("Enter a valid hexadecimal value")
        return [
            CalcResult("Decimal", fmt(dec)),
            CalcResult("Binary", bin(dec)[2:]),
            CalcResult("Octal", oct(dec)[2:]),
        ]


class OctalConversionCalc(Calculator):
    id = "cs_octal"
    name = "Octal Conversion"
    category = "Computer Science"
    description = "Octal to decimal, binary, hex"
    icon = "8️⃣"
    example = "377 → 255, 11111111, FF"

    def get_inputs(self):
        return [
            InputField("oct", "Octal value", "text", "377"),
        ]

    def calculate(self, values):
        o = str(values.get("oct", "")).strip()
        try:
            dec = int(o, 8)
        except ValueError:
            raise ValueError("Enter a valid octal value")
        return [
            CalcResult("Decimal", fmt(dec)),
            CalcResult("Binary", bin(dec)[2:]),
            CalcResult("Hexadecimal", hex(dec)[2:].upper()),
        ]


class BitwiseCalc(Calculator):
    id = "cs_bitwise"
    name = "Bitwise Calculation"
    category = "Computer Science"
    description = "AND, OR, XOR of two integers"
    icon = "🧮"
    example = "5 AND 3 = 1, 5 OR 3 = 7, 5 XOR 3 = 6"

    def get_inputs(self):
        return [
            InputField("a", "Integer A", "number", 5),
            InputField("b", "Integer B", "number", 3),
        ]

    def calculate(self, values):
        a, b = int(self.num(values, "a")), int(self.num(values, "b"))
        return [
            CalcResult("A & B (AND)", a & b, f"{a:08b} & {b:08b}"),
            CalcResult("A | B (OR)", a | b, f"{a:08b} | {b:08b}"),
            CalcResult("A ^ B (XOR)", a ^ b, f"{a:08b} ^ {b:08b}"),
            CalcResult("~A (NOT)", ~a),
            CalcResult("A << 1", a << 1),
            CalcResult("A >> 1", a >> 1),
        ]


class DataSizeCalc(Calculator):
    id = "cs_data_size"
    name = "Data Size Conversion"
    category = "Computer Science"
    description = "Convert between data storage units"
    icon = "💾"
    example = "1 GB = 1024 MB"

    def get_inputs(self):
        return [
            InputField("value", "Value", "number", 1),
            InputField("from", "From unit", "select", "GB", options=[
                "Bit", "Byte", "KB", "MB", "GB", "TB", "PB",
            ]),
            InputField("to", "To unit", "select", "MB", options=[
                "Bit", "Byte", "KB", "MB", "GB", "TB", "PB",
            ]),
        ]

    def calculate(self, values):
        value = self.num(values, "value")
        f = values.get("from", "GB")
        t = values.get("to", "MB")
        units = {"Bit": 1 / 8, "Byte": 1, "KB": 1024, "MB": 1024 ** 2,
                 "GB": 1024 ** 3, "TB": 1024 ** 4, "PB": 1024 ** 5}
        result = value * units[f] / units[t]
        return [
            CalcResult(f"{fmt(value)} {f} = {fmt(result, 6)} {t}", result),
            CalcResult("In bits", fmt(value * units[f] * 8)),
            CalcResult("In bytes", fmt(value * units[f])),
        ]


class NetworkBandwidthCalc(Calculator):
    id = "cs_bandwidth"
    name = "Network Bandwidth"
    category = "Computer Science"
    description = "Data transfer rate conversion"
    icon = "🌐"
    example = "100 Mbps = 12.5 MB/s"

    def get_inputs(self):
        return [
            InputField("speed", "Speed", "number", 100),
            InputField("unit", "Unit", "select", "Mbps", options=[
                "Kbps", "Mbps", "Gbps", "KB/s", "MB/s", "GB/s",
            ]),
        ]

    def calculate(self, values):
        speed = self.num(values, "speed")
        unit = values.get("unit", "Mbps")
        # convert to bits/sec
        to_bps = {
            "Kbps": 1000, "Mbps": 1000 ** 2, "Gbps": 1000 ** 3,
            "KB/s": 8000, "MB/s": 8000 * 1000, "GB/s": 8000 * 1000 ** 2,
        }
        bps = speed * to_bps[unit]
        return [
            CalcResult("In Mbps", fmt(bps / 1e6, 4)),
            CalcResult("In Gbps", fmt(bps / 1e9, 6)),
            CalcResult("In MB/s", fmt(bps / 8e6, 4)),
            CalcResult("In GB/s", fmt(bps / 8e9, 6)),
        ]


class DownloadTimeCalc(Calculator):
    id = "cs_download_time"
    name = "Download Time"
    category = "Computer Science"
    description = "Time to download a file at given speed"
    icon = "⬇️"
    example = "2 GB at 10 Mbps → 27.3 min"

    def get_inputs(self):
        return [
            InputField("size", "File size", "number", 2),
            InputField("size_unit", "Size unit", "select", "GB", options=["MB", "GB", "TB"]),
            InputField("speed", "Download speed (Mbps)", "number", 10),
        ]

    def calculate(self, values):
        size = self.num(values, "size")
        su = values.get("size_unit", "GB")
        speed = self.num(values, "speed")
        if speed <= 0:
            raise ValueError("Speed must be positive")
        bytes_map = {"MB": 8e6, "GB": 8e9, "TB": 8e12}
        bits = size * bytes_map[su]
        seconds = bits / (speed * 1e6)
        return [
            CalcResult("Seconds", fmt(seconds, 1)),
            CalcResult("Minutes", fmt(seconds / 60, 2)),
            CalcResult("Hours", fmt(seconds / 3600, 3)),
        ]


class StorageRequirementsCalc(Calculator):
    id = "cs_storage"
    name = "Storage Requirements"
    category = "Computer Science"
    description = "Storage needed for file count × size"
    icon = "🗄️"
    example = "1000 files × 5 MB = 4.88 GB"

    def get_inputs(self):
        return [
            InputField("files", "Number of files", "number", 1000),
            InputField("size", "Average file size", "number", 5),
            InputField("unit", "Size unit", "select", "MB", options=["KB", "MB", "GB"]),
        ]

    def calculate(self, values):
        files = self.num(values, "files")
        size = self.num(values, "size")
        unit = values.get("unit", "MB")
        mul = {"KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3}
        bytes_total = files * size * mul[unit]
        return [
            CalcResult("Total size (bytes)", fmt(bytes_total)),
            CalcResult("In MB", fmt(bytes_total / (1024 ** 2), 3)),
            CalcResult("In GB", fmt(bytes_total / (1024 ** 3), 3)),
            CalcResult("In TB", fmt(bytes_total / (1024 ** 4), 6)),
        ]
