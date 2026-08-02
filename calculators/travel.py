"""Travel calculators."""
import math
from .base import Calculator, CalcResult, InputField, fmt, money


class FuelCostCalc(Calculator):
    id = "travel_fuel_cost"
    name = "Fuel Cost"
    category = "Travel"
    description = "Total fuel cost for a trip"
    icon = "⛽"
    example = "500 km at 8 L/100km, $1.5/L → $60"

    def get_inputs(self):
        return [
            InputField("distance", "Distance (km)", "number", 500),
            InputField("efficiency", "Fuel consumption (L/100km)", "number", 8),
            InputField("price", "Fuel price per litre", "number", 1.5),
        ]

    def calculate(self, values):
        dist = self.num(values, "distance")
        eff = self.num(values, "efficiency")
        price = self.num(values, "price")
        litres = dist * eff / 100
        cost = litres * price
        return [
            CalcResult("Fuel needed", f"{fmt(litres, 2)} L"),
            CalcResult("Fuel cost", money(cost), "Litres × price"),
            CalcResult("Cost per km", money(cost / dist if dist else 0)),
        ]


class MileageCalc(Calculator):
    id = "travel_mileage"
    name = "Mileage"
    category = "Travel"
    description = "Vehicle mileage (km per litre)"
    icon = "🚗"
    example = "500 km on 40 L = 12.5 km/L"

    def get_inputs(self):
        return [
            InputField("distance", "Distance (km)", "number", 500),
            InputField("fuel", "Fuel used (L)", "number", 40),
        ]

    def calculate(self, values):
        dist, fuel = self.num(values, "distance"), self.num(values, "fuel")
        if fuel == 0:
            raise ValueError("Fuel used cannot be zero")
        mileage = dist / fuel
        return [
            CalcResult("Mileage", f"{fmt(mileage, 2)} km/L"),
            CalcResult("In mpg (US)", f"{fmt(mileage * 2.35215, 2)} mpg"),
            CalcResult("Fuel per 100 km", f"{fmt(100 / mileage, 2)} L/100km"),
        ]


class TravelTimeCalc(Calculator):
    id = "travel_time"
    name = "Travel Time"
    category = "Travel"
    description = "Time to travel a distance at given speed"
    icon = "🕐"
    example = "300 km at 80 km/h = 3h 45m"

    def get_inputs(self):
        return [
            InputField("distance", "Distance (km)", "number", 300),
            InputField("speed", "Average speed (km/h)", "number", 80),
        ]

    def calculate(self, values):
        dist, speed = self.num(values, "distance"), self.num(values, "speed")
        if speed <= 0:
            raise ValueError("Speed must be positive")
        hours = dist / speed
        h = int(hours)
        m = round((hours - h) * 60)
        if m == 60:
            h += 1
            m = 0
        return [
            CalcResult("Travel time", f"{h} hours {m} minutes"),
            CalcResult("In hours (decimal)", f"{fmt(hours, 2)}"),
            CalcResult("In minutes", fmt(hours * 60, 0)),
        ]


class DistanceCalc(Calculator):
    id = "travel_distance"
    name = "Distance"
    category = "Travel"
    description = "Distance from speed and time"
    icon = "📍"
    example = "80 km/h × 2.5h = 200 km"

    def get_inputs(self):
        return [
            InputField("speed", "Speed (km/h)", "number", 80),
            InputField("time_h", "Time (hours)", "number", 2.5),
        ]

    def calculate(self, values):
        speed, time = self.num(values, "speed"), self.num(values, "time_h")
        dist = speed * time
        return [
            CalcResult("Distance", f"{fmt(dist, 2)} km"),
            CalcResult("In miles", f"{fmt(dist * 0.621371, 2)} mi"),
        ]


class HotelCostCalc(Calculator):
    id = "travel_hotel"
    name = "Hotel Cost"
    category = "Travel"
    description = "Total hotel cost including taxes"
    icon = "🏨"
    example = "3 nights × $120 + 12% tax = $403.2"

    def get_inputs(self):
        return [
            InputField("nights", "Number of nights", "number", 3),
            InputField("rate", "Rate per night", "number", 120),
            InputField("tax", "Tax rate (%)", "number", 12),
        ]

    def calculate(self, values):
        nights, rate = self.num(values, "nights"), self.num(values, "rate")
        tax = self.num(values, "tax") / 100
        subtotal = nights * rate
        tax_amt = subtotal * tax
        total = subtotal + tax_amt
        return [
            CalcResult("Subtotal", money(subtotal)),
            CalcResult("Tax", money(tax_amt)),
            CalcResult("Total stay cost", money(total)),
            CalcResult("Per night incl. tax", money(total / nights if nights else 0)),
        ]


class TripBudgetCalc(Calculator):
    id = "travel_budget"
    name = "Trip Budget"
    category = "Travel"
    description = "Estimate total trip budget"
    icon = "💼"
    example = "Transport 200 + hotel 300 + food 150 + misc 50 = 700"

    def get_inputs(self):
        return [
            InputField("transport", "Transport", "number", 200),
            InputField("hotel", "Accommodation", "number", 300),
            InputField("food", "Food", "number", 150),
            InputField("activities", "Activities", "number", 50),
            InputField("misc", "Miscellaneous", "number", 50, required=False),
        ]

    def calculate(self, values):
        t = self.num(values, "transport")
        h = self.num(values, "hotel")
        f = self.num(values, "food")
        a = self.num(values, "activities")
        m = self.num(values, "misc")
        total = t + h + f + a + m
        return [
            CalcResult("Total budget", money(total)),
            CalcResult("Transport share", f"{fmt(t / total * 100 if total else 0, 1)}%"),
            CalcResult("Accommodation share", f"{fmt(h / total * 100 if total else 0, 1)}%"),
            CalcResult("Food share", f"{fmt(f / total * 100 if total else 0, 1)}%"),
            CalcResult("Activities share", f"{fmt(a / total * 100 if total else 0, 1)}%"),
            CalcResult("Misc share", f"{fmt(m / total * 100 if total else 0, 1)}%"),
        ]


class CurrencyExchangeTravelCalc(Calculator):
    id = "travel_currency"
    name = "Currency Exchange"
    category = "Travel"
    description = "Convert currency for travel"
    icon = "💱"
    example = "100 USD to EUR at 0.92 → 92 EUR"

    def get_inputs(self):
        return [
            InputField("amount", "Amount", "number", 100),
            InputField("rate", "Exchange rate (target per 1 base)", "number", 0.92),
        ]

    def calculate(self, values):
        amount, rate = self.num(values, "amount"), self.num(values, "rate")
        converted = amount * rate
        return [
            CalcResult("Converted amount", money(converted)),
            CalcResult("Rate applied", f"1 : {fmt(rate, 4)}"),
            CalcResult("Inverse", f"1 : {fmt(1 / rate if rate else 0, 4)}"),
        ]
