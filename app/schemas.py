from __future__ import annotations
from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    name: str
    age: int
    location: str
    preferences: str

    class Config:
        from_attributes = True


class Product(BaseModel):
    product_id: int
    product_name: str
    category: str
    description: str
    tags: str

    class Config:
        from_attributes = True


class Purchase(BaseModel):
    user_id: int
    product_id: int
    user: User

    class Config:
        from_attributes = True
