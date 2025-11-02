#!/usr/bin/python3
"""
4-stream_ages.py
Compute a memory-efficient average user age using generators.
"""

import seed


def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.
    Fetches data lazily to avoid loading all users at once.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:
        yield row['age']

    connection.close()


def compute_average_age():
    """
    Uses the stream_user_ages generator to compute the average age
    without loading all rows into memory.
    Must use no more than 2 loops.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    average_age = total_age / count if count > 0 else 0
    print(f"Average age of users: {average_age:.2f}")


if __name__ == "__main__":
    compute_average_age()
