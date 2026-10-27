# LifeGuard — Life Insurance Management System
## Computer Science Project | Class XII | CBSE

**Student Name:** __________________________  
**Class/Section:** XII ______  
**Roll Number:** __________________________  
**School:** _______________________________  
**Session:** ______________________________  
**Subject Teacher:** ______________________

---

## Certificate

This is to certify that __________________________ of Class XII has completed the Computer Science project titled **“LifeGuard — Life Insurance Management System”** under my guidance. The project demonstrates the use of Python programming, a graphical user interface, SQL database operations, data validation and report generation.

**Teacher's Signature:** ____________________  
**Date:** ____________________

## Acknowledgement

I would like to express my sincere gratitude to my Computer Science teacher for guidance and support during this project. I am also thankful to my school for providing the opportunity to apply programming and database concepts to a practical problem. This project helped me understand how a Python application can interact with a relational database to store, retrieve and manage information.

## Index

1. Introduction
2. Problem Statement
3. Objectives
4. Scope
5. Hardware and Software Requirements
6. System Design
7. Database Design
8. Main Features
9. Algorithms
10. Testing
11. Limitations
12. Future Scope
13. Conclusion
14. Bibliography

## 1. Introduction

Life insurance is a financial product designed to provide financial protection to beneficiaries under the terms of an insurance policy. An insurance office may need to maintain policyholder details, policy information, beneficiary records and premium payment history. Maintaining these records manually can be time-consuming and may lead to duplication or difficulty retrieving information.

LifeGuard is a desktop-based demonstration application developed using Python, Tkinter and SQL. It provides a graphical interface for managing fictional policyholder and insurance records. SQLite is used as the relational database engine so that the application can run without a separately installed database server.

## 2. Problem Statement

To develop a user-friendly computerised system that stores and manages life insurance policyholder details, policy information, beneficiaries and premium payments. The system should allow records to be added, viewed, updated and deleted where appropriate, and should generate useful summaries and export reports.

## 3. Objectives

- To create a graphical user interface using Tkinter.
- To store data persistently in a relational SQL database.
- To implement database operations such as INSERT, SELECT, UPDATE and DELETE.
- To connect related records using primary and foreign keys.
- To validate dates, numeric values and required fields.
- To use JOIN and aggregate queries for meaningful reports.
- To export reports in CSV format.
- To demonstrate modular programming and exception handling in Python.

## 4. Scope

The application is intended for educational demonstration. It manages fictional customer records, policy records, beneficiaries and payment entries. It is not connected to an insurance company, payment gateway, identity verification service or live actuarial pricing system.

## 5. Hardware and Software Requirements

### Hardware
- Computer or laptop
- Minimum 4 GB RAM recommended
- Keyboard, mouse and display

### Software
- Windows, macOS or Linux with a supported Python installation
- Python 3.9 or newer recommended
- Tkinter GUI library
- SQLite database engine through Python's `sqlite3` module
- Any text editor or Python IDE

No external Python package installation is required for the standard project.

## 6. System Design

### Architecture

1. **Presentation layer:** Tkinter forms, tabs, buttons, dashboard and tables.
2. **Application layer:** Python functions for validation, calculations, user actions and exception handling.
3. **Data layer:** SQLite database with four related tables.

### Workflow

1. The application starts and creates the database tables if they do not exist.
2. Fictional demonstration records are inserted only when the customer table is empty.
3. The dashboard reads summary values from SQL queries.
4. The user enters information through forms.
5. Python validates the input and executes parameterised SQL statements.
6. The interface refreshes to display the updated records.
7. Reports can be viewed and exported as CSV.

## 7. Database Design

### Table: customers

| Field | Type | Description |
|---|---|---|
| customer_id | INTEGER | Primary key; auto-generated |
| full_name | TEXT | Customer's full name |
| dob | TEXT | Date of birth in YYYY-MM-DD format |
| phone | TEXT | Contact number |
| email | TEXT | Email address |
| address | TEXT | Address |
| created_on | TEXT | Record creation date |

### Table: policies

| Field | Type | Description |
|---|---|---|
| policy_id | INTEGER | Primary key |
| policy_number | TEXT | Unique policy number |
| customer_id | INTEGER | Foreign key to customers |
| policy_type | TEXT | Type of insurance policy |
| sum_assured | REAL | Illustrative coverage amount |
| annual_premium | REAL | Annual premium entered or estimated |
| start_date | TEXT | Policy start date |
| term_years | INTEGER | Policy term in years |
| status | TEXT | Active, Lapsed, Matured or Cancelled |

### Table: beneficiaries

| Field | Type | Description |
|---|---|---|
| beneficiary_id | INTEGER | Primary key |
| policy_id | INTEGER | Foreign key to policies |
| full_name | TEXT | Beneficiary's name |
| relationship | TEXT | Relationship to policyholder |
| phone | TEXT | Contact number |

### Table: payments

| Field | Type | Description |
|---|---|---|
| payment_id | INTEGER | Primary key |
| policy_id | INTEGER | Foreign key to policies |
| payment_date | TEXT | Date of payment |
| amount | REAL | Payment amount |
| payment_mode | TEXT | UPI, cash, card, net banking or cheque |
| transaction_ref | TEXT | Unique transaction reference |

### Relationships

- One customer can have multiple policies.
- One policy can have multiple payment records.
- One policy can have multiple beneficiary records.
- Foreign keys maintain relationships between tables.

## 8. Main Features

1. Dashboard showing total customers, policies, active policies, coverage and recorded payments.
2. Customer management with add, update, view and delete operations.
3. Policy management with status, sum assured, annual premium and term.
4. An illustrative premium estimator.
5. Premium payment recording with unique transaction references.
6. Beneficiary management.
7. Reports for policy summary, premium collections and policies by status.
8. CSV report export.
9. Input validation and database error handling.

## 9. Algorithms

### Algorithm A: Add a customer
1. Accept customer details from the form.
2. Check that required fields are not empty.
3. Validate the date and phone number.
4. Execute an INSERT query using parameterised values.
5. Refresh the customer table and dashboard.
6. Display a success or error message.

### Algorithm B: Create a policy
1. Accept the policy number, customer ID, policy type, coverage, premium, start date, term and status.
2. Validate required fields and numeric values.
3. Validate the date format.
4. Insert the policy into the database.
5. Handle duplicate policy numbers and database errors.
6. Refresh the policy table and dashboard.

### Algorithm C: Record a payment
1. Select a policy.
2. Enter date, amount, payment mode and transaction reference.
3. Validate the date and positive payment amount.
4. Insert the payment using a parameterised query.
5. Refresh the payment history and reports.

### Algorithm D: Generate a report
1. Select a report type.
2. Execute the corresponding SELECT query.
3. Use JOIN or aggregate functions where needed.
4. Display the result in a table.
5. Optionally export the visible report to CSV.

## 10. Testing

Perform the following tests in the running application and record the actual outcome.

| Test | Input/Action | Expected Result |
|---|---|---|
| 1 | Launch application | Dashboard opens and sample data appears |
| 2 | Add customer with valid details | Customer is saved |
| 3 | Leave required customer field blank | Validation warning appears |
| 4 | Enter an invalid date | Date validation warning appears |
| 5 | Add two policies with the same policy number | Duplicate is rejected |
| 6 | Enter a negative sum assured | Validation warning appears |
| 7 | Record a valid payment | Payment appears in history |
| 8 | Reuse a transaction reference | Duplicate transaction is rejected |
| 9 | Add a beneficiary | Beneficiary appears in the register |
| 10 | Open policy summary | Policy information is displayed |
| 11 | Export report | A CSV file is created |
| 12 | Close and reopen application | Saved records remain available |

**Important:** Run these tests yourself and fill in actual results before submitting. Do not claim a test was performed unless you have performed it.

## 11. Limitations

- SQLite is a local database and is intended for a single-computer school demonstration.
- The application does not connect to an actual insurer.
- Premium estimation uses a simplified educational formula and does not use actuarial tables, age-based underwriting, taxes or insurer-specific rates.
- Payment entries are records only; no money is transferred.
- The project does not verify identities or authenticate real policyholders.
- The program uses fictional sample data.

## 12. Future Scope

- Add administrator login and role-based access.
- Migrate the database to MySQL if required by the school.
- Add printable policy statements and PDF reports.
- Add automated renewal reminders.
- Add stronger privacy protections, backups and audit logs.
- Integrate with a legitimate insurer API in a real-world system, subject to authorisation.

## 13. Conclusion

LifeGuard demonstrates how Python and SQL can be combined to build a practical desktop application. Tkinter provides the graphical interface, Python manages validation and application logic, and SQLite stores records in related tables. The project applies CRUD operations, keys, joins, aggregate functions, exception handling and CSV export to a realistic information-management problem.

## 14. Bibliography

- Python documentation: https://docs.python.org/3/
- Tkinter documentation: https://docs.python.org/3/library/tkinter.html
- SQLite documentation: https://www.sqlite.org/docs.html
- Python `sqlite3` documentation: https://docs.python.org/3/library/sqlite3.html

---
**Submission reminder:** Add your own name, school details, teacher's requirements and screenshots of your actual running application. Confirm with your teacher whether SQLite is acceptable or whether MySQL is compulsory.
