# sql_login_demo.py
import sqlite3
import re

def setup_database():
    """Create an in-memory database and populate it with demo users."""
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE accounts (user TEXT PRIMARY KEY, pwd TEXT)")
    cursor.executemany("INSERT INTO accounts VALUES (?, ?)", [
        ("emma", "pass123"), 
        ("liam", "letmein")
    ])
    connection.commit()
    return connection

def unsafe_auth(db, user, pwd):
    """Vulnerable SQL login (prone to injection)."""
    query = f"SELECT * FROM accounts WHERE user='{user}' AND pwd='{pwd}'"
    return db.execute(query).fetchone() is not None

def safe_auth(db, user, pwd):
    """Secure login using parameterized queries."""
    query = "SELECT * FROM accounts WHERE user=? AND pwd=?"
    return db.execute(query, (user, pwd)).fetchone() is not None

INPUT_PATTERN = re.compile(r'^[a-zA-Z0-9_]{1,32}$')

def validate_input(text: str) -> str:
    """Allow only alphanumeric and underscore inputs up to 32 chars."""
    if not INPUT_PATTERN.fullmatch(text):
        raise ValueError(f"Illegal input: {text}")
    return text

if __name__ == "__main__":
    db_conn = setup_database()
    
    print("Unsafe login with correct creds:", unsafe_auth(db_conn, "emma", "pass123"))
    
    malicious_payload = "' OR 'x'='x"
    print("Unsafe login with injection:", unsafe_auth(db_conn, "emma", malicious_payload))
    print("Safe login with injection:", safe_auth(db_conn, "emma", malicious_payload))
    
    try:
        validate_input("liam; DROP TABLE accounts")
    except ValueError as err:
        print("Validation error:", err)
