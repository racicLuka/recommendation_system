import csv
import sqlite3

conn = sqlite3.connect("../database.sqlite")
cursor = conn.cursor()


cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER
    )
"""
)


def populate_purchases_database(csv_file, cursor):
    with open(csv_file, "r") as dataset:
        csv_reader = csv.DictReader(dataset)
        for row in csv_reader:
            user_id = row["user_id"]
            product_id = row["product_id"]
            cursor.execute(
                """
                INSERT INTO purchases (user_id, product_id) VALUES (?, ?)
                """,
                (user_id, product_id),
            )


populate_purchases_database("../dataset - dataset.csv", cursor)
conn.commit()
conn.close()
