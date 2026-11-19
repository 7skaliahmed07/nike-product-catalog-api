
from sqlalchemy.orm import Session

from app.models import Product
from app.schemas import ProductCreate


def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.model_dump())

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def get_product(db: Session, product_id):
    return db.query(Product).filter(
        Product.id == product_id
    ).first()


def get_products(
    db: Session,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    page: int = 1,
    limit: int = 20
):
    query = db.query(Product)

    if category:
        query = query.filter(Product.category == category)

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    total = query.count()

    products = (
        query
        .order_by(Product.id)
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "products": products
    }



def update_product(db: Session, product_id, product):
    db_product = get_product(db, product_id)

    if not db_product:
        return None

    updated_data = product.model_dump()

    for key, value in updated_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)

    return db_product


def delete_product(db: Session, product_id):
    db_product = get_product(db, product_id)

    if not db_product:
        return False

    db.delete(db_product)
    db.commit()

    return True



def patch_product(db: Session, product_id, product):
    db_product = get_product(db, product_id)

    if not db_product:
        return None

    updated_data = product.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)

    return db_product
