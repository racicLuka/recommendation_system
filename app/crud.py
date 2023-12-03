from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.User):
    db_user = models.User(
        user_id=user.user_id,
        name=user.name,
        age=user.age,
        location=user.location,
        preferences=user.preferences,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_product(db: Session, product_id: int):
    return (
        db.query(models.Product).filter(models.Product.product_id == product_id).first()
    )


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.Product):
    db_product = models.Product(
        product_id=product.product_id,
        product_name=product.product_name,
        category=product.category,
        description=product.description,
        tags=product.tags,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def create_purchase(db: Session, purchase: schemas.Purchase):
    user = get_user(db, purchase.user_id)
    db_purchase = models.Purchase(
        user_id=purchase.user_id,
        product_id=purchase.product_id,
        user=user,
    )
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase


def get_purchases(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Purchase).offset(skip).limit(limit).all()


def get_purchase(db: Session, purchase_id: int):
    return db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()


def get_purchases_by_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User ID not found")
    return user.purchases


def get_purchases_by_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product ID not found")
    return (
        db.query(models.Purchase).filter(models.Purchase.product_id == product_id).all()
    )
