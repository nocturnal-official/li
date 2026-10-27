"""
LifeGuard - Life Insurance Management System
CBSE Class XII Computer Science Project
Python 3 + Tkinter + SQLite (SQL)

Run: python main.py
No third-party Python packages are required.
"""

import csv
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date, datetime
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "lifeguard.db"

NAVY = "#14233B"
NAVY_LIGHT = "#1D3557"
BLUE = "#2D6CDF"
GOLD = "#E9B949"
BG = "#F3F6FB"
WHITE = "#FFFFFF"
TEXT = "#1F2937"
MUTED = "#64748B"
GREEN = "#16835D"
RED = "#C0392B"


def connect_db():
    """Open a database connection and return rows by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():
    """Create all tables and insert sample records only on first run."""
    with connect_db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            dob TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            address TEXT,
            created_on TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS policies (
            policy_id INTEGER PRIMARY KEY AUTOINCREMENT,
            policy_number TEXT NOT NULL UNIQUE,
            customer_id INTEGER NOT NULL,
            policy_type TEXT NOT NULL,
            sum_assured REAL NOT NULL CHECK(sum_assured > 0),
            annual_premium REAL NOT NULL CHECK(annual_premium >= 0),
            start_date TEXT NOT NULL,
            term_years INTEGER NOT NULL CHECK(term_years > 0),
            status TEXT NOT NULL DEFAULT 'Active',
            FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
                ON UPDATE CASCADE ON DELETE RESTRICT
        );

        CREATE TABLE IF NOT EXISTS beneficiaries (
            beneficiary_id INTEGER PRIMARY KEY AUTOINCREMENT,
            policy_id INTEGER NOT NULL,
            full_name TEXT NOT NULL,
            relationship TEXT NOT NULL,
            phone TEXT,
            FOREIGN KEY(policy_id) REFERENCES policies(policy_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            policy_id INTEGER NOT NULL,
            payment_date TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            payment_mode TEXT NOT NULL,
            transaction_ref TEXT NOT NULL UNIQUE,
            FOREIGN KEY(policy_id) REFERENCES policies(policy_id)
                ON UPDATE CASCADE ON DELETE RESTRICT
        );
        """)

        count = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        if count == 0:
            today = date.today().isoformat()
            conn.executemany("""
                INSERT INTO customers(full_name, dob, phone, email, address, created_on)
                VALUES (?, ?, ?, ?, ?, ?)
            """, [
                ("Aarav Sharma", "1985-04-12", "9876543210", "aarav@example.com", "Gurugram, Haryana", today),
                ("Meera Kapoor", "1990-09-23", "9876501234", "meera@example.com", "New Delhi, India", today),
                ("Kabir Malhotra", "1978-01-05", "9811122233", "kabir@example.com", "Noida, Uttar Pradesh", today),
            ])
            customer_ids = [r[0] for r in conn.execute("SELECT customer_id FROM customers ORDER BY customer_id").fetchall()]
            conn.executemany("""
                INSERT INTO policies(policy_number, customer_id, policy_type, sum_assured,
                                     annual_premium, start_date, term_years, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                ("LG-10001", customer_ids[0], "Term Life", 2500000, 12500, today, 20, "Active"),
                ("LG-10002", customer_ids[1], "Endowment", 1500000, 42000, today, 15, "Active"),
                ("LG-10003", customer_ids[2], "Whole Life", 3000000, 28500, today, 30, "Active"),
            ])
            policy_ids = [r[0] for r in conn.execute("SELECT policy_id FROM policies ORDER BY policy_id").fetchall()]
            conn.executemany("""
                INSERT INTO beneficiaries(policy_id, full_name, relationship, phone)
                VALUES (?, ?, ?, ?)
            """, [
                (policy_ids[0], "Ananya Sharma", "Spouse", "9876500001"),
                (policy_ids[1], "Rohan Kapoor", "Son", "9876500002"),
                (policy_ids[2], "Nisha Malhotra", "Spouse", "9876500003"),
            ])
            conn.executemany("""
                INSERT INTO payments(policy_id, payment_date, amount, payment_mode, transaction_ref)
                VALUES (?, ?, ?, ?, ?)
            """, [
                (policy_ids[0], today, 12500, "UPI", "TXN-DEMO-1001"),
                (policy_ids[1], today, 42000, "Net Banking", "TXN-DEMO-1002"),
            ])


def money(value):
    try:
        return "₹{:,.2f}".format(float(value))
    except (TypeError, ValueError):
        return "₹0.00"


def valid_date(value, label):
    try:
        datetime.strptime(value.strip(), "%Y-%m-%d")
        return True
    except ValueError:
        messagebox.showerror("Invalid date", f"{label} must use YYYY-MM-DD format.")
        return False


class LifeGuardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LifeGuard | Life Insurance Management System")
        self.geometry("1220x760")
        self.minsize(1000, 650)
        self.configure(bg=BG)
        self._configure_style()
        initialize_database()
        self._build_shell()
        self.refresh_all()

    def _configure_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", background=WHITE, fieldbackground=WHITE,
                        foreground=TEXT, rowheight=29, borderwidth=0, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#E7EDF6", foreground=NAVY,
                        font=("Segoe UI", 10, "bold"), padding=8)
        style.map("Treeview", background=[("selected", "#D9E7FF")], foreground=[("selected", NAVY)])
        style.configure("TCombobox", padding=6)
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", padding=(18, 10), font=("Segoe UI", 10, "bold"))

    def _build_shell(self):
        header = tk.Frame(self, bg=NAVY, height=82)
        header.pack(fill="x")
        header.pack_propagate(False)
        brand = tk.Frame(header, bg=NAVY)
        brand.pack(side="left", padx=24, pady=13)
        tk.Label(brand, text="✦  LIFEGUARD", bg=NAVY, fg=GOLD,
                 font=("Segoe UI", 20, "bold")).pack(anchor="w")
        tk.Label(brand, text="LIFE INSURANCE MANAGEMENT SYSTEM", bg=NAVY, fg="#D9E2F2",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(header, text="CBSE CLASS XII  •  PYTHON + SQL", bg=NAVY, fg="#D9E2F2",
                 font=("Segoe UI", 10)).pack(side="right", padx=25)

        self.main = tk.Frame(self, bg=BG)
        self.main.pack(fill="both", expand=True, padx=22, pady=18)

        self.notebook = ttk.Notebook(self.main)
        self.notebook.pack(fill="both", expand=True)
        self.dashboard_tab = tk.Frame(self.notebook, bg=BG)
        self.customers_tab = tk.Frame(self.notebook, bg=BG)
        self.policies_tab = tk.Frame(self.notebook, bg=BG)
        self.payments_tab = tk.Frame(self.notebook, bg=BG)
        self.beneficiaries_tab = tk.Frame(self.notebook, bg=BG)
        self.reports_tab = tk.Frame(self.notebook, bg=BG)
        for tab, label in [
            (self.dashboard_tab, "Dashboard"),
            (self.customers_tab, "Customers"),
            (self.policies_tab, "Policies"),
            (self.payments_tab, "Payments"),
            (self.beneficiaries_tab, "Beneficiaries"),
            (self.reports_tab, "Reports & SQL"),
        ]:
            self.notebook.add(tab, text=label)

        self._build_dashboard()
        self._build_customers()
        self._build_policies()
        self._build_payments()
        self._build_beneficiaries()
        self._build_reports()

        footer = tk.Frame(self, bg="#E7EDF6", height=30)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="Educational demonstration only • Use fictional data • Not an insurer's official premium quote",
                 bg="#E7EDF6", fg=MUTED, font=("Segoe UI", 8)).pack(pady=7)

    def _section_heading(self, parent, title, subtitle=None):
        tk.Label(parent, text=title, bg=BG, fg=NAVY,
                 font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(2, 0))
        if subtitle:
            tk.Label(parent, text=subtitle, bg=BG, fg=MUTED,
                     font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 12))

    def _button(self, parent, text, command, primary=True):
        bg = BLUE if primary else "#E4EAF3"
        fg = WHITE if primary else NAVY
        return tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                         activebackground=NAVY_LIGHT if primary else "#D5DEEA",
                         activeforeground=WHITE if primary else NAVY,
                         relief="flat", bd=0, padx=14, pady=8,
                         font=("Segoe UI", 9, "bold"), cursor="hand2")

    def _build_dashboard(self):
        self._section_heading(self.dashboard_tab, "Welcome to LifeGuard",
                              "A single workspace to manage policyholders, coverage, payments and beneficiaries.")
        cards = tk.Frame(self.dashboard_tab, bg=BG)
        cards.pack(fill="x", pady=(0, 15))
        self.stat_labels = {}
        stats = [
            ("customers", "POLICYHOLDERS", "0"),
            ("policies", "TOTAL POLICIES", "0"),
            ("active", "ACTIVE POLICIES", "0"),
            ("coverage", "TOTAL COVERAGE", "₹0"),
            ("payments", "PAYMENTS RECORDED", "0"),
        ]
        for key, label, initial in stats:
            card = tk.Frame(cards, bg=WHITE, highlightbackground="#DCE4EF", highlightthickness=1)
            card.pack(side="left", fill="both", expand=True, padx=(0, 10))
            tk.Frame(card, bg=GOLD, height=4).pack(fill="x")
            tk.Label(card, text=label, bg=WHITE, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=13, pady=(12, 5))
            value = tk.Label(card, text=initial, bg=WHITE, fg=NAVY, font=("Segoe UI", 17, "bold"))
            value.pack(anchor="w", padx=13, pady=(0, 13))
            self.stat_labels[key] = value

        lower = tk.Frame(self.dashboard_tab, bg=BG)
        lower.pack(fill="both", expand=True)
        left = tk.Frame(lower, bg=WHITE, highlightbackground="#DCE4EF", highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        tk.Label(left, text="Recent Policies", bg=WHITE, fg=NAVY,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=14, pady=12)
        self.recent_tree = self._make_tree(left, ("number", "customer", "type", "premium", "status"),
                                           ("Policy Number", "Policyholder", "Policy Type", "Annual Premium", "Status"))
        self.recent_tree.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        right = tk.Frame(lower, bg=NAVY_LIGHT)
        right.pack(side="right", fill="y")
        tk.Label(right, text="QUICK ACTIONS", bg=NAVY_LIGHT, fg=GOLD,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=18, pady=(18, 12))
        for label, command in [
            ("＋  Add Customer", lambda: self.notebook.select(self.customers_tab)),
            ("＋  Create Policy", lambda: self.notebook.select(self.policies_tab)),
            ("＋  Record Payment", lambda: self.notebook.select(self.payments_tab)),
            ("▤  Open Reports", lambda: self.notebook.select(self.reports_tab)),
        ]:
            tk.Button(right, text=label, command=command, bg="#29466D", fg=WHITE,
                      activebackground="#365A87", activeforeground=WHITE,
                      relief="flat", anchor="w", padx=14, pady=11,
                      font=("Segoe UI", 9, "bold"), cursor="hand2").pack(fill="x", padx=12, pady=5)

    def _make_tree(self, parent, columns, headings):
        wrapper = tk.Frame(parent, bg=WHITE)
        tree = ttk.Treeview(wrapper, columns=columns, show="headings", selectmode="browse")
        for col, heading in zip(columns, headings):
            tree.heading(col, text=heading)
            tree.column(col, width=130, minwidth=85, anchor="w")
        yscroll = ttk.Scrollbar(wrapper, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=yscroll.set)
        tree.pack(side="left", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")
        wrapper.pack(fill="both", expand=True)
        # The wrapper is packed in the parent; return the tree for data operations and bindings.
        return tree

    def _form_row(self, parent, label, variable, row, width=28):
        tk.Label(parent, text=label, bg=BG, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=6)
        entry = tk.Entry(parent, textvariable=variable, width=width, relief="solid", bd=1,
                         font=("Segoe UI", 10), highlightthickness=1, highlightbackground="#DCE4EF")
        entry.grid(row=row, column=1, sticky="ew", pady=6)
        return entry

    def _build_customers(self):
        tab = self.customers_tab
        self._section_heading(tab, "Policyholder Directory", "Add and maintain customer records. Customer IDs are generated automatically.")
        form = tk.LabelFrame(tab, text="Customer Details", bg=BG, fg=NAVY, padx=12, pady=10,
                             font=("Segoe UI", 10, "bold"))
        form.pack(fill="x", pady=(0, 12))
        self.c_vars = {k: tk.StringVar() for k in ("id", "name", "dob", "phone", "email", "address")}
        self._form_row(form, "Customer ID (for update/delete)", self.c_vars["id"], 0)
        self._form_row(form, "Full name *", self.c_vars["name"], 1)
        self._form_row(form, "Date of birth (YYYY-MM-DD) *", self.c_vars["dob"], 2)
        self._form_row(form, "Phone *", self.c_vars["phone"], 3)
        self._form_row(form, "Email", self.c_vars["email"], 4)
        self._form_row(form, "Address", self.c_vars["address"], 5)
        form.columnconfigure(1, weight=1)
        buttons = tk.Frame(form, bg=BG)
        buttons.grid(row=0, column=2, rowspan=6, padx=25, sticky="n")
        self._button(buttons, "Add Customer", self.add_customer).pack(fill="x", pady=4)
        self._button(buttons, "Update Selected ID", self.update_customer, False).pack(fill="x", pady=4)
        self._button(buttons, "Delete Customer", self.delete_customer, False).pack(fill="x", pady=4)
        self._button(buttons, "Clear Form", self.clear_customer).pack(fill="x", pady=4)
        self.customer_tree = self._make_tree(tab, ("id", "name", "dob", "phone", "email", "address"),
                                             ("ID", "Full Name", "Date of Birth", "Phone", "Email", "Address"))
        self.customer_tree.pack(fill="both", expand=True)
        self.customer_tree.bind("<<TreeviewSelect>>", self.select_customer)

    def _build_policies(self):
        tab = self.policies_tab
        self._section_heading(tab, "Insurance Policies", "Create and manage coverage records linked to a policyholder.")
        form = tk.LabelFrame(tab, text="Policy Details", bg=BG, fg=NAVY, padx=12, pady=10,
                             font=("Segoe UI", 10, "bold"))
        form.pack(fill="x", pady=(0, 12))
        self.p_vars = {k: tk.StringVar() for k in ("id", "number", "customer", "type", "sum", "premium", "start", "term", "status")}
        self._form_row(form, "Policy ID (for update/delete)", self.p_vars["id"], 0)
        self._form_row(form, "Policy number *", self.p_vars["number"], 1)
        tk.Label(form, text="Customer ID *", bg=BG, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=6)
        self.customer_combo = ttk.Combobox(form, textvariable=self.p_vars["customer"], state="readonly", width=25)
        self.customer_combo.grid(row=2, column=1, sticky="ew", pady=6)
        tk.Label(form, text="Policy type *", bg=BG, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=6)
        self.policy_type_combo = ttk.Combobox(form, textvariable=self.p_vars["type"],
            values=("Term Life", "Endowment", "Whole Life", "Child Plan", "Retirement Plan"), state="readonly")
        self.policy_type_combo.grid(row=3, column=1, sticky="ew", pady=6)
        self._form_row(form, "Sum assured (₹) *", self.p_vars["sum"], 4)
        self._form_row(form, "Annual premium (₹) *", self.p_vars["premium"], 5)
        self._form_row(form, "Start date (YYYY-MM-DD) *", self.p_vars["start"], 6)
        self._form_row(form, "Term in years *", self.p_vars["term"], 7)
        tk.Label(form, text="Status", bg=BG, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=8, column=0, sticky="w", padx=(0, 10), pady=6)
        self.status_combo = ttk.Combobox(form, textvariable=self.p_vars["status"], values=("Active", "Lapsed", "Matured", "Cancelled"), state="readonly")
        self.status_combo.grid(row=8, column=1, sticky="ew", pady=6)
        form.columnconfigure(1, weight=1)
        buttons = tk.Frame(form, bg=BG)
        buttons.grid(row=0, column=2, rowspan=9, padx=25, sticky="n")
        self._button(buttons, "Create Policy", self.add_policy).pack(fill="x", pady=4)
        self._button(buttons, "Update Selected ID", self.update_policy, False).pack(fill="x", pady=4)
        self._button(buttons, "Delete Policy", self.delete_policy, False).pack(fill="x", pady=4)
        self._button(buttons, "Clear Form", self.clear_policy).pack(fill="x", pady=4)
        self._button(buttons, "Estimate Premium", self.estimate_premium).pack(fill="x", pady=4)
        self.policy_tree = self._make_tree(tab, ("id", "number", "customer", "type", "sum", "premium", "start", "term", "status"),
            ("ID", "Policy No.", "Customer", "Type", "Sum Assured", "Annual Premium", "Start Date", "Term", "Status"))
        self.policy_tree.pack(fill="both", expand=True)
        self.policy_tree.bind("<<TreeviewSelect>>", self.select_policy)

    def _build_payments(self):
        tab = self.payments_tab
        self._section_heading(tab, "Premium Payments", "Record a payment against a policy and view the transaction history.")
        form = tk.LabelFrame(tab, text="Payment Details", bg=BG, fg=NAVY, padx=12, pady=10,
                             font=("Segoe UI", 10, "bold"))
        form.pack(fill="x", pady=(0, 12))
        self.pay_vars = {k: tk.StringVar() for k in ("policy", "date", "amount", "mode", "ref")}
        tk.Label(form, text="Policy *", bg=BG, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=6)
        self.payment_policy_combo = ttk.Combobox(form, textvariable=self.pay_vars["policy"], state="readonly", width=25)
        self.payment_policy_combo.grid(row=0, column=1, sticky="ew", pady=6)
        self._form_row(form, "Payment date (YYYY-MM-DD) *", self.pay_vars["date"], 1)
        self._form_row(form, "Amount (₹) *", self.pay_vars["amount"], 2)
        tk.Label(form, text="Payment mode *", bg=BG, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=6)
        self.payment_mode_combo = ttk.Combobox(form, textvariable=self.pay_vars["mode"], values=("UPI", "Cash", "Debit/Credit Card", "Net Banking", "Cheque"), state="readonly")
        self.payment_mode_combo.grid(row=3, column=1, sticky="ew", pady=6)
        self._form_row(form, "Transaction reference *", self.pay_vars["ref"], 4)
        form.columnconfigure(1, weight=1)
        buttons = tk.Frame(form, bg=BG)
        buttons.grid(row=0, column=2, rowspan=5, padx=25, sticky="n")
        self._button(buttons, "Record Payment", self.add_payment).pack(fill="x", pady=4)
        self._button(buttons, "Clear Form", self.clear_payment, False).pack(fill="x", pady=4)
        self.payment_tree = self._make_tree(tab, ("id", "number", "customer", "date", "amount", "mode", "ref"),
            ("Payment ID", "Policy No.", "Policyholder", "Date", "Amount", "Mode", "Transaction Ref"))
        self.payment_tree.pack(fill="both", expand=True)

    def _build_beneficiaries(self):
        tab = self.beneficiaries_tab
        self._section_heading(tab, "Beneficiary Register", "Maintain beneficiary details for each policy. Use fictional data in this school project.")
        form = tk.LabelFrame(tab, text="Beneficiary Details", bg=BG, fg=NAVY, padx=12, pady=10,
                             font=("Segoe UI", 10, "bold"))
        form.pack(fill="x", pady=(0, 12))
        self.b_vars = {k: tk.StringVar() for k in ("policy", "name", "relationship", "phone")}
        tk.Label(form, text="Policy *", bg=BG, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=6)
        self.beneficiary_policy_combo = ttk.Combobox(form, textvariable=self.b_vars["policy"], state="readonly", width=25)
        self.beneficiary_policy_combo.grid(row=0, column=1, sticky="ew", pady=6)
        self._form_row(form, "Beneficiary full name *", self.b_vars["name"], 1)
        self._form_row(form, "Relationship *", self.b_vars["relationship"], 2)
        self._form_row(form, "Phone", self.b_vars["phone"], 3)
        form.columnconfigure(1, weight=1)
        buttons = tk.Frame(form, bg=BG)
        buttons.grid(row=0, column=2, rowspan=4, padx=25, sticky="n")
        self._button(buttons, "Add Beneficiary", self.add_beneficiary).pack(fill="x", pady=4)
        self._button(buttons, "Delete Selected", self.delete_beneficiary, False).pack(fill="x", pady=4)
        self.beneficiary_tree = self._make_tree(tab, ("id", "number", "name", "relationship", "phone"),
            ("ID", "Policy No.", "Beneficiary", "Relationship", "Phone"))
        self.beneficiary_tree.pack(fill="both", expand=True)

    def _build_reports(self):
        tab = self.reports_tab
        self._section_heading(tab, "Reports & SQL Explorer", "Run built-in reports and view selected SQL query results.")
        actions = tk.Frame(tab, bg=BG)
        actions.pack(fill="x", pady=(0, 12))
        self._button(actions, "Policy Summary", lambda: self.show_report("summary")).pack(side="left", padx=(0, 8))
        self._button(actions, "Premium Collections", lambda: self.show_report("collections")).pack(side="left", padx=8)
        self._button(actions, "Policies by Status", lambda: self.show_report("status")).pack(side="left", padx=8)
        self._button(actions, "Export Current Report CSV", self.export_report, False).pack(side="right")
        self.report_title = tk.Label(tab, text="Policy Summary", bg=BG, fg=NAVY, font=("Segoe UI", 12, "bold"))
        self.report_title.pack(anchor="w", pady=(0, 8))
        self.report_tree = self._make_tree(tab, ("a", "b", "c", "d"), ("Column 1", "Column 2", "Column 3", "Column 4"))
        self.report_tree.pack(fill="both", expand=True)
        self._button(tab, "Show SQL used in this project", self.show_sql_notes, False).pack(anchor="w", pady=10)
        self.report_rows = []
        self.report_columns = ("a", "b", "c", "d")

    def refresh_all(self):
        self.refresh_customers()
        self.refresh_policies()
        self.refresh_payments()
        self.refresh_beneficiaries()
        self.refresh_dashboard()
        self.show_report("summary")

    def refresh_customers(self):
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        with connect_db() as conn:
            rows = conn.execute("SELECT * FROM customers ORDER BY customer_id DESC").fetchall()
        for r in rows:
            self.customer_tree.insert("", "end", values=(r["customer_id"], r["full_name"], r["dob"], r["phone"], r["email"] or "", r["address"] or ""))
        self.refresh_combos()

    def refresh_combos(self):
        with connect_db() as conn:
            customers = conn.execute("SELECT customer_id, full_name FROM customers ORDER BY full_name").fetchall()
            policies = conn.execute("""SELECT p.policy_id, p.policy_number, c.full_name
                                       FROM policies p JOIN customers c ON c.customer_id=p.customer_id
                                       ORDER BY p.policy_number""").fetchall()
        self.customer_combo["values"] = [f'{r["customer_id"]} - {r["full_name"]}' for r in customers]
        self.payment_policy_combo["values"] = [f'{r["policy_id"]} - {r["policy_number"]} ({r["full_name"]})' for r in policies]
        self.beneficiary_policy_combo["values"] = [f'{r["policy_id"]} - {r["policy_number"]} ({r["full_name"]})' for r in policies]

    def refresh_policies(self):
        for item in self.policy_tree.get_children():
            self.policy_tree.delete(item)
        with connect_db() as conn:
            rows = conn.execute("""SELECT p.*, c.full_name FROM policies p
                                   JOIN customers c ON c.customer_id=p.customer_id
                                   ORDER BY p.policy_id DESC""").fetchall()
        for r in rows:
            self.policy_tree.insert("", "end", values=(r["policy_id"], r["policy_number"], f'{r["customer_id"]} - {r["full_name"]}',
                r["policy_type"], money(r["sum_assured"]), money(r["annual_premium"]), r["start_date"], r["term_years"], r["status"]))

    def refresh_payments(self):
        for item in self.payment_tree.get_children():
            self.payment_tree.delete(item)
        with connect_db() as conn:
            rows = conn.execute("""SELECT pay.*, p.policy_number, c.full_name
                FROM payments pay JOIN policies p ON p.policy_id=pay.policy_id
                JOIN customers c ON c.customer_id=p.customer_id
                ORDER BY pay.payment_id DESC""").fetchall()
        for r in rows:
            self.payment_tree.insert("", "end", values=(r["payment_id"], r["policy_number"], r["full_name"],
                r["payment_date"], money(r["amount"]), r["payment_mode"], r["transaction_ref"]))

    def refresh_beneficiaries(self):
        for item in self.beneficiary_tree.get_children():
            self.beneficiary_tree.delete(item)
        with connect_db() as conn:
            rows = conn.execute("""SELECT b.*, p.policy_number FROM beneficiaries b
                JOIN policies p ON p.policy_id=b.policy_id ORDER BY b.beneficiary_id DESC""").fetchall()
        for r in rows:
            self.beneficiary_tree.insert("", "end", values=(r["beneficiary_id"], r["policy_number"], r["full_name"], r["relationship"], r["phone"] or ""))

    def refresh_dashboard(self):
        with connect_db() as conn:
            customers = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
            policies = conn.execute("SELECT COUNT(*) FROM policies").fetchone()[0]
            active = conn.execute("SELECT COUNT(*) FROM policies WHERE status='Active'").fetchone()[0]
            coverage = conn.execute("SELECT COALESCE(SUM(sum_assured),0) FROM policies WHERE status='Active'").fetchone()[0]
            payments = conn.execute("SELECT COUNT(*) FROM payments").fetchone()[0]
            rows = conn.execute("""SELECT p.policy_number, c.full_name, p.policy_type, p.annual_premium, p.status
                                   FROM policies p JOIN customers c ON c.customer_id=p.customer_id
                                   ORDER BY p.policy_id DESC LIMIT 8""").fetchall()
        self.stat_labels["customers"].configure(text=str(customers))
        self.stat_labels["policies"].configure(text=str(policies))
        self.stat_labels["active"].configure(text=str(active))
        self.stat_labels["coverage"].configure(text=money(coverage))
        self.stat_labels["payments"].configure(text=str(payments))
        for item in self.recent_tree.get_children():
            self.recent_tree.delete(item)
        for r in rows:
            self.recent_tree.insert("", "end", values=(r["policy_number"], r["full_name"], r["policy_type"], money(r["annual_premium"]), r["status"]))

    def clear_customer(self):
        for v in self.c_vars.values():
            v.set("")

    def add_customer(self):
        name, dob, phone = self.c_vars["name"].get().strip(), self.c_vars["dob"].get().strip(), self.c_vars["phone"].get().strip()
        if not name or not dob or not phone:
            messagebox.showwarning("Missing information", "Full name, date of birth and phone are required.")
            return
        if not valid_date(dob, "Date of birth"):
            return
        if not phone.isdigit() or not 7 <= len(phone) <= 15:
            messagebox.showwarning("Invalid phone", "Enter a phone number containing 7 to 15 digits.")
            return
        try:
            with connect_db() as conn:
                conn.execute("""INSERT INTO customers(full_name,dob,phone,email,address,created_on)
                                VALUES(?,?,?,?,?,?)""",
                    (name, dob, phone, self.c_vars["email"].get().strip(), self.c_vars["address"].get().strip(), date.today().isoformat()))
            self.clear_customer()
            self.refresh_all()
            messagebox.showinfo("Success", "Customer added successfully.")
        except sqlite3.Error as exc:
            messagebox.showerror("Database error", str(exc))

    def select_customer(self, _event=None):
        selected = self.customer_tree.selection()
        if not selected:
            return
        values = self.customer_tree.item(selected[0], "values")
        for key, value in zip(("id", "name", "dob", "phone", "email", "address"), values):
            self.c_vars[key].set(value)

    def update_customer(self):
        try:
            cid = int(self.c_vars["id"].get())
        except ValueError:
            messagebox.showwarning("Select a customer", "Select a customer row or enter a valid Customer ID.")
            return
        name, dob, phone = self.c_vars["name"].get().strip(), self.c_vars["dob"].get().strip(), self.c_vars["phone"].get().strip()
        if not name or not dob or not phone:
            messagebox.showwarning("Missing information", "Full name, date of birth and phone are required.")
            return
        if not valid_date(dob, "Date of birth"):
            return
        try:
            with connect_db() as conn:
                cur = conn.execute("""UPDATE customers SET full_name=?, dob=?, phone=?, email=?, address=?
                                      WHERE customer_id=?""",
                    (name, dob, phone, self.c_vars["email"].get().strip(), self.c_vars["address"].get().strip(), cid))
                if cur.rowcount == 0:
                    messagebox.showwarning("Not found", "No customer exists with that ID.")
                    return
            self.refresh_all()
            messagebox.showinfo("Success", "Customer updated successfully.")
        except sqlite3.Error as exc:
            messagebox.showerror("Database error", str(exc))

    def delete_customer(self):
        try:
            cid = int(self.c_vars["id"].get())
        except ValueError:
            messagebox.showwarning("Select a customer", "Select a customer row first.")
            return
        if not messagebox.askyesno("Confirm deletion", "Delete this customer? Customers linked to policies cannot be deleted."):
            return
        try:
            with connect_db() as conn:
                conn.execute("DELETE FROM customers WHERE customer_id=?", (cid,))
            self.clear_customer()
            self.refresh_all()
        except sqlite3.IntegrityError:
            messagebox.showerror("Cannot delete", "This customer has linked policies. Delete or reassign those policies first.")
        except sqlite3.Error as exc:
            messagebox.showerror("Database error", str(exc))

    def clear_policy(self):
        for v in self.p_vars.values():
            v.set("")
        self.p_vars["start"].set(date.today().isoformat())
        self.p_vars["status"].set("Active")

    def _selected_combo_id(self, value):
        try:
            return int(value.split(" - ", 1)[0])
        except (ValueError, AttributeError):
            return None

    def _policy_values(self):
        number = self.p_vars["number"].get().strip()
        customer_id = self._selected_combo_id(self.p_vars["customer"].get())
        ptype = self.p_vars["type"].get().strip()
        start = self.p_vars["start"].get().strip()
        status = self.p_vars["status"].get().strip() or "Active"
        if not number or not customer_id or not ptype or not start or not self.p_vars["sum"].get().strip() or not self.p_vars["premium"].get().strip() or not self.p_vars["term"].get().strip():
            messagebox.showwarning("Missing information", "Complete all required policy fields.")
            return None
        if not valid_date(start, "Start date"):
            return None
        try:
            insured = float(self.p_vars["sum"].get())
            premium = float(self.p_vars["premium"].get())
            term = int(self.p_vars["term"].get())
            if insured <= 0 or premium < 0 or term <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid numbers", "Sum assured must be positive, premium cannot be negative, and term must be a positive whole number.")
            return None
        return (number, customer_id, ptype, insured, premium, start, term, status)

    def add_policy(self):
        values = self._policy_values()
        if not values:
            return
        try:
            with connect_db() as conn:
                conn.execute("""INSERT INTO policies(policy_number,customer_id,policy_type,sum_assured,
                                annual_premium,start_date,term_years,status) VALUES(?,?,?,?,?,?,?,?)""", values)
            self.refresh_all()
            messagebox.showinfo("Success", "Policy created successfully.")
        except sqlite3.IntegrityError as exc:
            messagebox.showerror("Could not create policy", "Check that the policy number is unique and the customer exists.\n\n" + str(exc))
        except sqlite3.Error as exc:
            messagebox.showerror("Database error", str(exc))

    def select_policy(self, _event=None):
        selected = self.policy_tree.selection()
        if not selected:
            return
        values = self.policy_tree.item(selected[0], "values")
        self.p_vars["id"].set(values[0])
        self.p_vars["number"].set(values[1])
        self.p_vars["customer"].set(values[2])
        self.p_vars["type"].set(values[3])
        self.p_vars["sum"].set(str(values[4]).replace("₹", "").replace(",", ""))
        self.p_vars["premium"].set(str(values[5]).replace("₹", "").replace(",", ""))
        self.p_vars["start"].set(values[6])
        self.p_vars["term"].set(values[7])
        self.p_vars["status"].set(values[8])
        # Keep exact customer ID selected, regardless of name formatting.
        self.p_vars["customer"].set(values[2])

    def update_policy(self):
        try:
            pid = int(self.p_vars["id"].get())
        except ValueError:
            messagebox.showwarning("Select a policy", "Select a policy row first.")
            return
        values = self._policy_values()
        if not values:
            return
        try:
            with connect_db() as conn:
                cur = conn.execute("""UPDATE policies SET policy_number=?,customer_id=?,policy_type=?,sum_assured=?,
                    annual_premium=?,start_date=?,term_years=?,status=? WHERE policy_id=?""", values + (pid,))
                if cur.rowcount == 0:
                    messagebox.showwarning("Not found", "No policy exists with that ID.")
                    return
            self.refresh_all()
            messagebox.showinfo("Success", "Policy updated successfully.")
        except sqlite3.IntegrityError as exc:
            messagebox.showerror("Could not update policy", "Check the policy number and customer selection.\n\n" + str(exc))
        except sqlite3.Error as exc:
            messagebox.showerror("Database error", str(exc))

    def delete_policy(self):
        try:
            pid = int(self.p_vars["id"].get())
        except ValueError:
            messagebox.showwarning("Select a policy", "Select a policy row first.")
            return
        if not messagebox.askyesno("Confirm deletion", "Delete this policy? Policies with payment records cannot be deleted."):
            return
        try:
            with connect_db() as conn:
                conn.execute("DELETE FROM policies WHERE policy_id=?", (pid,))
            self.refresh_all()
            self.clear_policy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Cannot delete", "This policy has payment records. Keep it for transaction history or remove the payments first.")
        except sqlite3.Error as exc:
            messagebox.showerror("Database error", str(exc))

    def estimate_premium(self):
        try:
            amount = float(self.p_vars["sum"].get())
            term = int(self.p_vars["term"].get())
            if amount <= 0 or term <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Enter values", "Enter a positive sum assured and term first.")
            return
        # Educational estimate only; not based on actuarial tables or an insurer's rates.
        estimated = amount * 0.005 + (amount * 0.0005 * max(1, 20 - min(term, 20)))
        self.p_vars["premium"].set(f"{estimated:.2f}")
        messagebox.showinfo("Illustrative estimate", f"Estimated annual premium: {money(estimated)}\n\nThis simplified classroom formula is illustrative only and is not a real insurance quotation.")

    def clear_payment(self):
        for v in self.pay_vars.values():
            v.set("")
        self.pay_vars["date"].set(date.today().isoformat())

    def add_payment(self):
        policy_id = self._selected_combo_id(self.pay_vars["policy"].get())
        pdate, amount_text = self.pay_vars["date"].get().strip(), self.pay_vars["amount"].get().strip()
        mode, ref = self.pay_vars["mode"].get().strip(), self.pay_vars["ref"].get().strip()
        if not policy_id or not pdate or not amount_text or not mode or not ref:
            messagebox.showwarning("Missing information", "Complete all payment fields.")
            return
        if not valid_date(pdate, "Payment date"):
            return
        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid amount", "Payment amount must be a positive number.")
            return
        try:
            with connect_db() as conn:
                conn.execute("""INSERT INTO payments(policy_id,payment_date,amount,payment_mode,transaction_ref)
                                VALUES(?,?,?,?,?)""", (policy_id, pdate, amount, mode, ref))
            self.clear_payment()
            self.refresh_all()
            messagebox.showinfo("Success", "Payment recorded successfully.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate or invalid payment", "Transaction reference must be unique and the selected policy must exist.")
        except sqlite3.Error as exc:
            messagebox.showerror("Database error", str(exc))

    def add_beneficiary(self):
        policy_id = self._selected_combo_id(self.b_vars["policy"].get())
        name = self.b_vars["name"].get().strip()
        relationship = self.b_vars["relationship"].get().strip()
        phone = self.b_vars["phone"].get().strip()
        if not policy_id or not name or not relationship:
            messagebox.showwarning("Missing information", "Select a policy and enter beneficiary name and relationship.")
            return
        try:
            with connect_db() as conn:
                conn.execute("INSERT INTO beneficiaries(policy_id,full_name,relationship,phone) VALUES(?,?,?,?)",
                             (policy_id, name, relationship, phone))
            for v in self.b_vars.values():
                v.set("")
            self.refresh_all()
            messagebox.showinfo("Success", "Beneficiary added successfully.")
        except sqlite3.Error as exc:
            messagebox.showerror("Database error", str(exc))

    def delete_beneficiary(self):
        selected = self.beneficiary_tree.selection()
        if not selected:
            messagebox.showwarning("Select a beneficiary", "Select a beneficiary row first.")
            return
        bid = self.beneficiary_tree.item(selected[0], "values")[0]
        if not messagebox.askyesno("Confirm deletion", "Delete this beneficiary record?"):
            return
        with connect_db() as conn:
            conn.execute("DELETE FROM beneficiaries WHERE beneficiary_id=?", (bid,))
        self.refresh_all()

    def show_report(self, kind):
        with connect_db() as conn:
            if kind == "summary":
                title = "Policy Summary"
                cols = ("Policy No.", "Policyholder", "Type", "Sum Assured", "Annual Premium", "Status")
                rows = conn.execute("""SELECT p.policy_number,c.full_name,p.policy_type,p.sum_assured,
                    p.annual_premium,p.status FROM policies p JOIN customers c ON c.customer_id=p.customer_id
                    ORDER BY p.policy_number""").fetchall()
                data = [(r[0], r[1], r[2], money(r[3]), money(r[4]), r[5]) for r in rows]
            elif kind == "collections":
                title = "Premium Collections by Policy"
                cols = ("Policy No.", "Policyholder", "Expected Annual Premium", "Payments Recorded", "Total Collected", "Balance (illustrative)")
                rows = conn.execute("""SELECT p.policy_number,c.full_name,p.annual_premium,
                    COUNT(pay.payment_id),COALESCE(SUM(pay.amount),0)
                    FROM policies p JOIN customers c ON c.customer_id=p.customer_id
                    LEFT JOIN payments pay ON pay.policy_id=p.policy_id
                    GROUP BY p.policy_id ORDER BY p.policy_number""").fetchall()
                data = [(r[0], r[1], money(r[2]), str(r[3]), money(r[4]), money(max(0, r[2]-r[4]))) for r in rows]
            else:
                title = "Policies by Status"
                cols = ("Status", "Number of Policies", "Total Sum Assured", "Total Annual Premium")
                rows = conn.execute("""SELECT status,COUNT(*),COALESCE(SUM(sum_assured),0),
                    COALESCE(SUM(annual_premium),0) FROM policies GROUP BY status ORDER BY status""").fetchall()
                data = [(r[0], str(r[1]), money(r[2]), money(r[3])) for r in rows]
        self.report_title.configure(text=title)
        self.report_columns = cols
        self.report_rows = data
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        self.report_tree["columns"] = tuple(f"c{i}" for i in range(len(cols)))
        self.report_tree["show"] = "headings"
        for i, col in enumerate(cols):
            self.report_tree.heading(f"c{i}", text=col)
            self.report_tree.column(f"c{i}", width=max(130, min(240, len(col)*9)), minwidth=90, anchor="w")
        for row in data:
            self.report_tree.insert("", "end", values=row)

    def export_report(self):
        if not self.report_rows:
            messagebox.showinfo("Nothing to export", "Run a report first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")],
                                            initialfile="lifeguard_report.csv")
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(self.report_columns)
                writer.writerows(self.report_rows)
            messagebox.showinfo("Export complete", f"Report saved to:\n{path}")
        except OSError as exc:
            messagebox.showerror("Export error", str(exc))

    def show_sql_notes(self):
        notes = (
            "SQL CONCEPTS DEMONSTRATED\n\n"
            "1. CREATE TABLE — creates customers, policies, beneficiaries and payments.\n"
            "2. INSERT — adds customers, policies, beneficiaries and payments.\n"
            "3. SELECT — retrieves records for tables, dashboard and reports.\n"
            "4. UPDATE — modifies existing customer and policy records.\n"
            "5. DELETE — removes selected records where database relationships allow it.\n"
            "6. WHERE — filters policies by status and finds records by ID.\n"
            "7. JOIN — combines policy records with customer and payment details.\n"
            "8. GROUP BY + aggregate functions — COUNT, SUM and COALESCE generate summaries.\n"
            "9. PRIMARY KEY / FOREIGN KEY — connects related tables and protects referential integrity.\n"
            "10. Parameterised queries — values are passed separately to SQL to reduce injection risk.\n\n"
            "Database file: lifeguard.db (created automatically beside main.py)\n"
            "SQL schema file: schema.sql"
        )
        messagebox.showinfo("SQL concepts", notes)


if __name__ == "__main__":
    try:
        app = LifeGuardApp()
        app.mainloop()
    except Exception as exc:
        messagebox.showerror("LifeGuard could not start", f"An unexpected error occurred:\n{exc}\n\nCheck that Python 3 and Tkinter are installed.")
        raise
