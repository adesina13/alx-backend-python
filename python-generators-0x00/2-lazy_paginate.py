#!/usr/bin/python3
"""
2-lazy_paginate.py
Simulates fetching paginated user data lazily using generators.
"""

import seed


def paginate_users(page_size, offset):
    """
    Fetch a page of users from the database with the given page_size and offset.
    Returns a list of rows (each as a dictionary).
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily loads paginated user data.
    Fetches the next page only when needed.
    Must use only one loop.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
