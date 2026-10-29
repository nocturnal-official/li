import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

# ---------------------------------------------------------------
# 1. DATABASE SETUP
# ---------------------------------------------------------------
conn = sqlite3.connect("lifeguard.db")
conn.execute("PRAGMA foreign_keys = ON")   # enforce FOREIGN KEY rules
cur = conn.cursor()


def create_tables():
    cur.execute("""CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name   TEXT NOT NULL,
        dob         TEXT NOT NULL,
        phone       TEXT NOT NULL,
        email       TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS policies (
        policy_id      INTEGER PRIMARY KEY AUTOINCREMENT,
        policy_number  TEXT NOT NULL UNIQUE,
        customer_id    INTEGER NOT NULL,
        policy_type    TEXT NOT NULL,
        sum_assured    REAL NOT NULL,
        annual_premium REAL NOT NULL,
        start_date     TEXT NOT NULL,
        term_years     INTEGER NOT NULL,
        status         TEXT DEFAULT 'Active',
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS payments (
        payment_id      INTEGER PRIMARY KEY AUTOINCREMENT,
        policy_id       INTEGER NOT NULL,
        payment_date    TEXT NOT NULL,
        amount          REAL NOT NULL,
        payment_mode    TEXT NOT NULL,
        transaction_ref TEXT NOT NULL UNIQUE,
        FOREIGN KEY (policy_id) REFERENCES policies(policy_id))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS beneficiaries (
        beneficiary_id INTEGER PRIMARY KEY AUTOINCREMENT,
        policy_id      INTEGER NOT NULL,
        full_name      TEXT NOT NULL,
        relationship   TEXT NOT NULL,
        phone          TEXT,
        FOREIGN KEY (policy_id) REFERENCES policies(policy_id)
            ON DELETE CASCADE)""")
    conn.commit()


def add_sample_data():
    """Insert demo records only if the database is empty."""
    if query("SELECT COUNT(*) FROM customers")[0][0] > 0:
        return
    today = date.today().isoformat()
    cur.execute("INSERT INTO customers(full_name,dob,phone,email) VALUES (?,?,?,?)",
                ("Aarav Sharma", "1985-04-12", "9876543210", "aarav@example.com"))
    cur.execute("INSERT INTO customers(full_name,dob,phone,email) VALUES (?,?,?,?)",
                ("Meera Kapoor", "1990-09-23", "9876501234", "meera@example.com"))
    cur.execute("""INSERT INTO policies(policy_number,customer_id,policy_type,sum_assured,
                   annual_premium,start_date,term_years) VALUES (?,?,?,?,?,?,?)""",
                ("LG-10001", 1, "Term Life", 2500000, 12500, today, 20))
    cur.execute("""INSERT INTO policies(policy_number,customer_id,policy_type,sum_assured,
                   annual_premium,start_date,term_years) VALUES (?,?,?,?,?,?,?)""",
                ("LG-10002", 2, "Endowment", 1500000, 42000, today, 15))
    cur.execute("INSERT INTO beneficiaries(policy_id,full_name,relationship,phone) VALUES (?,?,?,?)",
                (1, "Ananya Sharma", "Spouse", "9876500001"))
    cur.execute("INSERT INTO payments(policy_id,payment_date,amount,payment_mode,transaction_ref) "
                "VALUES (?,?,?,?,?)", (1, today, 12500, "UPI", "TXN-1001"))
    conn.commit()


# ---------------------------------------------------------------
# 2. HELPER FUNCTIONS
# ---------------------------------------------------------------
def query(sql, params=()):
    """Run a SELECT and return all rows."""
    cur.execute(sql, params)
    return cur.fetchall()


def execute(sql, params=()):
    """Run INSERT / UPDATE / DELETE. Returns True if successful."""
    try:
        cur.execute(sql, params)
        conn.commit()
        return True
    except sqlite3.Error as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Could not complete the action.\n\n{e}")
        return False


def valid_date(text):
    try:
        datetime.strptime(text, "%Y-%m-%d")
        return True
    except ValueError:
        messagebox.showwarning("Invalid date", "Date must be in YYYY-MM-DD format.")
        return False


def make_tab(title):
    frame = tk.Frame(notebook)
    notebook.add(frame, text=title)
    return frame


def make_form(parent, fields):
    """Create labelled input boxes. fields = [(key, label, options_or_None), ...]
    Returns a dictionary {key: StringVar}."""
    form = ttk.LabelFrame(parent, text="  DETAILS  ", padding=(14, 10))
    form.pack(fill="x", padx=14, pady=(12, 8))
    variables = {}
    for i, (key, label, options) in enumerate(fields):
        var = tk.StringVar()
        variables[key] = var
        row, col = i // 2, (i % 2) * 2
        ttk.Label(form, text=label).grid(row=row, column=col, sticky="w", padx=(6, 8), pady=7)
        if options:
            widget = ttk.Combobox(form, textvariable=var, values=options,
                                  state="readonly", width=28, style="Field.TCombobox")
        else:
            widget = ttk.Entry(form, textvariable=var, width=31, style="Field.TEntry")
        widget.grid(row=row, column=col + 1, sticky="ew", padx=(0, 14), pady=7)
        form.grid_columnconfigure(col + 1, weight=1)
    return variables


def make_buttons(parent, buttons):
    """buttons = [(text, function), ...]"""
    bar = ttk.Frame(parent, padding=(14, 2, 14, 8))
    bar.pack(fill="x")
    for i, (text, command) in enumerate(buttons):
        style = "Danger.TButton" if text == "Delete" else (
            "Primary.TButton" if text in ("Add", "Record Payment", "Update") else "Action.TButton")
        ttk.Button(bar, text=text, command=command, style=style).pack(side="left", padx=(0, 8), pady=3)


def make_table(parent, headings):
    frame = ttk.Frame(parent, padding=(14, 4, 14, 14))
    frame.pack(fill="both", expand=True)
    tree = ttk.Treeview(frame, columns=headings, show="headings", height=10,
                        style="Records.Treeview")
    for h in headings:
        tree.heading(h, text=h)
        tree.column(h, width=max(115, min(190, len(str(h)) * 10)), minwidth=90, anchor="w")
    yscroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    xscroll = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
    tree.grid(row=0, column=0, sticky="nsew")
    yscroll.grid(row=0, column=1, sticky="ns")
    xscroll.grid(row=1, column=0, sticky="ew")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    tree.tag_configure("odd", background="#F4F8FC")
    tree.tag_configure("even", background="#FFFFFF")
    return tree


def fill_table(tree, sql):
    """Clear a table and reload it using a SELECT query."""
    tree.delete(*tree.get_children())
    for index, row in enumerate(query(sql)):
        tree.insert("", "end", values=row, tags=("even" if index % 2 == 0 else "odd",))


def get_values(variables):
    return {key: var.get().strip() for key, var in variables.items()}


def clear_form(variables):
    for var in variables.values():
        var.set("")


def on_select(tree, variables):
    """When a row is clicked, copy its values into the form."""
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0], "values")
        for var, value in zip(variables.values(), values):
            var.set(value)


# ---------------------------------------------------------------
# 3. CUSTOMERS
# ---------------------------------------------------------------
def refresh_customers():
    fill_table(customer_tree,
               "SELECT customer_id, full_name, dob, phone, email FROM customers ORDER BY customer_id")


def check_customer(d):
    if not d["name"] or not d["dob"] or not d["phone"]:
        messagebox.showwarning("Missing data", "Name, date of birth and phone are required.")
        return False
    if not d["phone"].isdigit() or len(d["phone"]) != 10:
        messagebox.showwarning("Invalid phone", "Phone number must have exactly 10 digits.")
        return False
    return valid_date(d["dob"])


def add_customer():
    d = get_values(cust)
    if check_customer(d):
        if execute("INSERT INTO customers(full_name,dob,phone,email) VALUES (?,?,?,?)",
                   (d["name"], d["dob"], d["phone"], d["email"])):
            clear_form(cust)
            refresh_all()


def update_customer():
    d = get_values(cust)
    if not d["id"]:
        messagebox.showwarning("Select a row", "Click a customer row first.")
        return
    if check_customer(d):
        if execute("UPDATE customers SET full_name=?, dob=?, phone=?, email=? WHERE customer_id=?",
                   (d["name"], d["dob"], d["phone"], d["email"], d["id"])):
            refresh_all()


def delete_customer():
    d = get_values(cust)
    if not d["id"]:
        messagebox.showwarning("Select a row", "Click a customer row first.")
        return
    if messagebox.askyesno("Confirm", "Delete this customer?"):
        # Fails automatically if the customer still has policies (FOREIGN KEY)
        if execute("DELETE FROM customers WHERE customer_id=?", (d["id"],)):
            clear_form(cust)
            refresh_all()


# ---------------------------------------------------------------
# 4. POLICIES
# ---------------------------------------------------------------
def refresh_policies():
    fill_table(policy_tree, "SELECT * FROM policies ORDER BY policy_id")


def read_policy():
    """Validate the policy form. Returns a tuple of values, or None."""
    d = get_values(pol)
    if not all([d["number"], d["customer"], d["type"], d["sum"], d["premium"], d["start"], d["term"]]):
        messagebox.showwarning("Missing data", "Please fill all fields.")
        return None
    if not valid_date(d["start"]):
        return None
    try:
        sum_assured, premium, term = float(d["sum"]), float(d["premium"]), int(d["term"])
        if sum_assured <= 0 or premium < 0 or term <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Invalid number", "Check sum assured, premium and term values.")
        return None
    return (d["number"], d["customer"], d["type"], sum_assured, premium,
            d["start"], term, d["status"] or "Active")


def add_policy():
    values = read_policy()
    if values:
        if execute("""INSERT INTO policies(policy_number,customer_id,policy_type,sum_assured,
                      annual_premium,start_date,term_years,status) VALUES (?,?,?,?,?,?,?,?)""", values):
            refresh_all()


def update_policy():
    policy_id = pol["id"].get().strip()
    if not policy_id:
        messagebox.showwarning("Select a row", "Click a policy row first.")
        return
    values = read_policy()
    if values:
        if execute("""UPDATE policies SET policy_number=?, customer_id=?, policy_type=?, sum_assured=?,
                      annual_premium=?, start_date=?, term_years=?, status=? WHERE policy_id=?""",
                   values + (policy_id,)):
            refresh_all()


def delete_policy():
    policy_id = pol["id"].get().strip()
    if not policy_id:
        messagebox.showwarning("Select a row", "Click a policy row first.")
        return
    if messagebox.askyesno("Confirm", "Delete this policy?"):
        if execute("DELETE FROM policies WHERE policy_id=?", (policy_id,)):
            clear_form(pol)
            refresh_all()


def estimate_premium():
    """Simple classroom formula: 0.5% of the sum assured (not a real quote)."""
    try:
        premium = float(pol["sum"].get()) * 0.005
    except ValueError:
        messagebox.showwarning("Invalid", "Enter a valid sum assured first.")
        return
    pol["premium"].set(f"{premium:.2f}")


# ---------------------------------------------------------------
# 5. PAYMENTS
# ---------------------------------------------------------------
def refresh_payments():
    fill_table(payment_tree, "SELECT * FROM payments ORDER BY payment_id")


def add_payment():
    d = get_values(pay)
    if not all([d["policy"], d["date"], d["amount"], d["mode"], d["ref"]]):
        messagebox.showwarning("Missing data", "Please fill all fields.")
        return
    if not valid_date(d["date"]):
        return
    try:
        amount = float(d["amount"])
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Invalid amount", "Amount must be a positive number.")
        return
    if execute("""INSERT INTO payments(policy_id,payment_date,amount,payment_mode,transaction_ref)
                  VALUES (?,?,?,?,?)""", (d["policy"], d["date"], amount, d["mode"], d["ref"])):
        clear_form(pay)
        refresh_all()


# ---------------------------------------------------------------
# 6. BENEFICIARIES
# ---------------------------------------------------------------
def refresh_beneficiaries():
    fill_table(ben_tree, "SELECT * FROM beneficiaries ORDER BY beneficiary_id")


def add_beneficiary():
    d = get_values(ben)
    if not d["policy"] or not d["name"] or not d["relation"]:
        messagebox.showwarning("Missing data", "Policy ID, name and relationship are required.")
        return
    if execute("INSERT INTO beneficiaries(policy_id,full_name,relationship,phone) VALUES (?,?,?,?)",
               (d["policy"], d["name"], d["relation"], d["phone"])):
        clear_form(ben)
        refresh_all()


def delete_beneficiary():
    bid = ben["id"].get().strip()
    if not bid:
        messagebox.showwarning("Select a row", "Click a beneficiary row first.")
        return
    if execute("DELETE FROM beneficiaries WHERE beneficiary_id=?", (bid,)):
        clear_form(ben)
        refresh_all()


# ---------------------------------------------------------------
# 7. REPORTS (JOIN, GROUP BY, aggregate functions)
# ---------------------------------------------------------------
def show_report(kind):
    if kind == "summary":          # JOIN
        headings = ("Policy No.", "Policyholder", "Type", "Sum Assured", "Premium", "Status")
        sql = """SELECT p.policy_number, c.full_name, p.policy_type,
                        p.sum_assured, p.annual_premium, p.status
                 FROM policies p JOIN customers c ON p.customer_id = c.customer_id
                 ORDER BY p.policy_number"""
    elif kind == "collections":    # LEFT JOIN + GROUP BY
        headings = ("Policy No.", "Policyholder", "Annual Premium", "Payments Made", "Total Paid")
        sql = """SELECT p.policy_number, c.full_name, p.annual_premium,
                        COUNT(pay.payment_id), COALESCE(SUM(pay.amount), 0)
                 FROM policies p
                 JOIN customers c ON p.customer_id = c.customer_id
                 LEFT JOIN payments pay ON p.policy_id = pay.policy_id
                 GROUP BY p.policy_id
                 ORDER BY p.policy_number"""
    else:                          # GROUP BY status
        headings = ("Status", "No. of Policies", "Total Sum Assured", "Total Premium")
        sql = """SELECT status, COUNT(*), SUM(sum_assured), SUM(annual_premium)
                 FROM policies GROUP BY status"""

    report_title.config(text={"summary": "Policy Summary",
                              "collections": "Premium Collections",
                              "status": "Policies by Status"}[kind])
    report_tree["columns"] = headings
    for h in headings:
        report_tree.heading(h, text=h)
        report_tree.column(h, width=max(130, min(210, len(str(h)) * 10)), minwidth=100, anchor="w")
    fill_table(report_tree, sql)


def show_sql_notes():
    messagebox.showinfo("SQL concepts used",
        "CREATE TABLE  - customers, policies, payments, beneficiaries\n"
        "INSERT        - add new records\n"
        "SELECT        - display records\n"
        "UPDATE        - edit customers and policies\n"
        "DELETE        - remove records\n"
        "WHERE         - find a record by its ID\n"
        "JOIN          - combine policies with customers/payments\n"
        "GROUP BY      - COUNT and SUM in the reports\n"
        "PRIMARY KEY / FOREIGN KEY - link the tables\n"
        "? placeholders - parameterised queries (safe from SQL injection)")


# ---------------------------------------------------------------
# 8. REFRESH EVERYTHING
# ---------------------------------------------------------------
def refresh_all():
    refresh_customers()
    refresh_policies()
    refresh_payments()
    refresh_beneficiaries()
    show_report("summary")
    customers = query("SELECT COUNT(*) FROM customers")[0][0]
    policies = query("SELECT COUNT(*) FROM policies")[0][0]
    coverage = query("SELECT COALESCE(SUM(sum_assured),0) FROM policies WHERE status='Active'")[0][0]
    summary.config(text=f"Customers: {customers}   |   Policies: {policies}   |   "
                        f"Active coverage: Rs. {coverage:,.0f}")


# ---------------------------------------------------------------
# 9. BUILD THE WINDOW
# ---------------------------------------------------------------
create_tables()
add_sample_data()

root = tk.Tk()
root.title("LifeGuard | Life Insurance Management System")
root.geometry("1120x760")
root.minsize(940, 640)
root.configure(bg="#F3F6FA")

# A simple built-in ttk theme keeps the interface modern without extra packages.
style = ttk.Style(root)
style.theme_use("clam")
style.configure(".", font=("Segoe UI", 10))
style.configure("TFrame", background="#F3F6FA")
style.configure("TLabel", background="#F3F6FA", foreground="#23344D")
style.configure("TLabelframe", background="#FFFFFF", bordercolor="#D9E3EF")
style.configure("TLabelframe.Label", background="#FFFFFF", foreground="#176B70",
                font=("Segoe UI", 10, "bold"))
style.configure("TNotebook", background="#F3F6FA", borderwidth=0, tabmargins=(5, 5, 5, 0))
style.configure("TNotebook.Tab", padding=(18, 10), background="#E5ECF4",
                foreground="#34445B", font=("Segoe UI", 10, "bold"))
style.map("TNotebook.Tab", background=[("selected", "#FFFFFF")],
          foreground=[("selected", "#087F8C")])
style.configure("TEntry", padding=7, fieldbackground="#FFFFFF")
style.configure("TCombobox", padding=7, fieldbackground="#FFFFFF")
style.configure("Field.TEntry", padding=7)
style.configure("Field.TCombobox", padding=7)
style.configure("Primary.TButton", padding=(14, 8), background="#087F8C",
                foreground="#FFFFFF", font=("Segoe UI", 9, "bold"), borderwidth=0)
style.map("Primary.TButton", background=[("active", "#06656F")])
style.configure("Action.TButton", padding=(13, 8), background="#E1EAF3",
                foreground="#263A52", borderwidth=0)
style.map("Action.TButton", background=[("active", "#D0DFEC")])
style.configure("Danger.TButton", padding=(13, 8), background="#FCE8E8",
                foreground="#A52A2A", borderwidth=0)
style.map("Danger.TButton", background=[("active", "#F7D1D1")])
style.configure("Records.Treeview", rowheight=30, background="#FFFFFF",
                fieldbackground="#FFFFFF", foreground="#26364D",
                bordercolor="#DCE5EF", borderwidth=0, font=("Segoe UI", 9))
style.configure("Records.Treeview.Heading", background="#E8EFF6",
                foreground="#24364D", font=("Segoe UI", 9, "bold"), padding=(8, 10))
style.map("Records.Treeview", background=[("selected", "#CBECEF")],
          foreground=[("selected", "#173A45")])

header = tk.Frame(root, bg="#142B45", padx=22, pady=15)
header.pack(fill="x")
tk.Label(header, text="LIFEGUARD", font=("Segoe UI", 21, "bold"),
         bg="#142B45", fg="#FFFFFF").pack(anchor="w")
tk.Label(header, text="LIFE INSURANCE MANAGEMENT SYSTEM  •  CBSE CLASS XII PROJECT",
         font=("Segoe UI", 9, "bold"), bg="#142B45", fg="#8FE0D8").pack(anchor="w", pady=(2, 0))

summary_bar = tk.Frame(root, bg="#FFFFFF", padx=18, pady=11,
                       highlightbackground="#DCE5EF", highlightthickness=1)
summary_bar.pack(fill="x", padx=14, pady=(12, 4))
tk.Label(summary_bar, text="OVERVIEW", bg="#FFFFFF", fg="#087F8C",
         font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 14))
summary = tk.Label(summary_bar, text="", font=("Segoe UI", 10, "bold"),
                   bg="#FFFFFF", fg="#26364D", pady=2, anchor="w")
summary.pack(side="left", fill="x", expand=True)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=(4, 10))

# --- Customers tab ---
tab = make_tab("Customers")
cust = make_form(tab, [("id", "Customer ID (auto)", None), ("name", "Full name *", None),
                       ("dob", "DOB (YYYY-MM-DD) *", None), ("phone", "Phone (10 digits) *", None),
                       ("email", "Email", None)])
make_buttons(tab, [("Add", add_customer), ("Update", update_customer),
                   ("Delete", delete_customer), ("Clear", lambda: clear_form(cust))])
customer_tree = make_table(tab, ("ID", "Name", "DOB", "Phone", "Email"))
customer_tree.bind("<<TreeviewSelect>>", lambda e: on_select(customer_tree, cust))

# --- Policies tab ---
tab = make_tab("Policies")
pol = make_form(tab, [("id", "Policy ID (auto)", None), ("number", "Policy number *", None),
                      ("customer", "Customer ID *", None),
                      ("type", "Policy type *", ["Term Life", "Endowment", "Whole Life", "Child Plan"]),
                      ("sum", "Sum assured *", None), ("premium", "Annual premium *", None),
                      ("start", "Start date (YYYY-MM-DD) *", None), ("term", "Term (years) *", None),
                      ("status", "Status", ["Active", "Lapsed", "Matured", "Cancelled"])])
pol["start"].set(date.today().isoformat())
pol["status"].set("Active")
make_buttons(tab, [("Add", add_policy), ("Update", update_policy), ("Delete", delete_policy),
                   ("Estimate Premium", estimate_premium), ("Clear", lambda: clear_form(pol))])
policy_tree = make_table(tab, ("ID", "Policy No.", "Customer ID", "Type", "Sum Assured",
                               "Premium", "Start", "Term", "Status"))
policy_tree.bind("<<TreeviewSelect>>", lambda e: on_select(policy_tree, pol))

# --- Payments tab ---
tab = make_tab("Payments")
pay = make_form(tab, [("policy", "Policy ID *", None), ("date", "Date (YYYY-MM-DD) *", None),
                      ("amount", "Amount *", None),
                      ("mode", "Payment mode *", ["UPI", "Cash", "Card", "Net Banking", "Cheque"]),
                      ("ref", "Transaction reference *", None)])
pay["date"].set(date.today().isoformat())
make_buttons(tab, [("Record Payment", add_payment), ("Clear", lambda: clear_form(pay))])
payment_tree = make_table(tab, ("ID", "Policy ID", "Date", "Amount", "Mode", "Reference"))

# --- Beneficiaries tab ---
tab = make_tab("Beneficiaries")
ben = make_form(tab, [("id", "Beneficiary ID (auto)", None), ("policy", "Policy ID *", None),
                      ("name", "Full name *", None), ("relation", "Relationship *", None),
                      ("phone", "Phone", None)])
make_buttons(tab, [("Add", add_beneficiary), ("Delete", delete_beneficiary),
                   ("Clear", lambda: clear_form(ben))])
ben_tree = make_table(tab, ("ID", "Policy ID", "Name", "Relationship", "Phone"))
ben_tree.bind("<<TreeviewSelect>>", lambda e: on_select(ben_tree, ben))

# --- Reports tab ---
tab = make_tab("Reports")
make_buttons(tab, [("Policy Summary", lambda: show_report("summary")),
                   ("Premium Collections", lambda: show_report("collections")),
                   ("Policies by Status", lambda: show_report("status")),
                   ("SQL Concepts", show_sql_notes)])
report_title = tk.Label(tab, text="", font=("Arial", 12, "bold"))
report_title.pack(anchor="w", padx=12)
report_tree = make_table(tab, ("a", "b"))

refresh_all()
root.mainloop()
conn.close()
