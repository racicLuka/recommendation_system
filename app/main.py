from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user.user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User ID already in use")
    return crud.create_user(db=db, user=user)


@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.Product, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product.product_id)
    if db_product:
        raise HTTPException(status_code=400, detail="Product ID already in use")
    return crud.create_product(db=db, product=product)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/products/{product_id}", response_model=schemas.User)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.post("/purchases/", response_model=schemas.Purchase)
def create_purchase(user_id: int, product_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    product = crud.get_product(db, product_id=product_id)
    purchase = schemas.Purchase(
        user_id=user_id, product_id=product_id, user=user, product=product
    )
    return crud.create_purchase(db=db, purchase=purchase)


@app.get("/purchases/", response_model=list[schemas.Purchase])
def read_purchases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    purchases = crud.get_purchases(db, skip=skip, limit=limit)
    return purchases


@app.get("/purchases/{purchase_id}", response_model=schemas.Purchase)
def read_purchase(purchase_id: int, db: Session = Depends(get_db)):
    db_purchase = crud.get_purchase(db, purchase_id=purchase_id)
    if db_purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return db_purchase
