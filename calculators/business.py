"""Business calculators."""
import math
from .base import Calculator, CalcResult, InputField, fmt, money


class RevenueCalc(Calculator):
    id = "biz_revenue"
    name = "Revenue"
    category = "Business"
    description = "Total revenue from price and quantity"
    icon = "💰"
    example = "100 units × $50 = $5000"

    def get_inputs(self):
        return [
            InputField("price", "Price per unit", "number", 50),
            InputField("qty", "Quantity sold", "number", 100),
        ]

    def calculate(self, values):
        price, qty = self.num(values, "price"), self.num(values, "qty")
        revenue = price * qty
        return [
            CalcResult("Revenue", money(revenue), "Price × Quantity"),
            CalcResult("Average revenue", money(price)),
        ]


class ExpensesCalc(Calculator):
    id = "biz_expenses"
    name = "Expenses"
    category = "Business"
    description = "Total expenses from a list"
    icon = "🧾"
    example = "Rent 1000, Salaries 2000 → 3000"

    def get_inputs(self):
        return [
            InputField("items", "Expense amounts (comma separated)", "text", "1000,2000,500"),
            InputField("labels", "Labels (optional, comma separated)", "text", "Rent,Salaries,Utilities", required=False),
        ]

    def calculate(self, values):
        try:
            amounts = [float(x.strip()) for x in str(values.get("items", "")).split(",") if x.strip()]
        except ValueError:
            raise ValueError("Enter valid amounts separated by commas")
        if not amounts:
            raise ValueError("Enter at least one expense")
        labels = [x.strip() for x in str(values.get("labels", "")).split(",") if x.strip()]
        total = sum(amounts)
        results = [CalcResult("Total expenses", money(total))]
        if len(labels) == len(amounts):
            for label, amt in zip(labels, amounts):
                results.append(CalcResult(label, money(amt)))
        return results


class GrossProfitCalc(Calculator):
    id = "biz_gross_profit"
    name = "Gross Profit"
    category = "Business"
    description = "Revenue − Cost of Goods Sold"
    icon = "📊"
    example = "Revenue 5000, COGS 3000 → 2000 (40%)"

    def get_inputs(self):
        return [
            InputField("revenue", "Revenue", "number", 5000),
            InputField("cogs", "Cost of goods sold", "number", 3000),
        ]

    def calculate(self, values):
        rev, cogs = self.num(values, "revenue"), self.num(values, "cogs")
        gp = rev - cogs
        margin = gp / rev * 100 if rev else 0
        return [
            CalcResult("Gross profit", money(gp), "Revenue − COGS"),
            CalcResult("Gross margin", f"{fmt(margin, 2)}%"),
        ]


class NetProfitCalc(Calculator):
    id = "biz_net_profit"
    name = "Net Profit"
    category = "Business"
    description = "Revenue − all expenses"
    icon = "🏦"
    example = "Revenue 10000, expenses 7000 → 3000"

    def get_inputs(self):
        return [
            InputField("revenue", "Revenue", "number", 10000),
            InputField("expenses", "Total expenses", "number", 7000),
            InputField("tax", "Tax rate (%)", "number", 0, required=False),
        ]

    def calculate(self, values):
        rev, exp = self.num(values, "revenue"), self.num(values, "expenses")
        tax = self.num(values, "tax") / 100
        pre_tax = rev - exp
        tax_amt = pre_tax * tax
        net = pre_tax - tax_amt
        return [
            CalcResult("Profit before tax", money(pre_tax)),
            CalcResult("Tax", money(tax_amt)),
            CalcResult("Net profit", money(net)),
            CalcResult("Net margin", f"{fmt(net / rev * 100 if rev else 0, 2)}%"),
        ]


class ROICalc(Calculator):
    id = "biz_roi"
    name = "ROI"
    category = "Business"
    description = "Return on Investment"
    icon = "📈"
    example = "Invest 5000, gain 6500 → 30%"

    def get_inputs(self):
        return [
            InputField("invested", "Amount invested", "number", 5000),
            InputField("returned", "Final value", "number", 6500),
        ]

    def calculate(self, values):
        inv, ret = self.num(values, "invested"), self.num(values, "returned")
        if inv == 0:
            raise ValueError("Investment cannot be zero")
        profit = ret - inv
        roi = profit / inv * 100
        return [
            CalcResult("Profit", money(profit)),
            CalcResult("ROI", f"{fmt(roi, 2)}%"),
            CalcResult("ROI (annualized if 1 yr)", f"{fmt(roi, 2)}%/yr"),
        ]


class MarketShareCalc(Calculator):
    id = "biz_market_share"
    name = "Market Share"
    category = "Business"
    description = "Company share of total market"
    icon = "🌍"
    example = "Company 500K, market 5M → 10%"

    def get_inputs(self):
        return [
            InputField("company", "Company sales", "number", 500000),
            InputField("market", "Total market size", "number", 5000000),
        ]

    def calculate(self, values):
        company, market = self.num(values, "company"), self.num(values, "market")
        if market == 0:
            raise ValueError("Market size cannot be zero")
        share = company / market * 100
        return [
            CalcResult("Market share", f"{fmt(share, 2)}%"),
            CalcResult("Relative share", f"{fmt(company / (market - company) * 100 if market != company else 0, 2)}% of others"),
        ]


class CAGRCalc(Calculator):
    id = "biz_cagr"
    name = "CAGR"
    category = "Business"
    description = "Compound Annual Growth Rate"
    icon = "🌱"
    example = "100→200 in 5y = 14.87%"

    def get_inputs(self):
        return [
            InputField("begin", "Beginning value", "number", 100),
            InputField("end", "Ending value", "number", 200),
            InputField("years", "Years", "number", 5),
        ]

    def calculate(self, values):
        begin, end = self.num(values, "begin"), self.num(values, "end")
        years = self.num(values, "years")
        if begin <= 0 or years <= 0:
            raise ValueError("Begin value and years must be positive")
        cagr = ((end / begin) ** (1 / years) - 1) * 100
        return [
            CalcResult("CAGR", f"{fmt(cagr, 2)}%", "(End/Begin)^(1/n) − 1"),
            CalcResult("Total growth", f"{fmt((end / begin - 1) * 100, 2)}%"),
        ]


class ProductivityCalc(Calculator):
    id = "biz_productivity"
    name = "Productivity"
    category = "Business"
    description = "Output per unit of input"
    icon = "⚡"
    example = "500 units / 40 hours = 12.5/hr"

    def get_inputs(self):
        return [
            InputField("output", "Output (units)", "number", 500),
            InputField("input", "Input (hours/workers)", "number", 40),
        ]

    def calculate(self, values):
        out, inp = self.num(values, "output"), self.num(values, "input")
        if inp == 0:
            raise ValueError("Input cannot be zero")
        prod = out / inp
        return [
            CalcResult("Productivity", f"{fmt(prod, 3)} units/input"),
            CalcResult("Efficiency vs 100% target", f"{fmt(prod * 100, 1)}%"),
        ]


class InventoryTurnoverCalc(Calculator):
    id = "biz_inventory"
    name = "Inventory Turnover"
    category = "Business"
    description = "How often inventory is sold in a period"
    icon = "📦"
    example = "COGS 100K, avg inventory 20K → 5×"

    def get_inputs(self):
        return [
            InputField("cogs", "Cost of goods sold", "number", 100000),
            InputField("avg_inv", "Average inventory", "number", 20000),
        ]

    def calculate(self, values):
        cogs, avg = self.num(values, "cogs"), self.num(values, "avg_inv")
        if avg == 0:
            raise ValueError("Average inventory cannot be zero")
        turnover = cogs / avg
        days = 365 / turnover
        return [
            CalcResult("Inventory turnover", f"{fmt(turnover, 2)}×", "COGS / Avg inventory"),
            CalcResult("Days of inventory", f"{fmt(days, 1)} days", "365 / turnover"),
        ]


class DepreciationCalc(Calculator):
    id = "biz_depreciation"
    name = "Depreciation"
    category = "Business"
    description = "Straight-line depreciation"
    icon = "📉"
    example = "Asset 10000, salvage 1000, 5y → 1800/yr"

    def get_inputs(self):
        return [
            InputField("cost", "Asset cost", "number", 10000),
            InputField("salvage", "Salvage value", "number", 1000),
            InputField("life", "Useful life (years)", "number", 5),
        ]

    def calculate(self, values):
        cost, salvage = self.num(values, "cost"), self.num(values, "salvage")
        life = self.num(values, "life")
        if life <= 0:
            raise ValueError("Useful life must be positive")
        annual = (cost - salvage) / life
        rate = annual / cost * 100 if cost else 0
        return [
            CalcResult("Annual depreciation", money(annual), "(Cost − Salvage) / Life"),
            CalcResult("Depreciation rate", f"{fmt(rate, 2)}%"),
            CalcResult("Monthly depreciation", money(annual / 12)),
            CalcResult("Book value after 1 year", money(cost - annual)),
        ]
