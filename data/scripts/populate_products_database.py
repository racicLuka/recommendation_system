import sqlite3
from extract_users_and_products import extract_unique_product_ids

products_conn = sqlite3.connect("../database.sqlite")
products_cursor = products_conn.cursor()

unique_products = extract_unique_product_ids("../dataset - dataset.csv")
products_cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        category TEXT,
        product_name TEXT,
        description TEXT,
        tags TEXT
    )
"""
)


def populate_products_database(products_csv, products_cursor):
    for product_id, product in products_csv.items():
        category = product.category
        name = product.name
        description = product.description
        tags = product.tags
        products_cursor.execute(
            """
            INSERT INTO products (product_id, category, product_name, description, tags) VALUES (?, ?, ?, ?, ?)
            """,
            (product_id, category, name, description, tags),
        )


populate_products_database(unique_products, products_cursor)
products_conn.commit()
products_conn.close()
