import sqlite3
from database.extract_users_and_products import extract_unique_user_ids

users_conn = sqlite3.connect("users.sqlite")
users_cursor = users_conn.cursor()

unique_users = extract_unique_user_ids("dataset - dataset.csv")
users_cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        location TEXT,
        preferences TEXT
    )
"""
)


def populate_users_database(users, users_cursor):
    for user_id, user in users.items():
        name = user.name
        age = user.age
        location = user.location
        preferences = user.preferences
        users_cursor.execute(
            """
            INSERT INTO users (user_id, name, age, location, preferences) VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, name, age, location, preferences),
        )


populate_users_database(unique_users, users_cursor)
users_conn.commit()
users_conn.close()
