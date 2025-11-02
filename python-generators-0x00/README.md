# Python Generators — Task 0: Getting Started with Python Generators

## Objective
Create a generator that streams rows from an SQL database one by one.  
This task sets up the `ALX_prodev` database, creates the `user_data` table, and seeds it with CSV data.

---

## Files
- **`seed.py`** – Handles database setup and data seeding.
- **`0-main.py`** – Test script provided for validation.
- **`user_data.csv`** – Contains sample user records.

---

## Database Schema
| Field | Type | Description |
|--------|------|-------------|
| `user_id` | UUID (Primary Key) | Unique identifier for each user |
| `name` | VARCHAR | User’s full name |
| `email` | VARCHAR | User’s email address |
| `age` | DECIMAL | User’s age |

---

## Functions

| Function | Description |
|-----------|-------------|
| `connect_db()` | Connects to the MySQL server |
| `create_database(connection)` | Creates the `ALX_prodev` database |
| `connect_to_prodev()` | Connects to the `ALX_prodev` database |
| `create_table(connection)` | Creates `user_data` table if not exists |
| `insert_data(connection, csv_file)` | Inserts data from CSV into the table |

---

## Example Output
```bash
connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ...]
