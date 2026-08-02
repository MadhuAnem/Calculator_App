"""
AllCalc — Comprehensive Multi-Calculator Application
====================================================
A single Python/Tkinter desktop application with 200+ calculators
across 22 categories.

Run:  python app.py
"""
import math
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Ensure the package directory is importable when running app.py directly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calculators import CATEGORIES, ALL_CALCULATORS, total_count

# ── Color scheme ──────────────────────────────────────────────────────────
COLORS = {
    "bg":        "#0f172a",   # deep navy
    "bg_light":  "#1e293b",
    "bg_lighter":"#334155",
    "sidebar":   "#111827",
    "accent":    "#22d3ee",   # cyan
    "accent2":   "#f59e0b",   # amber
    "text":      "#e2e8f0",
    "text_dim":  "#94a3b8",
    "result":    "#10b981",   # green
    "error":     "#f87171",
    "card":      "#1e293b",
    "border":    "#475569",
}


class AllCalcApp:
    """Main application window."""

    def __init__(self, root):
        self.root = root
        root.title(f"AllCalc — {total_count()} Calculators in One App")
        root.geometry("1200x760")
        root.minsize(960, 600)
        root.configure(bg=COLORS["bg"])

        self.current_calc = None
        self.input_widgets = {}
        self.selected_category = None

        self._build_style()
        self._build_layout()
        self._load_categories()
        self._show_home()

    # ── Styling ──────────────────────────────────────────────────────────
    def _build_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background=COLORS["bg"])
        style.configure("Sidebar.TFrame", background=COLORS["sidebar"])
        style.configure("Card.TFrame", background=COLORS["card"])
        style.configure(
            "TLabel", background=COLORS["bg"], foreground=COLORS["text"],
            font=("Segoe UI", 10),
        )
        style.configure(
            "Title.TLabel", background=COLORS["bg"], foreground=COLORS["accent"],
            font=("Segoe UI", 22, "bold"),
        )
        style.configure(
            "Section.TLabel", background=COLORS["bg"], foreground=COLORS["accent2"],
            font=("Segoe UI", 13, "bold"),
        )
        style.configure(
            "Dim.TLabel", background=COLORS["bg"], foreground=COLORS["text_dim"],
            font=("Segoe UI", 9),
        )
        style.configure(
            "ResultValue.TLabel", background=COLORS["card"], foreground=COLORS["result"],
            font=("Segoe UI", 12, "bold"),
        )
        style.configure(
            "ResultLabel.TLabel", background=COLORS["card"], foreground=COLORS["text"],
            font=("Segoe UI", 10),
        )
        style.configure(
            "Cat.TButton", background=COLORS["bg_light"], foreground=COLORS["text"],
            borderwidth=0, focusthickness=0, padding=(10, 7),
            font=("Segoe UI", 10),
        )
        style.map("Cat.TButton",
                  background=[("active", COLORS["bg_lighter"]),
                              ("selected", COLORS["accent"])],
                  foreground=[("selected", COLORS["bg"])])
        style.configure(
            "Calc.TButton", background=COLORS["bg_lighter"], foreground=COLORS["text"],
            padding=(8, 6), font=("Segoe UI", 9),
        )
        style.map("Calc.TButton",
                  background=[("active", COLORS["accent"])],
                  foreground=[("active", COLORS["bg"])])
        style.configure(
            "Accent.TButton", background=COLORS["accent"], foreground=COLORS["bg"],
            padding=(16, 10), font=("Segoe UI", 12, "bold"),
        )
        style.map("Accent.TButton", background=[("active", "#67e8f9")])
        style.configure(
            "TEntry", fieldbackground=COLORS["bg_lighter"], foreground=COLORS["text"],
            bordercolor=COLORS["border"], insertcolor=COLORS["text"],
        )
        style.configure(
            "TCombobox", fieldbackground=COLORS["bg_lighter"],
            foreground=COLORS["text"], background=COLORS["bg_lighter"],
            arrowcolor=COLORS["text"],
        )
        style.configure(
            "TCheckbutton", background=COLORS["card"], foreground=COLORS["text"],
        )

    # ── Layout ───────────────────────────────────────────────────────────
    def _build_layout(self):
        # Main horizontal split: sidebar | content
        self.main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        # ── Sidebar ──────────────────────────────────────────────────────
        self.sidebar = ttk.Frame(self.main_pane, style="Sidebar.TFrame", width=280)
        self.sidebar.pack_propagate(False)
        self.main_pane.add(self.sidebar, weight=0)

        header = tk.Frame(self.sidebar, bg=COLORS["sidebar"])
        header.pack(fill=tk.X, padx=12, pady=(14, 8))
        tk.Label(header, text="🧮 AllCalc", bg=COLORS["sidebar"],
                 fg=COLORS["accent"], font=("Segoe UI", 17, "bold")).pack(anchor="w")
        tk.Label(header, text=f"{total_count()} calculators · 22 categories",
                 bg=COLORS["sidebar"], fg=COLORS["text_dim"],
                 font=("Segoe UI", 9)).pack(anchor="w")

        # Search box
        search_frame = tk.Frame(self.sidebar, bg=COLORS["sidebar"])
        search_frame.pack(fill=tk.X, padx=12, pady=(8, 4))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self._on_search())
        self.search_entry = tk.Entry(
            search_frame, textvariable=self.search_var, bg=COLORS["bg_lighter"],
            fg=COLORS["text"], insertbackground=COLORS["text"],
            relief="flat", font=("Segoe UI", 10),
        )
        self.search_entry.pack(fill=tk.X, ipady=6)
        self.search_entry.insert(0, "")
        self.search_entry.bind("<KeyRelease>", lambda e: self._on_search())

        # Category / search results list (scrollable)
        self.nav_container = tk.Frame(self.sidebar, bg=COLORS["sidebar"])
        self.nav_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)
        self.nav_canvas = tk.Canvas(self.nav_container, bg=COLORS["sidebar"],
                                    highlightthickness=0)
        self.nav_scroll = ttk.Scrollbar(self.nav_container, orient="vertical",
                                        command=self.nav_canvas.yview)
        self.nav_canvas.configure(yscrollcommand=self.nav_scroll.set)
        self.nav_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.nav_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.nav_inner = tk.Frame(self.nav_canvas, bg=COLORS["sidebar"])
        self._nav_window = self.nav_canvas.create_window((0, 0), window=self.nav_inner, anchor="nw")
        self.nav_inner.bind("<Configure>",
                            lambda e: self.nav_canvas.configure(scrollregion=self.nav_canvas.bbox("all")))
        self.nav_canvas.bind("<Enter>", lambda e: self._bind_mousewheel())
        self.nav_canvas.bind("<Leave>", lambda e: self._unbind_mousewheel())

        # ── Content area ─────────────────────────────────────────────────
        self.content = ttk.Frame(self.main_pane, style="TFrame")
        self.main_pane.add(self.content, weight=1)

        # Header bar
        self.topbar = tk.Frame(self.content, bg=COLORS["bg"])
        self.topbar.pack(fill=tk.X, padx=20, pady=(14, 6))
        self.crumb = tk.Label(self.topbar, text="Home", bg=COLORS["bg"],
                              fg=COLORS["text_dim"], font=("Segoe UI", 10))
        self.crumb.pack(anchor="w")

        # Scrollable body
        self.body_container = tk.Frame(self.content, bg=COLORS["bg"])
        self.body_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))
        self.body_canvas = tk.Canvas(self.body_container, bg=COLORS["bg"], highlightthickness=0)
        self.body_scroll = ttk.Scrollbar(self.body_container, orient="vertical",
                                         command=self.body_canvas.yview)
        self.body_canvas.configure(yscrollcommand=self.body_scroll.set)
        self.body_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.body_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.body = tk.Frame(self.body_canvas, bg=COLORS["bg"])
        self._body_window = self.body_canvas.create_window((0, 0), window=self.body, anchor="nw")
        self.body.bind("<Configure>",
                       lambda e: self.body_canvas.configure(scrollregion=self.body_canvas.bbox("all")))
        self.body_canvas.bind("<Enter>", lambda e: self._bind_body_mousewheel())
        self.body_canvas.bind("<Leave>", lambda e: self._unbind_body_mousewheel())

    # ── Mouse wheel helpers ──────────────────────────────────────────────
    def _bind_mousewheel(self):
        self.nav_canvas.bind_all("<MouseWheel>", self._on_nav_wheel)

    def _unbind_mousewheel(self):
        self.nav_canvas.unbind_all("<MouseWheel>")

    def _bind_body_mousewheel(self):
        self.body_canvas.bind_all("<MouseWheel>", self._on_body_wheel)

    def _unbind_body_mousewheel(self):
        self.body_canvas.unbind_all("<MouseWheel>")

    def _on_nav_wheel(self, event):
        self.nav_canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def _on_body_wheel(self, event):
        self.body_canvas.yview_scroll(-1 * (event.delta // 120), "units")

    # ── Data loading ─────────────────────────────────────────────────────
    def _load_categories(self):
        self.category_buttons = {}

    def _clear_nav(self):
        for w in self.nav_inner.winfo_children():
            w.destroy()
        self.category_buttons.clear()

    def _render_categories(self):
        """Render category buttons in sidebar."""
        self._clear_nav()
        for cat in CATEGORIES:
            count = len(CATEGORIES[cat])
            btn = tk.Button(
                self.nav_inner, text=f"{cat}  ({count})", anchor="w",
                bg=COLORS["bg_light"], fg=COLORS["text"], relief="flat",
                activebackground=COLORS["bg_lighter"], activeforeground=COLORS["text"],
                font=("Segoe UI", 10), padx=10, pady=7, bd=0,
                command=lambda c=cat: self._show_category(c),
            )
            btn.pack(fill=tk.X, pady=1)
            self.category_buttons[cat] = btn

    def _on_search(self):
        term = self.search_var.get().strip().lower()
        self._clear_nav()
        if not term:
            self._render_categories()
            return
        results = []
        for cat, calcs in CATEGORIES.items():
            for c in calcs:
                if term in c.name.lower() or term in cat.lower() or term in c.id.lower():
                    results.append((cat, c))
        if not results:
            tk.Label(self.nav_inner, text="No calculators found",
                     bg=COLORS["sidebar"], fg=COLORS["text_dim"],
                     font=("Segoe UI", 10)).pack(pady=10)
            return
        # Limit display
        for cat, c in results[:50]:
            btn = tk.Button(
                self.nav_inner, text=f"🔹 {c.name}", anchor="w",
                bg=COLORS["bg_light"], fg=COLORS["text"], relief="flat",
                activebackground=COLORS["bg_lighter"], activeforeground=COLORS["text"],
                font=("Segoe UI", 9), padx=10, pady=5, bd=0,
                command=lambda cc=c: self._show_calculator(cc),
            )
            btn.pack(fill=tk.X, pady=1)
        if len(results) > 50:
            tk.Label(self.nav_inner, text=f"+ {len(results)-50} more…",
                     bg=COLORS["sidebar"], fg=COLORS["text_dim"],
                     font=("Segoe UI", 9)).pack(pady=4)

    # ── Views ────────────────────────────────────────────────────────────
    def _clear_body(self):
        for w in self.body.winfo_children():
            w.destroy()

    def _show_home(self):
        self.crumb.config(text="Home")
        self._clear_body()
        self.current_calc = None

        tk.Label(self.body, text="Welcome to AllCalc", bg=COLORS["bg"],
                 fg=COLORS["accent"], font=("Segoe UI", 24, "bold")).pack(pady=(20, 4))
        tk.Label(self.body, text="One application. Every calculation you need.",
                 bg=COLORS["bg"], fg=COLORS["text_dim"],
                 font=("Segoe UI", 12)).pack(pady=(0, 16))

        # Search bar
        search_row = tk.Frame(self.body, bg=COLORS["bg"])
        search_row.pack(pady=10)
        self.home_search = tk.Entry(
            search_row, bg=COLORS["bg_light"], fg=COLORS["text"],
            insertbackground=COLORS["text"], relief="flat",
            font=("Segoe UI", 13), width=42,
        )
        self.home_search.pack(side=tk.LEFT, ipady=8, ipadx=8)
        self.home_search.bind("<KeyRelease>", lambda e: self._home_search())

        # Category grid
        grid = tk.Frame(self.body, bg=COLORS["bg"])
        grid.pack(pady=10, padx=10)
        icons = {
            "Basic Mathematics": "➗", "Financial Calculations": "💰",
            "Health & Fitness": "❤️", "Education": "🎓",
            "Date & Time": "📅", "Engineering": "🔧",
            "Physics": "⚛️", "Electricity": "⚡",
            "Chemistry": "🧪", "Construction": "🏗️",
            "Business": "📊", "Statistics": "📈",
            "Computer Science": "💻", "Unit Conversion": "📏",
            "Travel": "✈️", "Agriculture": "🌾",
            "Shopping": "🛒", "Household": "🏠",
            "Astronomy": "🔭", "Probability & Games": "🎲",
            "Miscellaneous": "✨",
        }
        row, col = 0, 0
        for cat in CATEGORIES:
            n = len(CATEGORIES[cat])
            icon = icons.get(cat, "🧮")
            card = tk.Frame(grid, bg=COLORS["card"], padx=12, pady=12,
                            highlightbackground=COLORS["border"], highlightthickness=1)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            tk.Label(card, text=f"{icon}  {cat}", bg=COLORS["card"],
                     fg=COLORS["text"], font=("Segoe UI", 11, "bold")).pack(anchor="w")
            tk.Label(card, text=f"{n} calculators", bg=COLORS["card"],
                     fg=COLORS["text_dim"], font=("Segoe UI", 9)).pack(anchor="w")
            tk.Button(card, text="Open →", bg=COLORS["bg_lighter"], fg=COLORS["accent"],
                      relief="flat", activebackground=COLORS["bg_lighter"],
                      activeforeground=COLORS["accent"], cursor="hand2",
                      command=lambda c=cat: self._show_category(c)).pack(anchor="e", pady=(8, 0))
            col += 1
            if col >= 4:
                col = 0
                row += 1
        for c in range(4):
            grid.columnconfigure(c, weight=1)

    def _home_search(self):
        term = self.home_search.get().strip().lower()
        self._clear_body()
        if not term:
            self._show_home()
            return
        self.crumb.config(text=f"Search: '{term}'")
        tk.Label(self.body, text=f"Search results for '{term}'", bg=COLORS["bg"],
                 fg=COLORS["accent"], font=("Segoe UI", 16, "bold")).pack(pady=(20, 8))
        found = 0
        for cat, calcs in CATEGORIES.items():
            matches = [c for c in calcs if term in c.name.lower() or term in c.id.lower()]
            if matches:
                found += len(matches)
                tk.Label(self.body, text=cat, bg=COLORS["bg"], fg=COLORS["accent2"],
                         font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(10, 2))
                for c in matches:
                    tk.Button(self.body, text=f"  {c.icon} {c.name} — {c.description}",
                              anchor="w", bg=COLORS["card"], fg=COLORS["text"],
                              relief="flat", activebackground=COLORS["bg_light"],
                              activeforeground=COLORS["text"], cursor="hand2",
                              command=lambda cc=c: self._show_calculator(cc)).pack(fill=tk.X, pady=2)
        if found == 0:
            tk.Label(self.body, text="No calculators match your search.",
                     bg=COLORS["bg"], fg=COLORS["error"], font=("Segoe UI", 12)).pack(pady=20)

    def _show_category(self, category):
        self.selected_category = category
        self.crumb.config(text=f"{category}")
        self._clear_body()
        self.current_calc = None

        calcs = CATEGORIES[category]
        tk.Label(self.body, text=f"{category}", bg=COLORS["bg"], fg=COLORS["accent"],
                 font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=(12, 2))
        tk.Label(self.body, text=f"{len(calcs)} calculators available",
                 bg=COLORS["bg"], fg=COLORS["text_dim"], font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 12))

        for c in calcs:
            card = tk.Frame(self.body, bg=COLORS["card"], padx=14, pady=10,
                            highlightbackground=COLORS["border"], highlightthickness=1,
                            cursor="hand2")
            card.pack(fill=tk.X, pady=4)
            card.bind("<Button-1>", lambda e, cc=c: self._show_calculator(cc))
            tk.Label(card, text=f"{c.icon}  {c.name}", bg=COLORS["card"],
                     fg=COLORS["text"], font=("Segoe UI", 12, "bold")).pack(anchor="w")
            tk.Label(card, text=c.description, bg=COLORS["card"],
                     fg=COLORS["text_dim"], font=("Segoe UI", 9)).pack(anchor="w")
            tk.Label(card, text=f"e.g., {c.example}", bg=COLORS["card"],
                     fg=COLORS["accent2"], font=("Segoe UI", 8)).pack(anchor="w", pady=(2, 0))

    def _show_calculator(self, calc):
        self.current_calc = calc
        self.crumb.config(text=f"{calc.category} › {calc.name}")
        self._clear_body()

        # Header
        tk.Label(self.body, text=f"{calc.icon}  {calc.name}", bg=COLORS["bg"],
                 fg=COLORS["accent"], font=("Segoe UI", 19, "bold")).pack(anchor="w", pady=(10, 2))
        tk.Label(self.body, text=calc.description, bg=COLORS["bg"],
                 fg=COLORS["text_dim"], font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 2))
        if calc.example:
            tk.Label(self.body, text=f"Example: {calc.example}", bg=COLORS["bg"],
                     fg=COLORS["accent2"], font=("Segoe UI", 9, "italic")).pack(anchor="w", pady=(0, 12))

        # Form card
        form_card = tk.Frame(self.body, bg=COLORS["card"], padx=20, pady=16,
                             highlightbackground=COLORS["border"], highlightthickness=1)
        form_card.pack(fill=tk.X, pady=(0, 12))

        self.input_widgets = {}
        fields = calc.get_inputs()
        for i, field in enumerate(fields):
            row = tk.Frame(form_card, bg=COLORS["card"])
            row.pack(fill=tk.X, pady=4)
            tk.Label(row, text=field.label, bg=COLORS["card"], fg=COLORS["text"],
                     font=("Segoe UI", 10), width=34, anchor="w").pack(side=tk.LEFT)
            if field.field_type == "select":
                var = tk.StringVar(value=field.default or field.options[0])
                combo = ttk.Combobox(row, textvariable=var, values=field.options,
                                     state="readonly", width=24)
                combo.pack(side=tk.LEFT)
                self.input_widgets[field.key] = var
            elif field.field_type == "date":
                var = tk.StringVar(value=field.default or "")
                entry = tk.Entry(row, textvariable=var, bg=COLORS["bg_light"],
                                 fg=COLORS["text"], insertbackground=COLORS["text"],
                                 relief="flat", font=("Segoe UI", 10), width=26)
                entry.pack(side=tk.LEFT)
                tk.Label(row, text="(YYYY-MM-DD)", bg=COLORS["card"],
                         fg=COLORS["text_dim"], font=("Segoe UI", 8)).pack(side=tk.LEFT, padx=6)
                self.input_widgets[field.key] = var
            else:  # number / text
                var = tk.StringVar(value=str(field.default) if field.default is not None else "")
                entry = tk.Entry(row, textvariable=var, bg=COLORS["bg_light"],
                                 fg=COLORS["text"], insertbackground=COLORS["text"],
                                 relief="flat", font=("Segoe UI", 10), width=26)
                entry.pack(side=tk.LEFT)
                self.input_widgets[field.key] = var
            if field.hint:
                tk.Label(row, text=field.hint, bg=COLORS["card"],
                         fg=COLORS["text_dim"], font=("Segoe UI", 8)).pack(side=tk.LEFT, padx=6)

        # Calculate button
        btn_row = tk.Frame(form_card, bg=COLORS["card"])
        btn_row.pack(pady=(12, 0))
        ttk.Button(btn_row, text="🔍  Calculate", style="Accent.TButton",
                   command=self._on_calculate).pack()

        # Results area
        self.results_frame = tk.Frame(self.body, bg=COLORS["bg"])
        self.results_frame.pack(fill=tk.X, pady=(0, 8))
        self._render_initial_results()

    def _render_initial_results(self):
        for w in self.results_frame.winfo_children():
            w.destroy()
        tk.Label(self.results_frame, text="Enter values above and press Calculate.",
                 bg=COLORS["bg"], fg=COLORS["text_dim"], font=("Segoe UI", 10)).pack(anchor="w", pady=6)

    # ── Calculation handling ─────────────────────────────────────────────
    def _gather_values(self):
        values = {}
        fields = self.current_calc.get_inputs()
        for field in fields:
            var = self.input_widgets.get(field.key)
            if var is None:
                continue
            raw = var.get().strip()
            if field.field_type in ("number",):
                if raw == "":
                    if not field.required:
                        values[field.key] = ""
                        continue
                    raise ValueError(f"'{field.label}' is required")
                try:
                    values[field.key] = float(raw)
                except ValueError:
                    raise ValueError(f"'{field.label}' must be a number")
            else:
                values[field.key] = raw
        return values

    def _on_calculate(self):
        if self.current_calc is None:
            return
        for w in self.results_frame.winfo_children():
            w.destroy()
        try:
            values = self._gather_values()
            results = self.current_calc.calculate(values)
            self._display_results(results)
        except ValueError as e:
            self._show_error(str(e))
        except Exception as e:
            self._show_error(f"Calculation error: {e}")

    def _show_error(self, msg):
        tk.Label(self.results_frame, text=f"⚠️  {msg}", bg=COLORS["bg"],
                 fg=COLORS["error"], font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=6)

    def _display_results(self, results):
        if not results:
            self._show_error("No results returned.")
            return
        # Group results by `group` (blank = single group)
        groups = {}
        order = []
        for r in results:
            g = r.group or "__main__"
            if g not in groups:
                groups[g] = []
                order.append(g)
            groups[g].append(r)

        for g in order:
            for r in groups[g]:
                card = tk.Frame(self.results_frame, bg=COLORS["card"], padx=16, pady=8,
                                highlightbackground=COLORS["border"], highlightthickness=1)
                card.pack(fill=tk.X, pady=3)
                tk.Label(card, text=r.label, bg=COLORS["card"], fg=COLORS["text"],
                         font=("Segoe UI", 10)).pack(side=tk.LEFT)
                tk.Label(card, text=str(r.value), bg=COLORS["card"], fg=COLORS["result"],
                         font=("Segoe UI", 12, "bold")).pack(side=tk.RIGHT)
                if r.formula:
                    tk.Label(card, text=r.formula, bg=COLORS["card"], fg=COLORS["text_dim"],
                             font=("Segoe UI", 8)).pack(side=tk.RIGHT, padx=10)


def main():
    root = tk.Tk()
    app = AllCalcApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
