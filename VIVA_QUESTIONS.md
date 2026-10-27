# LifeGuard — Viva Voce Questions and Answers

## Project overview

**1. What is the aim of your project?**  
To develop a desktop application that manages fictional life insurance policyholders, policies, beneficiaries and premium payment records using Python and SQL.

**2. Which technologies are used?**  
Python, Tkinter for the GUI, SQLite as the SQL database, and CSV export using Python's built-in `csv` module.

**3. Why did you choose this topic?**  
Insurance systems manage related records and need searching, updating and reporting. It is a practical way to demonstrate GUI programming and database concepts.

**4. What is a GUI?**  
A Graphical User Interface lets a user interact with software through visual elements such as windows, buttons, labels, forms and tables.

**5. What is Tkinter?**  
Tkinter is Python's standard interface to the Tk GUI toolkit. It is used to build desktop windows and controls.

## Python concepts

**6. What is a function?**  
A named, reusable block of code that performs a task.

**7. Why are functions used in this project?**  
They separate tasks such as adding customers, recording payments, refreshing tables and generating reports, making the program easier to maintain.

**8. What is exception handling?**  
It uses constructs such as `try` and `except` to handle errors without abruptly terminating normal program flow.

**9. What is input validation?**  
Checking user input before processing or saving it, such as verifying required fields, dates and positive amounts.

**10. What is a module?**  
A Python file or library that provides reusable code. This project imports modules including `tkinter`, `sqlite3`, `csv` and `datetime`.

## SQL and database concepts

**11. What is SQL?**  
Structured Query Language, used to define, retrieve and manipulate data in relational databases.

**12. What is a primary key?**  
A field or combination of fields that uniquely identifies each record in a table.

**13. What is a foreign key?**  
A field that refers to a key in another table and helps maintain referential integrity.

**14. What is a relational database?**  
A database that organises data in tables and links related records through keys.

**15. What is CRUD?**  
Create, Read, Update and Delete—the four common operations for managing records.

**16. Which SQL command adds a record?**  
`INSERT`.

**17. Which SQL command retrieves records?**  
`SELECT`.

**18. Which SQL command modifies existing records?**  
`UPDATE`.

**19. Which SQL command removes records?**  
`DELETE`.

**20. Why is `JOIN` used?**  
To combine related rows from two or more tables, for example showing a policy alongside its policyholder's name.

**21. Why are `COUNT()` and `SUM()` used?**  
`COUNT()` counts records, while `SUM()` calculates a total of numeric values.

**22. What is `GROUP BY` used for?**  
It groups rows that share a value so aggregate functions can calculate results for each group.

**23. What is a parameterised query?**  
A query where values are supplied separately from the SQL command. It helps prevent SQL injection and handles values more safely.

**24. Why are foreign keys enabled?**  
They prevent invalid relationships, such as a policy referencing a customer who does not exist.

**25. Why is the policy number unique?**  
It prevents two policy records from accidentally using the same policy number.

## Project-specific questions

**26. Why did you use SQLite instead of MySQL?**  
SQLite is included with Python and requires no separate server setup, making this version easy to run. If the school's project instructions require MySQL specifically, the database layer must be adapted.

**27. Where is the data stored?**  
In the `lifeguard.db` file created beside `main.py`.

**28. Does the data remain after the program closes?**  
Yes. Records are saved in the database file and can be retrieved when the application is opened again.

**29. Is the premium estimator an actual insurance quote?**  
No. It uses a simplified classroom formula to demonstrate calculations. Actual insurance premiums depend on insurer-specific rules and other factors.

**30. Does recording a payment transfer money?**  
No. It stores a payment record for demonstration and does not connect to a bank or payment gateway.

**31. What is the purpose of CSV export?**  
It allows report data to be opened in spreadsheet software such as Excel.

**32. What improvements could be made?**  
MySQL support, login and permissions, PDF reports, renewal reminders, stronger security and authorised integration with an insurer's system.

**Viva tip:** Practise explaining the code in your own words and demonstrate one successful insert, one validation warning, a report and CSV export.
