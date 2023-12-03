from __future__ import annotations
from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    name: str
    age: int
    location: str
    preferences: str
    purchases: list[Purchase]

    class Config:
        orm_mode = True


class Product(BaseModel):
    product_id: int
    product_name: str
    category: int
    description: str
    tags: str

    class Config:
        orm_mode = True


class Purchase(BaseModel):
    purchase_id: int
    user_id: int
    product_id: int
    user = User
    product = Product

    class Config:
        orm_mode = True
