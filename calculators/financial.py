"""Financial Calculations."""
import math
from .base import Calculator, CalcResult, InputField, fmt, money


class SimpleInterestCalc(Calculator):
    id = "fin_si"
    name = "Simple Interest"
    category = "Financial Calculations"
    description = "SI = P × R × T / 100"
    icon = "🏦"
    example = "P=1000, R=5%, T=3y → SI=150"

    def get_inputs(self):
        return [
            InputField("p", "Principal (P)", "number", 1000),
            InputField("r", "Annual rate (R %)", "number", 5),
            InputField("t", "Time (years)", "number", 3),
        ]

    def calculate(self, values):
        p, r, t = self.num(values, "p"), self.num(values, "r"), self.num(values, "t")
        si = (p * r * t) / 100
        return [
            CalcResult("Simple Interest", money(si), "SI = P×R×T/100"),
            CalcResult("Total Amount", money(p + si), "A = P + SI"),
        ]


class CompoundInterestCalc(Calculator):
    id = "fin_ci"
    name = "Compound Interest"
    category = "Financial Calculations"
    description = "A = P(1 + r/n)^(nt)"
    icon = "📈"
    example = "P=1000, 5%, 5y, yearly → A=1276.28"

    def get_inputs(self):
        return [
            InputField("p", "Principal (P)", "number", 1000),
            InputField("r", "Annual rate (R %)", "number", 5),
            InputField("t", "Time (years)", "number", 5),
            InputField("n", "Compounds per year", "select", 1, options=["1", "2", "4", "12", "365"]),
        ]

    def calculate(self, values):
        p, r, t = self.num(values, "p"), self.num(values, "r"), self.num(values, "t")
        n = float(values.get("n", 1))
        if n <= 0:
            raise ValueError("Compounds per year must be positive")
        rate = r / 100
        a = p * (1 + rate / n) ** (n * t)
        ci = a - p
        return [
            CalcResult("Total Amount", money(a), "A = P(1+r/n)^(nt)"),
            CalcResult("Compound Interest", money(ci), "CI = A - P"),
            CalcResult("Effective annual rate", f"{fmt(((1 + rate / n) ** n - 1) * 100, 4)}%"),
        ]


class EMICalc(Calculator):
    id = "fin_emi"
    name = "EMI (Loan Repayment)"
    category = "Financial Calculations"
    description = "EMI = P·r·(1+r)^n / ((1+r)^n - 1)"
    icon = "🏠"
    example = "P=500000, 8%, 5y → EMI ≈ 10,138"

    def get_inputs(self):
        return [
            InputField("p", "Loan amount (P)", "number", 500000),
            InputField("r", "Annual interest rate (%)", "number", 8),
            InputField("t", "Tenure (years)", "number", 5),
        ]

    def calculate(self, values):
        p, r, t = self.num(values, "p"), self.num(values, "r"), self.num(values, "t")
        if t <= 0:
            raise ValueError("Tenure must be positive")
        n = t * 12
        i = r / 100 / 12
        if i == 0:
            emi = p / n
        else:
            emi = p * i * (1 + i) ** n / ((1 + i) ** n - 1)
        total = emi * n
        return [
            CalcResult("Monthly EMI", money(emi)),
            CalcResult("Total Payment", money(total), f"EMI × {n} months"),
            CalcResult("Total Interest", money(total - p)),
        ]


class LoanEligibilityCalc(Calculator):
    id = "fin_loan_elig"
    name = "Loan Eligibility"
    category = "Financial Calculations"
    description = "Estimate loan amount based on income and existing EMIs"
    icon = "✅"
    example = "Salary=60000 → eligible ≈ 3,600,000"

    def get_inputs(self):
        return [
            InputField("income", "Monthly income", "number", 60000),
            InputField("existing_emi", "Existing EMIs per month", "number", 0),
            InputField("rate", "Interest rate (%)", "number", 8),
            InputField("tenure", "Tenure (years)", "number", 10),
            InputField("foir", "FOIR % (max income share for EMI)", "number", 50),
        ]

    def calculate(self, values):
        income = self.num(values, "income")
        existing = self.num(values, "existing_emi")
        rate = self.num(values, "rate")
        tenure = self.num(values, "tenure")
        foir = self.num(values, "foir") / 100
        avail = max(income * foir - existing, 0)
        n = tenure * 12
        i = rate / 100 / 12
        if i == 0:
            principal = avail * n
        else:
            principal = avail * ((1 + i) ** n - 1) / (i * (1 + i) ** n)
        total_pay = avail * n
        return [
            CalcResult("Max affordable EMI", money(avail)),
            CalcResult("Estimated eligible loan", money(principal)),
            CalcResult("Total interest payable", money(total_pay - principal)),
        ]


class MortgageCalc(Calculator):
    id = "fin_mortgage"
    name = "Mortgage / Home Loan"
    category = "Financial Calculations"
    description = "Monthly payment and amortization summary for a mortgage"
    icon = "🏡"
    example = "P=300000, 4%, 30y → monthly ≈ 1,432"

    def get_inputs(self):
        return [
            InputField("p", "Loan amount", "number", 300000),
            InputField("r", "Annual rate (%)", "number", 4),
            InputField("t", "Years", "number", 30),
            InputField("extra", "Extra monthly payment", "number", 0, required=False),
        ]

    def calculate(self, values):
        p, r, t = self.num(values, "p"), self.num(values, "r"), self.num(values, "t")
        extra = self.num(values, "extra")
        n = t * 12
        i = r / 100 / 12
        if i == 0:
            base = p / n
        else:
            base = p * i * (1 + i) ** n / ((1 + i) ** n - 1)
        total_base = base * n
        # with extra payment
        if extra > 0:
            bal = p
            months = 0
            total_paid = 0
            while bal > 0 and months < 1200:
                months += 1
                interest = bal * i
                paid = base + extra
                bal = bal + interest - paid
                total_paid += paid
            payoff_months = months
            payoff_years = payoff_months // 12
            payoff_m = payoff_months % 12
            return [
                CalcResult("Monthly Payment", money(base)),
                CalcResult("Total Payment (base)", money(total_base)),
                CalcResult("Total Interest (base)", money(total_base - p)),
                CalcResult("With extra payment, payoff time", f"{payoff_years}y {payoff_m}m"),
                CalcResult("Interest saved with extra", money(total_base - total_paid)),
            ]
        return [
            CalcResult("Monthly Payment", money(base)),
            CalcResult("Total Payment", money(total_base)),
            CalcResult("Total Interest", money(total_base - p)),
            CalcResult("Note", "Add an extra monthly payment to shorten the loan"),
        ]


class CreditCardInterestCalc(Calculator):
    id = "fin_cc"
    name = "Credit Card Interest"
    category = "Financial Calculations"
    description = "Interest on outstanding credit card balance"
    icon = "💳"
    example = "Balance=5000, 24%, 3 months"

    def get_inputs(self):
        return [
            InputField("bal", "Outstanding balance", "number", 5000),
            InputField("rate", "Annual interest rate (%)", "number", 24),
            InputField("months", "Months unpaid", "number", 3),
        ]

    def calculate(self, values):
        bal, rate, months = self.num(values, "bal"), self.num(values, "rate"), self.num(values, "months")
        i = rate / 100 / 12
        total = bal * (1 + i) ** months
        return [
            CalcResult("Interest charged", money(total - bal)),
            CalcResult("Total owed after", money(total)),
            CalcResult("Effective annual rate", f"{fmt(((1 + i) ** 12 - 1) * 100, 4)}%"),
        ]


class SavingsGrowthCalc(Calculator):
    id = "fin_savings"
    name = "Savings Growth"
    category = "Financial Calculations"
    description = "Future value of a lump sum at compound interest"
    icon = "🐷"
    example = "10000 at 6% for 10y = 17,908"

    def get_inputs(self):
        return [
            InputField("p", "Initial deposit", "number", 10000),
            InputField("r", "Annual rate (%)", "number", 6),
            InputField("t", "Years", "number", 10),
            InputField("monthly", "Monthly addition", "number", 0, required=False),
        ]

    def calculate(self, values):
        p, r, t = self.num(values, "p"), self.num(values, "r"), self.num(values, "t")
        monthly = self.num(values, "monthly")
        i = r / 100 / 12
        n = t * 12
        fv = p * (1 + i) ** n
        fv_add = monthly * ((1 + i) ** n - 1) / i if i > 0 else monthly * n
        total = fv + fv_add
        invested = p + monthly * n
        return [
            CalcResult("Future value", money(total)),
            CalcResult("Lump sum growth", money(fv)),
            CalcResult("Monthly additions growth", money(fv_add)),
            CalcResult("Total invested", money(invested)),
            CalcResult("Interest earned", money(total - invested)),
        ]


class FDCalc(Calculator):
    id = "fin_fd"
    name = "Fixed Deposit (FD)"
    category = "Financial Calculations"
    description = "Maturity amount of a fixed deposit"
    icon = "🏦"
    example = "100000 at 7% for 5y = 141,474"

    def get_inputs(self):
        return [
            InputField("p", "Deposit amount", "number", 100000),
            InputField("r", "Annual rate (%)", "number", 7),
            InputField("t", "Years", "number", 5),
            InputField("n", "Compounds per year", "select", 4, options=["1", "2", "4", "12"]),
        ]

    def calculate(self, values):
        p, r, t = self.num(values, "p"), self.num(values, "r"), self.num(values, "t")
        n = float(values.get("n", 4))
        i = r / 100 / n
        maturity = p * (1 + i) ** (n * t)
        return [
            CalcResult("Maturity amount", money(maturity)),
            CalcResult("Interest earned", money(maturity - p)),
            CalcResult("Effective annual yield", f"{fmt(((1 + i) ** n - 1) * 100, 4)}%"),
        ]


class RDCalc(Calculator):
    id = "fin_rd"
    name = "Recurring Deposit (RD)"
    category = "Financial Calculations"
    description = "Maturity value of monthly recurring deposits"
    icon = "📅"
    example = "5000/mo at 7% for 5y = 358,960"

    def get_inputs(self):
        return [
            InputField("p", "Monthly deposit", "number", 5000),
            InputField("r", "Annual rate (%)", "number", 7),
            InputField("t", "Years", "number", 5),
        ]

    def calculate(self, values):
        p, r, t = self.num(values, "p"), self.num(values, "r"), self.num(values, "t")
        n = t * 12
        i = r / 100 / 12
        if i == 0:
            mv = p * n
        else:
            mv = p * ((1 + i) ** n - 1) / i * (1 + i)
        invested = p * n
        return [
            CalcResult("Maturity value", money(mv)),
            CalcResult("Total invested", money(invested)),
            CalcResult("Interest earned", money(mv - invested)),
        ]


class InvestmentReturnsCalc(Calculator):
    id = "fin_investment"
    name = "Investment Returns"
    category = "Financial Calculations"
    description = "Simple annualized return on investment"
    icon = "📊"
    example = "1000 → 1600 in 3y = 16.96%/yr"

    def get_inputs(self):
        return [
            InputField("p", "Amount invested", "number", 1000),
            InputField("fv", "Final value", "number", 1600),
            InputField("years", "Years held", "number", 3),
        ]

    def calculate(self, values):
        p, fv, years = self.num(values, "p"), self.num(values, "fv"), self.num(values, "years")
        if p == 0 or years == 0:
            raise ValueError("Investment and years must be non-zero")
        cagr = ((fv / p) ** (1 / years) - 1) * 100
        total_return = (fv - p) / p * 100
        return [
            CalcResult("Total return", f"{fmt(total_return, 4)}%"),
            CalcResult("CAGR (annualized)", f"{fmt(cagr, 4)}%"),
            CalcResult("Absolute gain", money(fv - p)),
        ]


class SIPCalc(Calculator):
    id = "fin_sip"
    name = "SIP Returns"
    category = "Financial Calculations"
    description = "Systematic Investment Plan future value"
    icon = "📈"
    example = "5000/mo, 12%/yr, 10y = 1,161,695"

    def get_inputs(self):
        return [
            InputField("p", "Monthly investment", "number", 5000),
            InputField("r", "Expected annual return (%)", "number", 12),
            InputField("t", "Years", "number", 10),
        ]

    def calculate(self, values):
        p, r, t = self.num(values, "p"), self.num(values, "r"), self.num(values, "t")
        n = t * 12
        i = r / 100 / 12
        if i == 0:
            fv = p * n
        else:
            fv = p * ((1 + i) ** n - 1) / i * (1 + i)
        invested = p * n
        return [
            CalcResult("Future value", money(fv)),
            CalcResult("Amount invested", money(invested)),
            CalcResult("Estimated returns", money(fv - invested)),
            CalcResult("Wealth gain factor", f"{fmt(fv / invested, 2)}×"),
        ]


class MutualFundReturnsCalc(Calculator):
    id = "fin_mf"
    name = "Mutual Fund Returns"
    category = "Financial Calculations"
    description = "Lumpsum or SIP mutual fund future value"
    icon = "💼"
    example = "Lumpsum 100000, 12%, 5y = 176,234"

    def get_inputs(self):
        return [
            InputField("p", "Investment amount", "number", 100000),
            InputField("r", "Expected annual return (%)", "number", 12),
            InputField("t", "Years", "number", 5),
            InputField("mode", "Investment mode", "select", "Lumpsum", options=["Lumpsum", "SIP Monthly"]),
        ]

    def calculate(self, values):
        p, r, t = self.num(values, "p"), self.num(values, "r"), self.num(values, "t")
        mode = values.get("mode", "Lumpsum")
        if mode == "SIP Monthly":
            n = t * 12
            i = r / 100 / 12
            fv = p * ((1 + i) ** n - 1) / i * (1 + i) if i else p * n
            invested = p * n
        else:
            i = r / 100
            fv = p * (1 + i) ** t
            invested = p
        return [
            CalcResult("Future value", money(fv)),
            CalcResult("Amount invested", money(invested)),
            CalcResult("Returns", money(fv - invested)),
            CalcResult("Growth factor", f"{fmt(fv / invested, 2)}×"),
        ]


class StockProfitLossCalc(Calculator):
    id = "fin_stock"
    name = "Stock Profit / Loss"
    category = "Financial Calculations"
    description = "Profit/loss from buying and selling shares"
    icon = "📉"
    example = "Buy 10@100, sell@120 → +200"

    def get_inputs(self):
        return [
            InputField("qty", "Quantity of shares", "number", 10),
            InputField("buy", "Buy price per share", "number", 100),
            InputField("sell", "Sell price per share", "number", 120),
            InputField("brokerage", "Brokerage (%)", "number", 0.1, required=False),
        ]

    def calculate(self, values):
        qty, buy, sell = self.num(values, "qty"), self.num(values, "buy"), self.num(values, "sell")
        b = self.num(values, "brokerage") / 100
        cost = qty * buy * (1 + b)
        proceeds = qty * sell * (1 - b)
        pl = proceeds - cost
        return [
            CalcResult("Total cost (incl. brokerage)", money(cost)),
            CalcResult("Total proceeds", money(proceeds)),
            CalcResult("Profit / Loss", money(pl)),
            CalcResult("Return %", f"{fmt(pl / cost * 100 if cost else 0, 4)}%"),
        ]


class CapitalGainsCalc(Calculator):
    id = "fin_capital_gains"
    name = "Capital Gains"
    category = "Financial Calculations"
    description = "Short/long-term capital gain on asset sale"
    icon = "🏛️"
    example = "Buy 50000, sell 80000 → gain 30000"

    def get_inputs(self):
        return [
            InputField("buy", "Purchase price", "number", 50000),
            InputField("sell", "Sale price", "number", 80000),
            InputField("expenses", "Brokerage/expenses", "number", 500, required=False),
            InputField("holding", "Holding period (months)", "number", 24),
        ]

    def calculate(self, values):
        buy, sell = self.num(values, "buy"), self.num(values, "sell")
        expenses = self.num(values, "expenses")
        holding = int(self.num(values, "holding"))
        gain = sell - buy - expenses
        gain_pct = gain / buy * 100 if buy else 0
        holding_years = holding / 12
        annualized = ((sell / buy) ** (1 / holding_years) - 1) * 100 if buy > 0 and holding_years > 0 else 0
        term = "Long-term" if holding > 12 else "Short-term"
        return [
            CalcResult(f"Capital gain ({term})", money(gain)),
            CalcResult("Gain %", f"{fmt(gain_pct, 4)}%"),
            CalcResult("Annualized return", f"{fmt(annualized, 4)}%"),
            CalcResult("Holding period", f"{holding} months ({holding / 12:.1f} years)"),
        ]


class TaxCalc(Calculator):
    id = "fin_tax"
    name = "Tax Calculation"
    category = "Financial Calculations"
    description = "Estimate income tax with marginal slabs"
    icon = "🧾"
    example = "Income 800000, deductions 100000 → tax slab-based"

    def get_inputs(self):
        return [
            InputField("income", "Annual income", "number", 800000),
            InputField("deductions", "Deductions (80C, etc.)", "number", 150000),
            InputField("regime", "Tax regime", "select", "Old", options=["Old", "New"]),
        ]

    def calculate(self, values):
        income = self.num(values, "income")
        deductions = self.num(values, "deductions")
        regime = values.get("regime", "Old")
        if regime == "Old":
            slabs = [(250000, 0), (500000, 5), (1000000, 20), (float("inf"), 30)]
            taxable = max(income - deductions, 0)
        else:
            slabs = [(300000, 0), (700000, 5), (1000000, 10), (1500000, 15), (float("inf"), 20)]
            taxable = income
        tax = 0
        prev = 0
        for limit, rate in slabs:
            if taxable > prev:
                tax += (min(taxable, limit) - prev) * rate / 100
            prev = limit
        cess = tax * 0.04
        return [
            CalcResult("Taxable income", money(taxable)),
            CalcResult("Income tax", money(tax)),
            CalcResult("Health & education cess (4%)", money(cess)),
            CalcResult("Total tax liability", money(tax + cess)),
            CalcResult(f"Effective tax rate", f"{fmt((tax + cess) / income * 100 if income else 0, 2)}%"),
        ]


class GSTVATCalc(Calculator):
    id = "fin_gst"
    name = "GST / VAT"
    category = "Financial Calculations"
    description = "Add or remove tax from a price"
    icon = "🏷️"
    example = "1000 + 18% GST = 1180"

    def get_inputs(self):
        return [
            InputField("amount", "Amount (excl. or incl. tax)", "number", 1000),
            InputField("rate", "Tax rate (%)", "number", 18),
            InputField("mode", "Mode", "select", "Add tax", options=["Add tax", "Remove tax"]),
        ]

    def calculate(self, values):
        amount, rate = self.num(values, "amount"), self.num(values, "rate")
        mode = values.get("mode", "Add tax")
        if mode == "Add tax":
            tax = amount * rate / 100
            total = amount + tax
        else:
            total = amount
            tax = amount * rate / (100 + rate)
            base = amount - tax
        return [
            CalcResult("Tax amount", money(tax), f"{fmt(rate)}% of base"),
            CalcResult("Net/Gross amount", money(total)),
        ]


class DiscountCalc(Calculator):
    id = "fin_discount"
    name = "Discounts"
    category = "Financial Calculations"
    description = "Discounted price and savings"
    icon = "💰"
    example = "Price 500, 10% off → 450"

    def get_inputs(self):
        return [
            InputField("price", "Original price", "number", 500),
            InputField("discount", "Discount (%)", "number", 10),
        ]

    def calculate(self, values):
        price, discount = self.num(values, "price"), self.num(values, "discount")
        saved = price * discount / 100
        final_price = price - saved
        return [
            CalcResult("You save", money(saved)),
            CalcResult("Final price", money(final_price)),
            CalcResult("Price after 1st discount only", money(final_price)),
        ]


class ProfitLossCalc(Calculator):
    id = "fin_profit_loss"
    name = "Profit & Loss"
    category = "Financial Calculations"
    description = "Profit/loss, cost and selling price calculations"
    icon = "⚖️"
    example = "CP=800, SP=1000 → profit 200 (25%)"

    def get_inputs(self):
        return [
            InputField("cp", "Cost price", "number", 800),
            InputField("sp", "Selling price", "number", 1000),
        ]

    def calculate(self, values):
        cp, sp = self.num(values, "cp"), self.num(values, "sp")
        diff = sp - cp
        kind = "Profit" if diff > 0 else "Loss" if diff < 0 else "No profit / no loss"
        pct = abs(diff) / cp * 100 if cp else 0
        margin = diff / sp * 100 if sp else 0
        return [
            CalcResult(kind, money(diff)),
            CalcResult(f"{kind} %", f"{fmt(pct, 4)}%"),
            CalcResult("Profit margin (on selling price)", f"{fmt(margin, 4)}%"),
        ]


class BreakEvenCalc(Calculator):
    id = "fin_breakeven"
    name = "Break-Even Analysis"
    category = "Financial Calculations"
    description = "Break-even point in units and revenue"
    icon = "📊"
    example = "FC=50000, SP=100, VC=60 → BEP=1250"

    def get_inputs(self):
        return [
            InputField("fc", "Fixed costs", "number", 50000),
            InputField("vc", "Variable cost per unit", "number", 60),
            InputField("sp", "Selling price per unit", "number", 100),
        ]

    def calculate(self, values):
        fc, vc, sp = self.num(values, "fc"), self.num(values, "vc"), self.num(values, "sp")
        cm = sp - vc
        if cm <= 0:
            raise ValueError("Selling price must exceed variable cost")
        units = fc / cm
        revenue = units * sp
        return [
            CalcResult("Contribution margin per unit", money(cm)),
            CalcResult("Break-even (units)", round(units)),
            CalcResult("Break-even (revenue)", money(revenue), "Units × Selling price"),
            CalcResult("Contribution margin ratio", f"{fmt(cm / sp * 100, 2)}%"),
        ]


class SalaryCalc(Calculator):
    id = "fin_salary"
    name = "Salary (Net Pay)"
    category = "Financial Calculations"
    description = "Net salary after tax and deductions"
    icon = "💵"
    example = "Gross 60000, tax 8%, pf 12%"

    def get_inputs(self):
        return [
            InputField("gross", "Gross monthly salary", "number", 60000),
            InputField("tax", "Tax deduction (%)", "number", 8),
            InputField("pf", "PF deduction (%)", "number", 12),
            InputField("other", "Other deductions", "number", 0, required=False),
        ]

    def calculate(self, values):
        gross, tax, pf = self.num(values, "gross"), self.num(values, "tax"), self.num(values, "pf")
        other = self.num(values, "other")
        tax_amt = gross * tax / 100
        pf_amt = gross * pf / 100
        net = gross - tax_amt - pf_amt - other
        return [
            CalcResult("Gross salary", money(gross)),
            CalcResult("Tax deducted", money(tax_amt)),
            CalcResult("PF deducted", money(pf_amt)),
            CalcResult("Other deductions", money(other)),
            CalcResult("Net salary (take-home)", money(net)),
            CalcResult("Annual net salary", money(net * 12)),
        ]


class BonusCalc(Calculator):
    id = "fin_bonus"
    name = "Bonus"
    category = "Financial Calculations"
    description = "Bonus amount based on salary and percentage"
    icon = "🎁"
    example = "Salary 50000, 10% bonus = 5000"

    def get_inputs(self):
        return [
            InputField("salary", "Monthly salary", "number", 50000),
            InputField("pct", "Bonus (%)", "number", 10),
            InputField("months", "Months of bonus pay", "number", 1, required=False),
        ]

    def calculate(self, values):
        salary, pct = self.num(values, "salary"), self.num(values, "pct")
        months = self.num(values, "months") or 1
        bonus = salary * pct / 100 * months
        return [
            CalcResult("Bonus amount", money(bonus)),
            CalcResult("Total with salary", money(salary + bonus)),
        ]


class OvertimeCalc(Calculator):
    id = "fin_overtime"
    name = "Overtime Pay"
    category = "Financial Calculations"
    description = "Overtime wages based on hourly rate"
    icon = "⏰"
    example = "Rate 200/hr, 20 OT hrs at 1.5× = 6000"

    def get_inputs(self):
        return [
            InputField("rate", "Hourly rate", "number", 200),
            InputField("hours", "Overtime hours", "number", 20),
            InputField("mult", "OT multiplier", "number", 1.5, required=False),
        ]

    def calculate(self, values):
        rate, hours = self.num(values, "rate"), self.num(values, "hours")
        mult = self.num(values, "mult") or 1.5
        ot = rate * hours * mult
        return [
            CalcResult("Overtime pay", money(ot)),
            CalcResult("OT rate per hour", money(rate * mult)),
        ]


class CommissionCalc(Calculator):
    id = "fin_commission"
    name = "Commission"
    category = "Financial Calculations"
    description = "Commission earned on sales"
    icon = "🤝"
    example = "Sales 100000, 5% commission = 5000"

    def get_inputs(self):
        return [
            InputField("sales", "Total sales", "number", 100000),
            InputField("rate", "Commission rate (%)", "number", 5),
        ]

    def calculate(self, values):
        sales, rate = self.num(values, "sales"), self.num(values, "rate")
        commission = sales * rate / 100
        return [
            CalcResult("Commission", money(commission)),
            CalcResult("Amount after commission", money(sales - commission)),
        ]


CURRENCIES = {
    "USD": {"name": "US Dollar", "symbol": "$"},
    "EUR": {"name": "Euro", "symbol": "€"},
    "GBP": {"name": "British Pound", "symbol": "£"},
    "INR": {"name": "Indian Rupee", "symbol": "₹"},
    "JPY": {"name": "Japanese Yen", "symbol": "¥"},
    "AUD": {"name": "Australian Dollar", "symbol": "A$"},
    "CAD": {"name": "Canadian Dollar", "symbol": "C$"},
    "CNY": {"name": "Chinese Yuan", "symbol": "¥"},
    "SGD": {"name": "Singapore Dollar", "symbol": "S$"},
    "AED": {"name": "UAE Dirham", "symbol": "د.إ"},
    "PHP": {"name": "Philippine Peso", "symbol": "₱"},
    "IDR": {"name": "Indonesian Rupiah", "symbol": "Rp"},
}

# Base rate: 1 USD worth of each currency (approx. daily rates)
FX_RATES = {
    "USD": 1.0, "EUR": 0.92, "GBP": 0.79, "INR": 83.2, "JPY": 149.5,
    "AUD": 1.52, "CAD": 1.36, "CNY": 7.24, "SGD": 1.34, "AED": 3.67,
    "PHP": 56.3, "IDR": 15700,
}


class CurrencyConversionCalc(Calculator):
    id = "fin_currency"
    name = "Currency Conversion"
    category = "Financial Calculations"
    description = "Convert between major world currencies"
    icon = "🌍"
    example = "100 USD = 8,320 INR"

    def get_inputs(self):
        return [
            InputField("amount", "Amount", "number", 100),
            InputField("from", "From currency", "select", "USD", options=list(CURRENCIES.keys())),
            InputField("to", "To currency", "select", "INR", options=list(CURRENCIES.keys())),
        ]

    def calculate(self, values):
        amount = self.num(values, "amount")
        c_from = values.get("from", "USD")
        c_to = values.get("to", "INR")
        rate = FX_RATES[c_to] / FX_RATES[c_from]
        converted = amount * rate
        sym_f = CURRENCIES[c_from]["symbol"]
        sym_t = CURRENCIES[c_to]["symbol"]
        return [
            CalcResult(f"{sym_f}{fmt(amount, 2)} = {sym_t}{fmt(converted, 2)}", converted, f"1 {c_from} = {fmt(rate, 4)} {c_to}"),
            CalcResult("Exchange rate", f"1 {c_from} = {fmt(rate, 4)} {c_to}"),
            CalcResult("Inverse rate", f"1 {c_to} = {fmt(1 / rate, 4)} {c_from}"),
        ]


class InflationCalc(Calculator):
    id = "fin_inflation"
    name = "Inflation"
    category = "Financial Calculations"
    description = "Future cost due to inflation"
    icon = "🎈"
    example = "1000 today at 6% inflation for 10y = 1,791"

    def get_inputs(self):
        return [
            InputField("amount", "Current amount", "number", 1000),
            InputField("rate", "Inflation rate (%)", "number", 6),
            InputField("years", "Years in future", "number", 10),
        ]

    def calculate(self, values):
        amount, rate, years = self.num(values, "amount"), self.num(values, "rate"), self.num(values, "years")
        future = amount * (1 + rate / 100) ** years
        buying_power = amount / (1 + rate / 100) ** years
        return [
            CalcResult("Future cost", money(future), f"{amount} × (1.06)^{years}"),
            CalcResult("Today's buying power of same future amount", money(buying_power)),
            CalcResult("Increase", money(future - amount)),
        ]
