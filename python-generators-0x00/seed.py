#!/usr/bin/python3
"""
seed.py
Sets up the ALX_prodev MySQL database and populates it with data from user_data.csv.
"""

import mysql.connector
from mysql.connector import Error
import csv
import uuid


def connect_db():
    """Connects to the MySQL server (without specifying a database)."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password_here'  # 🔁 Replace with your MySQL root password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    return None


def create_database(connection):
    """Creates the database ALX_prodev if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created or already exists.")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password_here',  # 🔁 Replace again here
            database='ALX_prodev'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
    return None


def create_table(connection):
    """Creates the user_data table if it does not exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(10,2) NOT NULL,
        INDEX (user_id)
    );
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """Inserts data into the user_data table from a CSV file if it doesn’t already exist."""
    try:
        cursor = connection.cursor()

        with open(csv_file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            inserted_count = 0
            for row in csv_reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']

                # Check if email already exists
                cursor.execute("SELECT email FROM user_data WHERE email = %s;", (email,))
                existing = cursor.fetchone()

                if not existing:
                    insert_query = """
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s);
                    """
                    cursor.execute(insert_query, (user_id, name, email, age))
                    inserted_count += 1

            connection.commit()
            print(f"{inserted_count} records inserted successfully.")
        cursor.close()

    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
    except Error as e:
        print(f"Error inserting data: {e}")
