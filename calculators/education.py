"""Education calculators."""
import math
from .base import Calculator, CalcResult, InputField, fmt


class GPACalc(Calculator):
    id = "edu_gpa"
    name = "GPA"
    category = "Education"
    description = "Grade Point Average from course grades and credits"
    icon = "🎓"
    example = "Course 4cr A(4.0), 3cr B(3.0) → 3.57"

    def get_inputs(self):
        return [
            InputField("grades", "Grades (comma separated)", "text", "4,3"),
            InputField("credits", "Credits (comma separated)", "text", "4,3"),
        ]

    def calculate(self, values):
        try:
            grades = [float(x.strip()) for x in str(values.get("grades", "")).split(",") if x.strip()]
            credits = [float(x.strip()) for x in str(values.get("credits", "")).split(",") if x.strip()]
        except ValueError:
            raise ValueError("Enter numeric values separated by commas")
        if len(grades) != len(credits) or not grades:
            raise ValueError("Number of grades must match number of credits")
        total_points = sum(g * c for g, c in zip(grades, credits))
        total_credits = sum(credits)
        gpa = total_points / total_credits if total_credits else 0
        return [
            CalcResult("GPA", f"{fmt(gpa, 2)}", "Σ(grade × credit) / Σ credits"),
            CalcResult("Total grade points", fmt(total_points)),
            CalcResult("Total credits", fmt(total_credits)),
        ]


class CGPACalc(Calculator):
    id = "edu_cgpa"
    name = "CGPA"
    category = "Education"
    description = "Cumulative GPA across semesters"
    icon = "📚"
    example = "Sem GPA 8.5, 9.0 with credits 20, 22 → 8.74"

    def get_inputs(self):
        return [
            InputField("gpas", "Semester GPAs (comma separated)", "text", "8.5,9.0"),
            InputField("credits", "Semester credits (comma separated)", "text", "20,22"),
        ]

    def calculate(self, values):
        try:
            gpas = [float(x.strip()) for x in str(values.get("gpas", "")).split(",") if x.strip()]
            credits = [float(x.strip()) for x in str(values.get("credits", "")).split(",") if x.strip()]
        except ValueError:
            raise ValueError("Enter numeric values separated by commas")
        if len(gpas) != len(credits) or not gpas:
            raise ValueError("Number of GPAs must match number of credits")
        cgpa = sum(g * c for g, c in zip(gpas, credits)) / sum(credits)
        return [
            CalcResult("CGPA", f"{fmt(cgpa, 2)}", "Σ(sem GPA × credits) / Σ credits"),
            CalcResult("Total credits", fmt(sum(credits))),
            CalcResult("Converted percentage (CGPA × 9.5)", f"{fmt(cgpa * 9.5, 2)}%"),
        ]


class MarksPercentageCalc(Calculator):
    id = "edu_marks_pct"
    name = "Percentage from Marks"
    category = "Education"
    description = "Percentage of marks obtained vs total"
    icon = "📝"
    example = "450 out of 500 = 90%"

    def get_inputs(self):
        return [
            InputField("obtained", "Marks obtained", "number", 450),
            InputField("total", "Total marks", "number", 500),
        ]

    def calculate(self, values):
        obtained, total = self.num(values, "obtained"), self.num(values, "total")
        if total <= 0:
            raise ValueError("Total marks must be positive")
        pct = obtained / total * 100
        return [
            CalcResult("Percentage", f"{fmt(pct, 2)}%", f"{fmt(obtained)} / {fmt(total)} × 100"),
            CalcResult("Fraction", f"{fmt(obtained)} / {fmt(total)}"),
        ]


class GradeConversionCalc(Calculator):
    id = "edu_grade"
    name = "Grade Conversion"
    category = "Education"
    description = "Convert percentage to letter grade and GPA"
    icon = "🔤"
    example = "85% → A / A+ (4.0)"

    def get_inputs(self):
        return [
            InputField("pct", "Percentage (%)", "number", 85),
        ]

    def calculate(self, values):
        pct = self.num(values, "pct")
        if pct >= 90:
            grade, gpa = "A / A+", 4.0
        elif pct >= 80:
            grade, gpa = "A- / B+", 3.7
        elif pct >= 70:
            grade, gpa = "B", 3.0
        elif pct >= 60:
            grade, gpa = "C", 2.0
        elif pct >= 50:
            grade, gpa = "D", 1.0
        else:
            grade, gpa = "F", 0.0
        return [
            CalcResult("Letter grade (approx)", grade),
            CalcResult("GPA equivalent", f"{fmt(gpa, 1)}"),
            CalcResult("CGPA equivalent (/10)", f"{fmt(pct / 9.5, 2)}"),
        ]


class AttendanceCalc(Calculator):
    id = "edu_attendance"
    name = "Attendance Percentage"
    category = "Education"
    description = "Attendance % and required classes"
    icon = "📋"
    example = "Attended 60 of 75 classes = 80%"

    def get_inputs(self):
        return [
            InputField("attended", "Classes attended", "number", 60),
            InputField("total", "Total classes", "number", 75),
            InputField("required_pct", "Required attendance (%)", "number", 75, required=False),
        ]

    def calculate(self, values):
        attended = self.num(values, "attended")
        total = self.num(values, "total")
        req = self.num(values, "required_pct") or 75
        if total <= 0:
            raise ValueError("Total classes must be positive")
        pct = attended / total * 100
        need_extra = max((req * total - 100 * attended) / (100 - req), 0)
        can_skip = max((attended * 100 - req * total) / req, 0)
        results = [CalcResult("Attendance %", f"{fmt(pct, 2)}%")]
        if pct < req:
            results.append(CalcResult(f"Classes to reach {fmt(req,0)}%", f"{fmt(need_extra,1)} more (≈{math.ceil(need_extra)})"))
            results.append(CalcResult("Total classes at that point", fmt(math.ceil(total + need_extra))))
        else:
            results.append(CalcResult("Status", "Above required attendance ✓"))
            results.append(CalcResult("Classes you can skip", fmt(math.floor(can_skip))))
        return results


class RankingCalc(Calculator):
    id = "edu_rank"
    name = "Ranking / Percentile"
    category = "Education"
    description = "Percentile rank from position"
    icon = "🏆"
    example = "Rank 3 of 100 → 97th percentile"

    def get_inputs(self):
        return [
            InputField("rank", "Your rank", "number", 3),
            InputField("total", "Total candidates", "number", 100),
        ]

    def calculate(self, values):
        rank = self.num(values, "rank")
        total = self.num(values, "total")
        if total <= 0 or rank <= 0:
            raise ValueError("Rank and total must be positive")
        percentile = (total - rank) / total * 100
        return [
            CalcResult("Percentile", f"{fmt(percentile, 2)}th percentile"),
            CalcResult("Candidates above you", fmt(rank - 1)),
            CalcResult("Candidates below you", fmt(total - rank)),
        ]


class AgeCalc(Calculator):
    id = "edu_age"
    name = "Age (Education)"
    category = "Education"
    description = "Age and birth year from birth date"
    icon = "🎂"
    example = "Born 2000-05-15"

    def get_inputs(self):
        return [
            InputField("dob", "Date of birth", "date", "2000-05-15"),
        ]

    def calculate(self, values):
        from datetime import datetime
        raw = values.get("dob", "")
        try:
            dob = datetime.strptime(str(raw), "%Y-%m-%d")
        except (ValueError, TypeError):
            raise ValueError("Enter a valid date (YYYY-MM-DD)")
        today = datetime.now()
        years = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        months = (today.year - dob.year) * 12 + (today.month - dob.month)
        days = (today - dob).days
        return [
            CalcResult("Age in years", f"{years} years"),
            CalcResult("Age in months", fmt(months)),
            CalcResult("Age in days", fmt(days)),
        ]


class StudyHoursCalc(Calculator):
    id = "edu_study_hours"
    name = "Study Hours"
    category = "Education"
    description = "Total study time and grade-based suggestion"
    icon = "📖"
    example = "2 hours/day × 30 days = 60 hours"

    def get_inputs(self):
        return [
            InputField("hours_day", "Study hours per day", "number", 2),
            InputField("days", "Number of days", "number", 30),
        ]

    def calculate(self, values):
        h = self.num(values, "hours_day")
        d = self.num(values, "days")
        total = h * d
        weekly = h * 7
        return [
            CalcResult("Total study hours", fmt(total)),
            CalcResult("Total minutes", fmt(total * 60)),
            CalcResult("Weekly hours", fmt(weekly)),
            CalcResult("Daily recommended (temple formula)", f"{fmt(d * 3, 0)} minutes" if d else "—"),
        ]
