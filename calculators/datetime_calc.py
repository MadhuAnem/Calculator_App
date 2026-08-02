"""Date & Time calculators."""
import math
from datetime import datetime, date, timedelta
from .base import Calculator, CalcResult, InputField, fmt


def _parse_date(raw, field="date"):
    if isinstance(raw, datetime):
        return raw.date()
    if isinstance(raw, date):
        return raw
    if isinstance(raw, str):
        for f in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(raw.strip(), f).date()
            except ValueError:
                continue
    raise ValueError(f"Enter a valid {field} (YYYY-MM-DD)")


class AgeCalculationCalc(Calculator):
    id = "dt_age"
    name = "Age Calculation"
    category = "Date & Time"
    description = "Exact age in years, months and days"
    icon = "🎂"
    example = "Born 1995-08-10 → today's age"

    def get_inputs(self):
        return [
            InputField("dob", "Date of birth", "date", "1995-08-10"),
        ]

    def calculate(self, values):
        dob = _parse_date(values.get("dob"))
        today = date.today()
        if dob > today:
            raise ValueError("Date of birth cannot be in the future")
        years = today.year - dob.year
        months = today.month - dob.month
        days = today.day - dob.day
        if days < 0:
            months -= 1
            prev_month = today.replace(day=1) - timedelta(days=1)
            days += prev_month.day
        if months < 0:
            years -= 1
            months += 12
        total_days = (today - dob).days
        total_weeks = total_days // 7
        total_months = years * 12 + months
        next_bday = dob.replace(year=today.year)
        if next_bday < today:
            try:
                next_bday = dob.replace(year=today.year + 1)
            except ValueError:
                next_bday = dob.replace(year=today.year + 1, day=28)
        days_to_next = (next_bday - today).days
        return [
            CalcResult("Age", f"{years} years, {months} months, {days} days"),
            CalcResult("Age in months", fmt(total_months)),
            CalcResult("Age in weeks", fmt(total_weeks)),
            CalcResult("Age in days", fmt(total_days)),
            CalcResult("Hours lived", fmt(total_days * 24)),
            CalcResult("Days until next birthday", fmt(days_to_next)),
        ]


class DaysBetweenDatesCalc(Calculator):
    id = "dt_days_between"
    name = "Days Between Dates"
    category = "Date & Time"
    description = "Number of days between two dates"
    icon = "📅"
    example = "01-Jan-2024 to 15-Mar-2024 = 74 days"

    def get_inputs(self):
        return [
            InputField("start", "Start date", "date", "2024-01-01"),
            InputField("end", "End date", "date", "2024-03-15"),
            InputField("incl", "Include end day?", "select", "No", options=["Yes", "No"]),
        ]

    def calculate(self, values):
        start = _parse_date(values.get("start"), "start date")
        end = _parse_date(values.get("end"), "end date")
        days = (end - start).days
        if values.get("incl", "No") == "Yes":
            days += 1
        return [
            CalcResult("Days between", fmt(abs(days))),
            CalcResult("Weeks", f"{fmt(abs(days) / 7, 2)}"),
            CalcResult("Months (approx 30.44 d)", f"{fmt(abs(days) / 30.44, 1)}"),
            CalcResult("Years (approx)", f"{fmt(abs(days) / 365.25, 2)}"),
        ]


class BusinessDaysCalc(Calculator):
    id = "dt_business_days"
    name = "Business Days"
    category = "Date & Time"
    description = "Working days between two dates (excl. weekends)"
    icon = "💼"
    example = "Jan 2024 (23 weekdays)"

    def get_inputs(self):
        return [
            InputField("start", "Start date", "date", "2024-01-01"),
            InputField("end", "End date", "date", "2024-01-31"),
        ]

    def calculate(self, values):
        start = _parse_date(values.get("start"), "start date")
        end = _parse_date(values.get("end"), "end date")
        days = (end - start).days
        if days < 0:
            raise ValueError("End date must be after start date")
        weekdays = 0
        weekends = 0
        for i in range(days + 1):
            d = start + timedelta(days=i)
            if d.weekday() < 5:
                weekdays += 1
            else:
                weekends += 1
        return [
            CalcResult("Business days (Mon-Fri)", fmt(weekdays)),
            CalcResult("Weekend days", fmt(weekends)),
            CalcResult("Total calendar days", fmt(days + 1)),
        ]


class LeapYearCalc(Calculator):
    id = "dt_leap_year"
    name = "Leap Year"
    category = "Date & Time"
    description = "Check if a year is a leap year"
    icon = "🐸"
    example = "2024 → Yes; 2100 → No"

    def get_inputs(self):
        return [
            InputField("year", "Year", "number", 2024),
        ]

    def calculate(self, values):
        year = int(self.num(values, "year"))
        is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        return [
            CalcResult("Is leap year?", "Yes" if is_leap else "No"),
            CalcResult("Days in year", 366 if is_leap else 365),
            CalcResult("Reason", f"{year} % 4, % 100, % 400 rules"),
        ]


class TimeDifferenceCalc(Calculator):
    id = "dt_time_diff"
    name = "Time Difference"
    category = "Date & Time"
    description = "Duration between two times"
    icon = "🕐"
    example = "09:30 to 17:45 = 8h 15m"

    def get_inputs(self):
        return [
            InputField("start_time", "Start time (HH:MM)", "text", "09:30"),
            InputField("end_time", "End time (HH:MM)", "text", "17:45"),
        ]

    def calculate(self, values):
        def parse_t(t):
            parts = str(t).strip().split(":")
            h = int(parts[0])
            m = int(parts[1]) if len(parts) > 1 else 0
            return h * 60 + m
        s = parse_t(values.get("start_time", "09:30"))
        e = parse_t(values.get("end_time", "17:45"))
        if e < s:
            e += 24 * 60
        diff = e - s
        h, m = divmod(diff, 60)
        return [
            CalcResult("Time difference", f"{h} hours {m} minutes"),
            CalcResult("In minutes", fmt(diff)),
            CalcResult("In hours", f"{fmt(diff / 60, 2)}"),
        ]


class CountdownCalc(Calculator):
    id = "dt_countdown"
    name = "Countdown"
    category = "Date & Time"
    description = "Time remaining until a target date"
    icon = "⏳"
    example = "2025-01-01 from today"

    def get_inputs(self):
        return [
            InputField("target", "Target date", "date", "2025-01-01"),
        ]

    def calculate(self, values):
        target = _parse_date(values.get("target"), "target date")
        today = date.today()
        diff = (target - today).days
        if diff < 0:
            status = "Date has passed"
            diff = abs(diff)
        else:
            status = "Upcoming"
        weeks = diff // 7
        rem = diff % 7
        return [
            CalcResult("Status", status),
            CalcResult("Days remaining/passed", fmt(diff)),
            CalcResult("Weeks + days", f"{weeks} weeks {rem} days"),
            CalcResult("Hours", fmt(diff * 24)),
            CalcResult("Minutes", fmt(diff * 1440)),
        ]


class TimeZoneConversionCalc(Calculator):
    id = "dt_timezone"
    name = "Time Zone Conversion"
    category = "Date & Time"
    description = "Convert time between time zones"
    icon = "🌐"
    example = "12:00 UTC = 17:30 IST"

    def get_inputs(self):
        return [
            InputField("time", "Time (HH:MM)", "text", "12:00"),
            InputField("from_offset", "From UTC offset (hours)", "number", 0),
            InputField("to_offset", "To UTC offset (hours)", "number", 5.5),
        ]

    def calculate(self, values):
        parts = str(values.get("time", "12:00")).strip().split(":")
        h = int(parts[0])
        m = int(parts[1]) if len(parts) > 1 else 0
        total_min = h * 60 + m
        diff = (float(values.get("to_offset", 0)) - float(values.get("from_offset", 0))) * 60
        converted = total_min + diff
        converted %= 24 * 60
        ch, cm = divmod(int(converted), 60)
        suffix = "AM" if ch < 12 else "PM"
        ch12 = ch % 12
        if ch12 == 0:
            ch12 = 12
        return [
            CalcResult("Converted time", f"{ch:02d}:{cm:02d} ({ch12}:{cm:02d} {suffix})"),
            CalcResult("UTC equivalent", f"{(h - int(float(values.get('from_offset', 0)))) % 24:02d}:{m:02d}"),
            CalcResult("Offset difference", f"{fmt(diff / 60, 1)} hours"),
        ]


class ShiftDurationCalc(Calculator):
    id = "dt_shift"
    name = "Shift Duration"
    category = "Date & Time"
    description = "Length of a work shift including break"
    icon = "🕗"
    example = "08:00–17:00 with 45m break = 8h 15m"

    def get_inputs(self):
        return [
            InputField("start", "Shift start (HH:MM)", "text", "08:00"),
            InputField("end", "Shift end (HH:MM)", "text", "17:00"),
            InputField("break_m", "Break (minutes)", "number", 45),
        ]

    def calculate(self, values):
        def parse_t(t):
            parts = str(t).strip().split(":")
            return int(parts[0]) * 60 + (int(parts[1]) if len(parts) > 1 else 0)
        s = parse_t(values.get("start", "08:00"))
        e = parse_t(values.get("end", "17:00"))
        if e < s:
            e += 24 * 60
        work_min = e - s - self.num(values, "break_m")
        h, m = divmod(work_min, 60)
        return [
            CalcResult("Shift duration", f"{h} hours {m} minutes"),
            CalcResult("Total hours (decimal)", f"{fmt(work_min / 60, 2)}"),
            CalcResult("In minutes", fmt(work_min)),
        ]


class WorkHoursCalc(Calculator):
    id = "dt_work_hours"
    name = "Work Hours"
    category = "Date & Time"
    description = "Weekly/monthly work hours and pay"
    icon = "💵"
    example = "8h/day × 5 days = 40h/week"

    def get_inputs(self):
        return [
            InputField("hours_day", "Hours per day", "number", 8),
            InputField("days_week", "Days per week", "number", 5),
            InputField("rate", "Hourly rate", "number", 0, required=False),
        ]

    def calculate(self, values):
        h = self.num(values, "hours_day")
        d = self.num(values, "days_week")
        rate = self.num(values, "rate")
        week = h * d
        month = week * 4.33
        year = week * 52
        results = [
            CalcResult("Weekly hours", fmt(week)),
            CalcResult("Monthly hours", fmt(month, 1)),
            CalcResult("Yearly hours", fmt(year, 1)),
        ]
        if rate > 0:
            results.append(CalcResult("Weekly pay", f"${fmt(week * rate, 2)}"))
            results.append(CalcResult("Monthly pay", f"${fmt(month * rate, 2)}"))
            results.append(CalcResult("Yearly pay", f"${fmt(year * rate, 2)}"))
        return results


class OvertimeCalcDateTime(Calculator):
    id = "dt_overtime"
    name = "Overtime Work"
    category = "Date & Time"
    description = "Overtime hours beyond standard workday"
    icon = "⏰"
    example = "9.5h worked, 8h standard → 1.5h OT"

    def get_inputs(self):
        return [
            InputField("worked", "Hours worked", "number", 9.5),
            InputField("standard", "Standard hours", "number", 8),
            InputField("ot_rate", "OT rate (× normal)", "number", 1.5, required=False),
            InputField("hourly", "Hourly pay", "number", 0, required=False),
        ]

    def calculate(self, values):
        worked = self.num(values, "worked")
        standard = self.num(values, "standard")
        ot = max(worked - standard, 0)
        regular = worked - ot
        results = [
            CalcResult("Regular hours", fmt(regular)),
            CalcResult("Overtime hours", fmt(ot)),
        ]
        hourly = self.num(values, "hourly")
        omult = self.num(values, "ot_rate") or 1.5
        if hourly > 0:
            results.append(CalcResult("Regular pay", f"${fmt(regular * hourly, 2)}"))
            results.append(CalcResult("Overtime pay", f"${fmt(ot * hourly * omult, 2)}"))
            results.append(CalcResult("Total pay", f"${fmt(regular * hourly + ot * hourly * omult, 2)}"))
        return results
