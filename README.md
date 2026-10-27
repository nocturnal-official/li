# LifeGuard — Class XII CBSE Computer Science Project

## What's included
- `main.py` — complete desktop GUI application (Python + Tkinter + SQL)
- `schema.sql` — SQL table definitions
- `PROJECT_REPORT.md` — ready-to-edit project documentation
- `VIVA_QUESTIONS.md` — viva preparation
- `requirements.txt` — no third-party packages required

## Quick start (Windows)
1. Download and extract this ZIP file to a normal folder.
2. Install Python 3 from https://www.python.org/downloads/ if it is not already installed.
   During installation, tick **Add Python to PATH**.
3. Open the extracted folder.
4. Double-click `main.py`, or open Command Prompt in this folder and run:
   `python main.py`
5. The application creates `lifeguard.db` automatically on first launch and inserts fictional sample records.
6. Use the tabs to manage customers, policies, payments and beneficiaries.

## Requirements
- Python 3.9 or newer recommended
- Tkinter (included with standard Python on most Windows installations)
- SQLite (included with Python's `sqlite3` module)
- Internet is not required
- No `pip install` is required

## Important database note
This project uses SQLite, a relational SQL database built into Python, so it can run directly after extraction without installing or configuring a separate database server. If your teacher specifically requires MySQL and `mysql.connector`, this version should be adapted to that requirement before submission.

## Demo data
The app adds fictional sample customers, policies, beneficiaries and payments only when the database is first created. You can safely experiment with the sample records. Keep a backup of `lifeguard.db` if you need to preserve your final demo data.

## Reset the sample database
Close the application, then delete `lifeguard.db`. Start `main.py` again to recreate the database and sample records. This permanently removes the records stored in that local database.

## Troubleshooting
- **Python is not recognised:** reinstall Python and tick "Add Python to PATH", or use the Python launcher: `py main.py`.
- **No module named tkinter:** repair/reinstall Python with Tcl/Tk support enabled.
- **App does not open when double-clicked:** run `python main.py` in Command Prompt so that any error message is visible.
- **Database error:** close the app and make sure the folder is writable.

## Academic integrity / demonstration
Use fictional data only. Review and personalise the project report and be prepared to explain each function. The premium estimator is a simplified classroom illustration, not an actual insurance pricing model or financial recommendation.
