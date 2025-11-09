#!/usr/bin/env python3
"""
1-execute.py
Reusable class-based context manager to execute queries
"""

import sqlite3


class ExecuteQuery:
    """Context manager that executes a given query with parameters"""

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.results = None

    def __enter__(self):
        """Open connection and execute query"""
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results  # Return results directly

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the connection"""
        if self.conn:
            self.conn.close()
        # Do not suppress exceptions
        return False


def main():
    db_name = "mydb.sqlite"

    # Ensure the table exists with sample data for demonstration
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL
        )
        """)
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            users = [
                ("Alice", 30, "alice@example.com"),
                ("Bob", 20, "bob@example.com"),
                ("Charlie", 40, "charlie@example.com")
            ]
            cursor.executemany("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", users)
            conn.commit()

    # Use the ExecuteQuery context manager
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery(db_name, query, params) as results:
        print(f"Users older than {params[0]}:")
        for row in results:
            print(row)


if __name__ == "__main__":
    main()
