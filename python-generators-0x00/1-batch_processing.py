#!/usr/bin/python3
"""
1-batch_processing.py
Fetch and process data in batches from the ALX_prodev.user_data table using Python generators.
"""

import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of users from the user_data table.
    Each batch contains at most `batch_size` rows.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password_here',  # 🔁 Replace with your MySQL password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data;")

            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch

            cursor.close()
            connection.close()

    except Error as e:
        print(f"Database error: {e}")
        return


def batch_processing(batch_size):
    """
    Processes each batch of users fetched by stream_users_in_batches().
    Filters users with age > 25 and yields them one by one.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if float(user['age']) > 25:
                print(user)
                yield user
