
from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Product

from app.schemas import (
    ProductCreate,
    ProductUpdate,
    ProductPatch,
    ProductResponse,
    ProductListResponse
)
from app import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nike Product Catalog API")


@app.get("/")
def home():
    return {"message": "Nike Product Catalog API is running"}


@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    return crud.create_product(db, product)


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: UUID,
    db: Session = Depends(get_db)
):
    product = crud.get_product(db, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product



@app.get("/products", response_model=ProductListResponse)
def list_products(
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="Page must be greater than or equal to 1"
        )

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 100"
        )

    if min_price is not None and min_price < 0:
        raise HTTPException(
            status_code=400,
            detail="Minimum price cannot be negative"
        )

    if max_price is not None and max_price < 0:
        raise HTTPException(
            status_code=400,
            detail="Maximum price cannot be negative"
        )

    if (
        min_price is not None
        and max_price is not None
        and min_price > max_price
    ):
        raise HTTPException(
            status_code=400,
            detail="Minimum price cannot exceed maximum price"
        )

    return crud.get_products(
        db=db,
        category=category,
        min_price=min_price,
        max_price=max_price,
        page=page,
        limit=limit
    )




@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: UUID,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    updated_product = crud.update_product(
        db,
        product_id,
        product
    )

    if not updated_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return updated_product


@app.patch("/products/{product_id}", response_model=ProductResponse)
def patch_product(
    product_id: UUID,
    product: ProductPatch,
    db: Session = Depends(get_db)
):
    updated_data = product.model_dump(exclude_unset=True)

    if not updated_data:
        raise HTTPException(
            status_code=400,
            detail="At least one field must be provided for update"
        )

    updated_product = crud.patch_product(
        db,
        product_id,
        product
    )

    if not updated_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return updated_product

@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_product(
    product_id: UUID,
    db: Session = Depends(get_db)
):
    deleted = crud.delete_product(db, product_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


