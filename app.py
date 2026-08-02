"""
AllCalc — Comprehensive Multi-Calculator Application
====================================================
A single Python/Tkinter desktop application with 200+ calculators
across 20+ categories.

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
from calculators.base import option_key
from calculators.financial import FX_RATES, CURRENCIES, _currency_code, _currency_option_for

# ── Color scheme (light / white theme) ──────────────────────────────────
COLORS = {
    "bg":         "#f1f5f9",   # app background (light gray)
    "bg_light":   "#ffffff",   # white cards / surfaces
    "bg_lighter": "#e2e8f0",   # hover / subtle fill
    "sidebar":    "#e8eef5",   # sidebar light
    "accent":     "#0284c7",   # sky blue
    "accent2":    "#d97706",   # amber
    "text":       "#0f172a",   # near-black
    "text_dim":   "#64748b",   # slate gray
    "result":     "#15803d",   # green
    "error":      "#dc2626",   # red
    "card":       "#ffffff",
    "border":     "#cbd5e1",
}


class AllCalcApp:
    """Main application window."""

    def __init__(self, root):
        self.root = root
        root.title(f"AllCalc — {total_count()} Calculators in One App")
        root.geometry("1280x800")
        root.minsize(1024, 640)
        root.configure(bg=COLORS["bg"])

        self.current_calc = None
        self.input_widgets = {}
        self._combo_widgets = {}
        self.selected_category = None
        self.currency_ratio_label = None

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
                  foreground=[("selected", COLORS["bg_light"])])
        style.configure(
            "Calc.TButton", background=COLORS["bg_light"], foreground=COLORS["text"],
            padding=(8, 6), font=("Segoe UI", 9),
        )
        style.map("Calc.TButton",
                  background=[("active", COLORS["accent"])],
                  foreground=[("active", COLORS["bg_light"])])
        style.configure(
            "Accent.TButton", background=COLORS["accent"], foreground=COLORS["bg_light"],
            padding=(16, 10), font=("Segoe UI", 12, "bold"),
        )
        style.map("Accent.TButton", background=[("active", "#0ea5e9")])
        style.configure(
            "Nav.TButton", background=COLORS["bg_light"], foreground=COLORS["accent"],
            padding=(10, 6), font=("Segoe UI", 10, "bold"),
        )
        style.map("Nav.TButton",
                  background=[("active", COLORS["bg_lighter"])],
                  foreground=[("active", COLORS["accent"])])
        style.configure(
            "TEntry", fieldbackground=COLORS["bg_light"], foreground=COLORS["text"],
            bordercolor=COLORS["border"], insertcolor=COLORS["text"],
        )
        # Combobox: light-blue field + solid blue arrow button so it is
        # unmistakably a dropdown (not a plain text entry).
        style.configure(
            "TCombobox", fieldbackground="#eef6ff",
            foreground=COLORS["text"], background=COLORS["accent"],
            arrowcolor="#ffffff", bordercolor=COLORS["accent"],
            lightcolor=COLORS["accent"], darkcolor=COLORS["accent"],
            padding=(6, 4), relief="solid",
        )
        style.map("TCombobox",
                  fieldbackground=[("readonly", "#eef6ff")],
                  foreground=[("readonly", COLORS["text"])],
                  background=[("readonly", COLORS["accent"])],
                  arrowcolor=[("readonly", "#ffffff")],
                  bordercolor=[("readonly", COLORS["accent"])])
        style.configure(
            "TCheckbutton", background=COLORS["card"], foreground=COLORS["text"],
        )

    # ── Layout ───────────────────────────────────────────────────────────
    def _build_layout(self):
        # Main horizontal split: sidebar | content
        self.main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        # ── Sidebar ──────────────────────────────────────────────────────
        self.sidebar = ttk.Frame(self.main_pane, style="Sidebar.TFrame", width=300)
        self.sidebar.pack_propagate(False)
        self.main_pane.add(self.sidebar, weight=0)

        header = tk.Frame(self.sidebar, bg=COLORS["sidebar"])
        header.pack(fill=tk.X, padx=12, pady=(14, 8))
        tk.Label(header, text="🧮 AllCalc", bg=COLORS["sidebar"],
                 fg=COLORS["accent"], font=("Segoe UI", 17, "bold")).pack(anchor="w")
        tk.Label(header, text=f"{total_count()} calculators · {len(CATEGORIES)} categories",
                 bg=COLORS["sidebar"], fg=COLORS["text_dim"],
                 font=("Segoe UI", 9)).pack(anchor="w")

        # Search box
        search_frame = tk.Frame(self.sidebar, bg=COLORS["sidebar"])
        search_frame.pack(fill=tk.X, padx=12, pady=(8, 4))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self._on_search())
        self.search_entry = tk.Entry(
            search_frame, textvariable=self.search_var, bg=COLORS["bg_light"],
            fg=COLORS["text"], insertbackground=COLORS["text"],
            relief="flat", font=("Segoe UI", 10),
        )
        self.search_entry.pack(fill=tk.X, ipady=6)
        self.search_entry.insert(0, "")
        self.search_entry.bind("<KeyRelease>", lambda e: self._on_search())

        # ── "Jump to calculator" dropdown ────────────────────────────────
        jump_frame = tk.Frame(self.sidebar, bg=COLORS["sidebar"])
        jump_frame.pack(fill=tk.X, padx=12, pady=(6, 2))
        tk.Label(jump_frame, text="⚡ Jump to calculator", bg=COLORS["sidebar"],
                 fg=COLORS["text"], font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.jump_var = tk.StringVar()
        self.jump_combo = ttk.Combobox(
            jump_frame, textvariable=self.jump_var, state="readonly",
            width=32, style="TCombobox",
        )
        self.jump_combo.pack(fill=tk.X, pady=(2, 0))
        self.jump_combo.bind("<<ComboboxSelected>>", self._on_jump)
        self._jump_map = {}

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

        # Header bar (navigation)
        self.topbar = tk.Frame(self.content, bg=COLORS["bg"])
        self.topbar.pack(fill=tk.X, padx=20, pady=(14, 6))

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

    # ── Topbar navigation ────────────────────────────────────────────────
    def _render_topbar(self, show_home=True, show_back=False, crumb=""):
        for w in self.topbar.winfo_children():
            w.destroy()
        if show_home:
            ttk.Button(self.topbar, text="🏠  Home", style="Nav.TButton",
                       command=self._show_home).pack(side=tk.LEFT, padx=(0, 6))
        if show_back:
            ttk.Button(self.topbar, text="←  Back", style="Nav.TButton",
                       command=self._go_back).pack(side=tk.LEFT, padx=(0, 6))
        self.crumb = tk.Label(self.topbar, text=crumb, bg=COLORS["bg"],
                              fg=COLORS["text_dim"], font=("Segoe UI", 10))
        self.crumb.pack(side=tk.LEFT, padx=8)

    def _go_back(self):
        if self.current_calc is not None and self.selected_category:
            self._show_category(self.selected_category)
        elif self.selected_category:
            self._show_home()
        else:
            self._show_home()

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
        # Build jump dropdown options: "Category › Service"
        options = []
        self._jump_map.clear()
        for cat in CATEGORIES:
            for c in CATEGORIES[cat]:
                label = f"{cat} › {c.name}"
                options.append(label)
                self._jump_map[label] = c
        self.jump_combo.configure(values=options)
        self._render_categories()

    def _on_jump(self, event=None):
        val = self.jump_var.get()
        calc = self._jump_map.get(val)
        self.jump_var.set("")
        if calc:
            self._show_calculator(calc)

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
                self.nav_inner, text=f"▸ {cat}  ({count})", anchor="w",
                bg=COLORS["sidebar"], fg=COLORS["text"], relief="flat",
                activebackground=COLORS["bg_lighter"], activeforeground=COLORS["accent"],
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
                self.nav_inner, text=f"🔹 {c.icon} {c.name}", anchor="w",
                bg=COLORS["sidebar"], fg=COLORS["text"], relief="flat",
                activebackground=COLORS["bg_lighter"], activeforeground=COLORS["accent"],
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
        self.selected_category = None
        self.current_calc = None
        self._render_topbar(show_home=False, show_back=False, crumb="Home")
        self._clear_body()

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
                tk.Label(self.body, text=f"{cat}", bg=COLORS["bg"], fg=COLORS["accent2"],
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
        self.current_calc = None
        self._render_topbar(show_home=True, show_back=True, crumb=category)
        self._clear_body()

        calcs = CATEGORIES[category]
        tk.Label(self.body, text=f"{category}", bg=COLORS["bg"], fg=COLORS["accent"],
                 font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=(12, 2))
        tk.Label(self.body, text=f"{len(calcs)} calculators available",
                 bg=COLORS["bg"], fg=COLORS["text_dim"], font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 8))

        # ── "Select a calculator" dropdown for this category ────────────
        sel_row = tk.Frame(self.body, bg=COLORS["bg"])
        sel_row.pack(fill=tk.X, pady=(2, 10))
        tk.Label(sel_row, text="▶  Select a calculator:", bg=COLORS["bg"],
                 fg=COLORS["text"], font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
        self.cat_combo_var = tk.StringVar()
        self.cat_combo = ttk.Combobox(
            sel_row, textvariable=self.cat_combo_var, state="readonly",
            values=[c.name for c in calcs], width=40, style="TCombobox",
        )
        self.cat_combo.pack(side=tk.LEFT, padx=8)
        self.cat_combo.bind("<<ComboboxSelected>>", lambda e: self._on_cat_select(category))
        ttk.Button(sel_row, text="Open", style="Accent.TButton",
                   command=lambda: self._on_cat_select(category)).pack(side=tk.LEFT, padx=(0, 8))
        tk.Label(sel_row, text="— or click a card below", bg=COLORS["bg"],
                 fg=COLORS["text_dim"], font=("Segoe UI", 9)).pack(side=tk.LEFT)

        # ── Service cards ───────────────────────────────────────────────
        for c in calcs:
            card = tk.Frame(self.body, bg=COLORS["card"], padx=14, pady=10,
                            highlightbackground=COLORS["border"], highlightthickness=1,
                            cursor="hand2")
            card.pack(fill=tk.X, pady=4)
            # Make the card AND every child clickable → open the calculator
            def open_calc(e=None, cc=c):
                self._show_calculator(cc)
            card.bind("<Button-1>", open_calc)
            title_lbl = tk.Label(card, text=f"{c.icon}  {c.name}", bg=COLORS["card"],
                                 fg=COLORS["text"], font=("Segoe UI", 12, "bold"),
                                 cursor="hand2")
            title_lbl.pack(anchor="w")
            title_lbl.bind("<Button-1>", open_calc)
            desc_lbl = tk.Label(card, text=c.description, bg=COLORS["card"],
                                fg=COLORS["text_dim"], font=("Segoe UI", 9),
                                cursor="hand2")
            desc_lbl.pack(anchor="w")
            desc_lbl.bind("<Button-1>", open_calc)
            ex_lbl = tk.Label(card, text=f"e.g., {c.example}", bg=COLORS["card"],
                              fg=COLORS["accent2"], font=("Segoe UI", 8),
                              cursor="hand2")
            ex_lbl.pack(anchor="w", pady=(2, 0))
            ex_lbl.bind("<Button-1>", open_calc)

    def _on_cat_select(self, category):
        name = self.cat_combo_var.get()
        if not name:
            return
        for c in CATEGORIES[category]:
            if c.name == name:
                self._show_calculator(c)
                return

    def _show_calculator(self, calc):
        self.current_calc = calc
        self.selected_category = calc.category
        self.input_widgets = {}
        self._combo_widgets = {}
        self.currency_ratio_label = None
        self._render_topbar(show_home=True, show_back=True,
                            crumb=f"{calc.category} › {calc.name}")
        self._clear_body()

        # ── Switch-service dropdown (flow from one service to another) ──
        switch_row = tk.Frame(self.body, bg=COLORS["bg"])
        switch_row.pack(fill=tk.X, pady=(8, 4))
        tk.Label(switch_row, text="🔄  Switch service:", bg=COLORS["bg"],
                 fg=COLORS["text"], font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
        cat_names = [c.name for c in CATEGORIES[calc.category]]
        self.switch_var = tk.StringVar(value=calc.name)
        self.switch_combo = ttk.Combobox(
            switch_row, textvariable=self.switch_var, state="readonly",
            values=cat_names, width=36, style="TCombobox",
        )
        self.switch_combo.pack(side=tk.LEFT, padx=8)
        self.switch_combo.bind("<<ComboboxSelected>>", self._on_switch)

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

        fields = calc.get_inputs()
        for i, field in enumerate(fields):
            row = tk.Frame(form_card, bg=COLORS["card"])
            row.pack(fill=tk.X, pady=4)
            tk.Label(row, text=field.label, bg=COLORS["card"], fg=COLORS["text"],
                     font=("Segoe UI", 10), width=34, anchor="w").pack(side=tk.LEFT)
            if field.field_type == "select":
                var = tk.StringVar(value=field.default or field.options[0])
                is_currency = (calc.id == "fin_currency" and field.key in ("from", "to"))
                combo = ttk.Combobox(row, textvariable=var, values=field.options,
                                     state="normal" if is_currency else "readonly",
                                     width=44, style="TCombobox")
                combo.pack(side=tk.LEFT)
                # Remember the full option list so we can restore it after
                # search-as-you-type filtering or after a selection is made.
                combo._full_options = list(field.options)
                # Click anywhere on a dropdown opens its list (not just the arrow),
                # so every service's select is clearly clickable.
                combo.bind("<Button-1>", lambda e, c=combo: self._open_dropdown(c))
                if is_currency:
                    # Editable + searchable dropdown for currency selection
                    combo.bind(
                        "<KeyRelease>",
                        lambda e, c=combo, opts=list(field.options): self._on_combo_type(c, opts),
                    )
                self.input_widgets[field.key] = var
                self._combo_widgets[field.key] = combo
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

        # ── Currency Conversion extras: Swap button + live ratio ─────────
        if calc.id == "fin_currency":
            self._build_currency_extra(form_card)

        # Calculate button
        btn_row = tk.Frame(form_card, bg=COLORS["card"])
        btn_row.pack(pady=(12, 0))
        ttk.Button(btn_row, text="🔍  Calculate", style="Accent.TButton",
                   command=self._on_calculate).pack()

        # Results area
        self.results_frame = tk.Frame(self.body, bg=COLORS["bg"])
        self.results_frame.pack(fill=tk.X, pady=(0, 8))
        self._render_initial_results()

    def _on_switch(self, event=None):
        name = self.switch_var.get()
        if not name:
            return
        for c in CATEGORIES[self.selected_category]:
            if c.name == name:
                self._show_calculator(c)
                return

# ── Combobox helpers ────────────────────────────────────────────────
    def _open_dropdown(self, combo):
        """Open a combobox's dropdown list when the user clicks anywhere on it.

        Also restores the full option list so a previously filtered/searchable
        dropdown always shows every choice on a fresh click.
        """
        try:
            full = getattr(combo, "_full_options", None)
            if full:
                combo.configure(values=list(full))
            combo.event_generate("<Down>")
        except tk.TclError:
            pass

    def _on_combo_type(self, combo, options):
        """Filter dropdown options as user types, for editable currency combos."""
        typed = combo.get().strip().lower()
        if not typed:
            combo.configure(values=options)
            combo.event_generate("<Down>")
            return
        # Filter: show options matching typed text or country/code
        filtered = [o for o in options if typed in o.lower()]
        combo.configure(values=filtered)
        if filtered:
            combo.event_generate("<Down>")

    def _on_currency_selected(self):
        """After picking a currency from the list, restore the full option
        list so the dropdown is never left in a filtered state."""
        for key in ("from", "to"):
            combo = self._combo_widgets.get(key)
            if combo is not None:
                full = getattr(combo, "_full_options", None)
                if full:
                    combo.configure(values=list(full))
        self._update_currency_ratio()

    # ── Currency Conversion extras ───────────────────────────────────────
    def _build_currency_extra(self, form_card):
        extra = tk.Frame(form_card, bg=COLORS["card"])
        extra.pack(fill=tk.X, pady=(4, 0))
        ttk.Button(extra, text="⇄  Swap currencies", style="Nav.TButton",
                   command=self._swap_currencies).pack(side=tk.LEFT, padx=(0, 14))
        self.currency_ratio_label = tk.Label(
            extra, text="", bg=COLORS["card"], fg=COLORS["accent2"],
            font=("Segoe UI", 10, "bold"),
        )
        self.currency_ratio_label.pack(side=tk.LEFT)
        for key in ("from", "to"):
            w = self._combo_widgets.get(key)
            if w:
                w.bind("<<ComboboxSelected>>",
                       lambda e: self._on_currency_selected())
        # Hint text under the currency dropdowns
        hint = tk.Label(form_card, text="💡 Click a dropdown and choose a country, "
                                        "or type a code / country name to search.",
                        bg=COLORS["card"], fg=COLORS["text_dim"],
                        font=("Segoe UI", 8, "italic"))
        hint.pack(fill=tk.X, pady=(2, 0))
        self._update_currency_ratio()

    def _swap_currencies(self):
        if "from" not in self.input_widgets or "to" not in self.input_widgets:
            return
        f = self.input_widgets["from"].get()
        t = self.input_widgets["to"].get()
        self.input_widgets["from"].set(t)
        self.input_widgets["to"].set(f)
        self._update_currency_ratio()

    def _update_currency_ratio(self):
        if self.currency_ratio_label is None:
            return
        try:
            frm = _currency_code(self.input_widgets["from"].get())
            to = _currency_code(self.input_widgets["to"].get())
            ratio = FX_RATES[to] / FX_RATES[frm]
            self.currency_ratio_label.config(
                text=f"1 {frm} = {ratio:,.4f} {to}    |    {CURRENCIES[frm]['name']} → {CURRENCIES[to]['name']}"
            )
        except Exception:
            self.currency_ratio_label.config(text="")

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
