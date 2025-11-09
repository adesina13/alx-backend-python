#!/usr/bin/env python3
"""
0-databaseconnection.py
Custom class-based context manager for SQLite database connection
"""

import sqlite3


class DatabaseConnection:
    """Class-based context manager for SQLite database connections"""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the database connection"""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
        # Do not suppress exceptions
        return False


def main():
    db_name = "mydb.sqlite"

    # Ensure the table exists for demonstration
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
        """)
        # Optional: insert sample data if empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Alice", "alice@example.com"))
            cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Bob", "bob@example.com"))
            conn.commit()

    # Use the custom context manager
    with DatabaseConnection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print("Users in database:")
        for row in results:
            print(row)


if __name__ == "__main__":
    main()
