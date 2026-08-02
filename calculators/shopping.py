"""Shopping calculators."""
import math
from .base import Calculator, CalcResult, InputField, fmt, money


class ShoppingDiscountCalc(Calculator):
    id = "shop_discount"
    name = "Discount"
    category = "Shopping"
    description = "Final price after discount"
    icon = "🏷️"
    example = "$100 at 25% off = $75"

    def get_inputs(self):
        return [
            InputField("price", "Original price", "number", 100),
            InputField("discount", "Discount (%)", "number", 25),
        ]

    def calculate(self, values):
        price, disc = self.num(values, "price"), self.num(values, "discount")
        saved = price * disc / 100
        final = price - saved
        return [
            CalcResult("You save", money(saved)),
            CalcResult("Final price", money(final)),
            CalcResult("You pay %", f"{fmt(100 - disc, 1)}%"),
        ]


class CashbackCalc(Calculator):
    id = "shop_cashback"
    name = "Cashback"
    category = "Shopping"
    description = "Cashback earned on a purchase"
    icon = "💳"
    example = "$500 at 5% cashback = $25"

    def get_inputs(self):
        return [
            InputField("amount", "Purchase amount", "number", 500),
            InputField("rate", "Cashback rate (%)", "number", 5),
        ]

    def calculate(self, values):
        amount, rate = self.num(values, "amount"), self.num(values, "rate")
        cb = amount * rate / 100
        return [
            CalcResult("Cashback", money(cb)),
            CalcResult("Effective cost", money(amount - cb)),
            CalcResult("Effective discount", f"{fmt(rate, 2)}%"),
        ]


class ShoppingEMICalc(Calculator):
    id = "shop_emi"
    name = "EMI (Shopping)"
    category = "Shopping"
    description = "Monthly EMI on a purchase"
    icon = "🛒"
    example = "$1200 at 12% for 12 months = $106.6/mo"

    def get_inputs(self):
        return [
            InputField("price", "Item price", "number", 1200),
            InputField("down", "Down payment", "number", 0, required=False),
            InputField("rate", "Annual interest (%)", "number", 12),
            InputField("months", "Tenure (months)", "number", 12),
        ]

    def calculate(self, values):
        price, down = self.num(values, "price"), self.num(values, "down")
        rate, months = self.num(values, "rate"), int(self.num(values, "months"))
        if months <= 0:
            raise ValueError("Tenure must be positive")
        principal = price - down
        i = rate / 100 / 12
        if i == 0:
            emi = principal / months
        else:
            emi = principal * i * (1 + i) ** months / ((1 + i) ** months - 1)
        return [
            CalcResult("Financed amount", money(principal)),
            CalcResult("Monthly EMI", money(emi)),
            CalcResult("Total payable", money(emi * months)),
            CalcResult("Interest paid", money(emi * months - principal)),
        ]


class FinalPriceCalc(Calculator):
    id = "shop_final"
    name = "Final Price"
    category = "Shopping"
    description = "Price after discount + tax"
    icon = "🧾"
    example = "$100, 10% off, 8% tax = $97.2"

    def get_inputs(self):
        return [
            InputField("price", "Original price", "number", 100),
            InputField("discount", "Discount (%)", "number", 10),
            InputField("tax", "Tax rate (%)", "number", 8),
        ]

    def calculate(self, values):
        price, disc = self.num(values, "price"), self.num(values, "discount")
        tax = self.num(values, "tax")
        discounted = price * (1 - disc / 100)
        tax_amt = discounted * tax / 100
        final = discounted + tax_amt
        return [
            CalcResult("After discount", money(discounted)),
            CalcResult("Tax amount", money(tax_amt)),
            CalcResult("Final price", money(final)),
            CalcResult("Total savings vs original", money(price - final)),
        ]


class PriceComparisonCalc(Calculator):
    id = "shop_compare"
    name = "Price Comparison"
    category = "Shopping"
    description = "Compare unit prices of two products"
    icon = "⚖️"
    example = "500g for $3 vs 1kg for $5.5"

    def get_inputs(self):
        return [
            InputField("p1", "Product 1 price", "number", 3),
            InputField("q1", "Product 1 quantity", "number", 0.5),
            InputField("p2", "Product 2 price", "number", 5.5),
            InputField("q2", "Product 2 quantity", "number", 1),
        ]

    def calculate(self, values):
        p1, q1 = self.num(values, "p1"), self.num(values, "q1")
        p2, q2 = self.num(values, "p2"), self.num(values, "q2")
        if q1 <= 0 or q2 <= 0:
            raise ValueError("Quantities must be positive")
        up1, up2 = p1 / q1, p2 / q2
        if up1 < up2:
            better = "Product 1"
        elif up2 < up1:
            better = "Product 2"
        else:
            better = "Equal"
        return [
            CalcResult("Product 1 unit price", money(up1)),
            CalcResult("Product 2 unit price", money(up2)),
            CalcResult("Better deal", better),
            CalcResult("Savings per unit", money(abs(up1 - up2))),
        ]


class CostPerUnitCalc(Calculator):
    id = "shop_cost_per_unit"
    name = "Cost Per Unit"
    category = "Shopping"
    description = "Cost per unit of a package"
    icon = "📦"
    example = "Pack of 24 for $6 → $0.25 each"

    def get_inputs(self):
        return [
            InputField("price", "Total price", "number", 6),
            InputField("units", "Number of units", "number", 24),
        ]

    def calculate(self, values):
        price, units = self.num(values, "price"), self.num(values, "units")
        if units <= 0:
            raise ValueError("Units must be positive")
        cpu = price / units
        return [
            CalcResult("Cost per unit", money(cpu)),
            CalcResult("Units per dollar", f"{fmt(units / price if price else 0, 3)}"),
        ]
