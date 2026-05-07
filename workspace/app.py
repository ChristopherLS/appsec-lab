"""
AppSec Lab — workspace/app.py
==============================
This is your working file for all labs.
Use GitHub Copilot to generate each route/function as instructed
in the challenge cards, then identify and fix the vulnerabilities.
"""

import sqlite3
from flask import Flask, g, request
import bcrypt

app = Flask(__name__)
app.config["DATABASE"] = ":memory:"
app.config["SECRET_KEY"] = "change-me-in-production"
app.config["TESTING"] = False

# ── Database helpers ────────────────────────────────────────────────────────
_db_connection: sqlite3.Connection | None = None


def get_db() -> sqlite3.Connection:
    """Return the shared database connection, creating it once if needed."""
    global _db_connection
    if _db_connection is None:
        _db_connection = sqlite3.connect(
            app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
            check_same_thread=False,   # allow access from test threads
        )
        _db_connection.row_factory = sqlite3.Row
    return _db_connection
 
 
def init_db() -> None:
    """Create tables if they don't exist."""
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS invoices (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id  TEXT NOT NULL,
            amount   REAL NOT NULL,
            details  TEXT
        );
    """)
    db.execute(
        "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
        ("testuser", "testpassword")
    )
    db.commit()


# ── Lab 01: SQL Injection ────────────────────────────────────────────────────
# Ask Copilot: "Write a Flask POST /login route that checks a username
#               and password against a SQLite database called users.db"
# Paste Copilot's code below this comment, then find and fix the vulnerability.

# Fixed Code 
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    db = get_db()

    user = db.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()
 
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return "Login successful"
    else:
        return "Invalid credentials", 401
 
# ── Lab 02: Cross-Site Scripting (XSS) ──────────────────────────────────────
# Ask Copilot: "Write a Flask GET /search route that displays search results
#               for a query parameter q in an HTML response"
# Paste Copilot's code below this comment, then find and fix the vulnerability.




# ── Lab 03: Broken Authentication ────────────────────────────────────────────
# Ask Copilot: "Write a register_user(username, password) function that hashes
#               the password and stores the user in the SQLite database"
# Paste Copilot's code below this comment, then find and fix the vulnerability.

# YOUR CODE HERE


# ── Lab 04: IDOR ─────────────────────────────────────────────────────────────
# Ask Copilot: "Write a Flask GET /invoice/<invoice_id> route that returns
#               the invoice as JSON for the logged-in user"
# Paste Copilot's code below this comment, then find and fix the vulnerability.

# YOUR CODE HERE


# ── Lab 05: Sensitive Data Exposure ──────────────────────────────────────────
# Ask Copilot: "Write a Python module that connects to AWS S3 and
#               a Stripe payment API using configuration variables"
# Paste Copilot's code below this comment, then find and fix the vulnerability.

# YOUR CODE HERE


# ── Lab 06: Command Injection ────────────────────────────────────────────────
# Ask Copilot: "Write a Flask POST /ping route that pings a hostname
#               submitted by the user and returns the output"
# Paste Copilot's code below this comment, then find and fix the vulnerability.

# YOUR CODE HERE


# ── Lab 07: XXE Injection ────────────────────────────────────────────────────
# Ask Copilot: "Write a Flask POST /upload route that accepts an XML file
#               upload and returns the parsed content as JSON"
# Paste Copilot's code below this comment, then find and fix the vulnerability.

# YOUR CODE HERE

init_db()
 
if __name__ == "__main__":
    app.run(debug=False)