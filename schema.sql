-- LifeGuard: Life Insurance Management System
-- CBSE Class XII Computer Science Project
-- Compatible with SQLite 3. The application creates these tables automatically.

PRAGMA foreign_keys = ON;

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
