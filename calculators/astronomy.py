"""Astronomy calculators."""
import math
from datetime import datetime, timedelta
from .base import Calculator, CalcResult, InputField, fmt


class SunriseSunsetCalc(Calculator):
    id = "astro_sunrise"
    name = "Sunrise & Sunset"
    category = "Astronomy"
    description = "Approximate sunrise/sunset times"
    icon = "🌅"
    example = "Latitude 28.6°, longitude 77.2°, Jan 1"

    def get_inputs(self):
        return [
            InputField("lat", "Latitude", "number", 28.6),
            InputField("lon", "Longitude", "number", 77.2),
            InputField("date", "Date", "date", "2025-01-01"),
        ]

    def calculate(self, values):
        lat = self.num(values, "lat")
        lon = self.num(values, "lon")
        raw = str(values.get("date", "2025-01-01"))
        try:
            d = datetime.strptime(raw, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Enter a valid date (YYYY-MM-DD)")
        N = d.timetuple().tm_yday
        # Solar declination approximation
        decl = 23.44 * math.sin(math.radians(360 / 365 * (N - 81)))
        lat_r = math.radians(lat)
        decl_r = math.radians(decl)
        cos_ha = -math.tan(lat_r) * math.tan(decl_r)
        if cos_ha < -1 or cos_ha > 1:
            raise ValueError("Polar day/night — no sunrise/sunset on this date")
        ha = math.degrees(math.acos(cos_ha))
        # Solar noon in minutes UTC
        solar_noon = 720 - 4 * lon - 1 * (math.sin(math.radians(360 / 365 * (N - 81))))
        sunrise = (solar_noon - ha * 4) / 60
        sunset = (solar_noon + ha * 4) / 60
        def fmt_h(h):
            h = h % 24
            hh = int(h)
            mm = int((h - hh) * 60)
            return f"{hh:02d}:{mm:02d}"
        day_length = ha * 8  # minutes
        return [
            CalcResult("Sunrise (approx)", fmt_h(sunrise)),
            CalcResult("Sunset (approx)", fmt_h(sunset)),
            CalcResult("Solar noon", fmt_h(solar_noon / 60)),
            CalcResult("Day length", f"{int(day_length // 60)}h {int(day_length % 60)}m"),
        ]


class MoonPhasesCalc(Calculator):
    id = "astro_moon"
    name = "Moon Phase"
    category = "Astronomy"
    description = "Moon phase on a given date"
    icon = "🌙"
    example = "New moon cycle approximation"

    def get_inputs(self):
        return [
            InputField("date", "Date", "date", "2025-01-01"),
        ]

    def calculate(self, values):
        raw = str(values.get("date", "2025-01-01"))
        try:
            d = datetime.strptime(raw, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Enter a valid date (YYYY-MM-DD)")
        # Known new moon: 2000-01-06 18:14 UTC
        ref = datetime(2000, 1, 6, 18, 14)
        days = (d - ref).days + (d - ref).seconds / 86400
        synodic = 29.53058867
        phase = (days % synodic) / synodic
        if phase < 0.025:
            name = "New Moon"
        elif phase < 0.225:
            name = "Waxing Crescent"
        elif phase < 0.275:
            name = "First Quarter"
        elif phase < 0.475:
            name = "Waxing Gibbous"
        elif phase < 0.525:
            name = "Full Moon"
        elif phase < 0.725:
            name = "Waning Gibbous"
        elif phase < 0.775:
            name = "Last Quarter"
        elif phase < 0.975:
            name = "Waning Crescent"
        else:
            name = "New Moon"
        illum = (1 - math.cos(2 * math.pi * phase)) / 2 * 100
        return [
            CalcResult("Moon phase", name),
            CalcResult("Illumination", f"{fmt(illum, 1)}%"),
            CalcResult("Phase fraction", f"{fmt(phase, 4)} (0=new, 0.5=full)"),
            CalcResult("Days since new moon", f"{fmt(days % synodic, 1)} days"),
        ]


class PlanetDistanceCalc(Calculator):
    id = "astro_planet"
    name = "Planet Distances"
    category = "Astronomy"
    description = "Average distance of planets from the Sun"
    icon = "🪐"
    example = "Earth 149.6M km, light time 8.3 min"

    def get_inputs(self):
        return [
            InputField("planet", "Planet", "select", "Earth", options=[
                "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune",
            ]),
        ]

    def calculate(self, values):
        planet = values.get("planet", "Earth")
        data = {
            "Mercury": 57.9, "Venus": 108.2, "Earth": 149.6, "Mars": 227.9,
            "Jupiter": 778.5, "Saturn": 1433.5, "Uranus": 2872.5, "Neptune": 4495.1,
        }
        dist = data[planet]  # million km
        light_min = dist * 1e6 / 299792.458 / 60
        au = dist / 149.6
        return [
            CalcResult("Distance from Sun", f"{fmt(dist, 1)} million km"),
            CalcResult("In AU", f"{fmt(au, 3)} AU"),
            CalcResult("Light travel time", f"{fmt(light_min, 2)} minutes"),
        ]


class OrbitalPeriodCalc(Calculator):
    id = "astro_orbit"
    name = "Orbital Period"
    category = "Astronomy"
    description = "Orbital period using Kepler's Third Law"
    icon = "🛰️"
    example = "1 AU → 1 year"

    def get_inputs(self):
        return [
            InputField("a", "Semi-major axis (AU)", "number", 1),
            InputField("mass", "Central mass (solar masses)", "number", 1),
        ]

    def calculate(self, values):
        a, m = self.num(values, "a"), self.num(values, "mass")
        if a <= 0 or m <= 0:
            raise ValueError("Axis and mass must be positive")
        period_years = math.sqrt(a ** 3 / m)
        period_days = period_years * 365.25
        return [
            CalcResult("Orbital period", f"{fmt(period_years, 3)} years"),
            CalcResult("In days", f"{fmt(period_days, 1)} days"),
            CalcResult("Orbital velocity (approx)", f"{fmt(29.78 / math.sqrt(a) * math.sqrt(m) if a else 0, 2)} km/s"),
        ]
