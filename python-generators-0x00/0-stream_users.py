#!/usr/bin/python3
"""
0-stream_users.py
A generator function that streams rows from the user_data table in the ALX_prodev database.
"""

import mysql.connector
from mysql.connector import Error


def stream_users():
    """Generator that yields rows one by one from user_data table."""
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password_here',  # 🔁 Replace with your MySQL password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data;")

            # Use a single loop to yield rows one by one
            for row in cursor:
                yield row

            cursor.close()
            connection.close()

    except Error as e:
        print(f"Database error: {e}")
        return
