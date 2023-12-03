import csv
from typing import Mapping
from dataclasses import dataclass


@dataclass
class User:
    name: str
    age: int
    location: str
    preferences: str


@dataclass
class Product:
    name: str
    category: int
    description: str
    tags: str


def extract_unique_user_ids(csv_file):
    uniques_users: Mapping[str, User] = {}

    with open(csv_file, "r") as dataset:
        csv_reader = csv.DictReader(dataset)
        for row in csv_reader:
            user_id = row["user_id"]
            name = row["name"]
            age = row["age"]
            location = row["location"]
            preferences = row["preferences"]

            uniques_users.setdefault(user_id, User(name, age, location, preferences))

    return uniques_users


def extract_unique_product_ids(csv_file):
    unique_products: Mapping[str, Product] = {}

    with open(csv_file, "r") as dataset:
        csv_reader = csv.DictReader(dataset)
        for row in csv_reader:
            product_id = row["product_id"]
            name = row["product_name"]
            category = row["category"]
            description = row["description"]
            tags = row["tags"]

            unique_products.setdefault(
                product_id, Product(name, category, description, tags)
            )

    return unique_products
