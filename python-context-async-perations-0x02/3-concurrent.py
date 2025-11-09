#!/usr/bin/env python3
"""
3-concurrent.py
Run multiple asynchronous database queries concurrently using aiosqlite
"""

import asyncio
import aiosqlite

DB_NAME = "mydb.sqlite"


async def async_fetch_users():
    """Fetch all users asynchronously"""
    async with aiosqlite.connect(DB_NAME) as conn:
        async with conn.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows


async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously"""
    async with aiosqlite.connect(DB_NAME) as conn:
        async with conn.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            rows = await cursor.fetchall()
            return rows


async def fetch_concurrently():
    """Run multiple async queries concurrently"""
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    all_users, older_users = results

    print("All users:")
    for user in all_users:
        print(user)

    print("\nUsers older than 40:")
    for user in older_users:
        print(user)


def main():
    # Ensure the table exists with sample data
    import sqlite3
    with sqlite3.connect(DB_NAME) as conn:
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
                ("Bob", 45, "bob@example.com"),
                ("Charlie", 50, "charlie@example.com"),
                ("Diana", 25, "diana@example.com")
            ]
            cursor.executemany("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", users)
            conn.commit()

    # Run concurrent async queries
    asyncio.run(fetch_concurrently())


if __name__ == "__main__":
    main()
