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


@app.post("/users/", response_model=schemas.User, tags=["users"])
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user.user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User ID already in use")
    return crud.create_user(db=db, user=user)


@app.post("/products/", response_model=schemas.Product, tags=["products"])
def create_product(product: schemas.Product, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product.product_id)
    if db_product:
        raise HTTPException(status_code=400, detail="Product ID already in use")
    return crud.create_product(db=db, product=product)


@app.get("/users/", response_model=list[schemas.User], tags=["users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/products/", response_model=list[schemas.Product], tags=["products"])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


@app.get("/users/{user_id}", response_model=schemas.User, tags=["users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/products/{product_id}", response_model=schemas.Product, tags=["products"])
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.post("/purchases/", response_model=schemas.Purchase, tags=["purchases"])
def create_purchase(user_id: int, product_id: int, db: Session = Depends(get_db)):
    if not (db_user := crud.get_user(db, user_id=user_id)):
        raise HTTPException(status_code=404, detail="User ID not found")
    if not (db_product := crud.get_product(db, product_id=product_id)):
        raise HTTPException(status_code=404, detail="Product ID not found")

    purchase = schemas.Purchase(
        user_id=user_id,
        product_id=product_id,
        user=db_user,
    )
    return crud.create_purchase(db=db, purchase=purchase)


@app.get("/purchases/", response_model=list[schemas.Purchase], tags=["purchases"])
def read_purchases(skip: int = 0, db: Session = Depends(get_db)):
    purchases = crud.get_purchases(db, skip=skip)
    return purchases


@app.get(
    "/purchases/{purchase_id}", response_model=schemas.Purchase, tags=["purchases"]
)
def read_purchase(purchase_id: int, db: Session = Depends(get_db)):
    db_purchase = crud.get_purchase(db, purchase_id=purchase_id)
    if db_purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return db_purchase


@app.get(
    "/users/{user_id}/purchases/",
    response_model=list[schemas.Purchase],
    tags=["users"],
)
def read_purchases_by_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_purchases_by_user(db, user_id=user_id)


@app.get(
    "/products/{product_id}/purchases/",
    response_model=list[schemas.Purchase],
    tags=["products"],
)
def read_purchases_by_product(product_id: int, db: Session = Depends(get_db)):
    return crud.get_purchases_by_product(db, product_id=product_id)


@app.get(
    "/recommendations/{user_id}",
    response_model=list[schemas.Product],
    tags=["recommendations"],
)
def recommend_products_by_user_id(user_id: int, db: Session = Depends(get_db)):
    return crud.recommend_products_by_user(db, user_id=user_id)
