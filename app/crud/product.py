from sqlalchemy.orm import Session
from app.models.models import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.db.redis import redis_client
import json

CACHE_EXPIRE = 3600  # 1 hora

def get_product(db: Session, product_id: int):
    # Tentar buscar no cache primeiro
    cached_product = redis_client.get(f"product:{product_id}")
    if cached_product:
        return json.loads(cached_product)
    
    # Se não estiver no cache, buscar no banco
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        # Salvar no cache para futuras consultas
        product_data = {
            "id": db_product.id,
            "name": db_product.name,
            "description": db_product.description,
            "price": db_product.price,
            "stock": db_product.stock,
            "is_active": db_product.is_active,
            "category_id": db_product.category_id,
            "created_at": db_product.created_at.isoformat() if db_product.created_at else None
        }
        redis_client.setex(f"product:{product_id}", CACHE_EXPIRE, json.dumps(product_data))
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        update_data = product.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        # Invalidar cache após atualização
        redis_client.delete(f"product:{product_id}")
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        # Remover do cache após exclusão
        redis_client.delete(f"product:{product_id}")
    return db_product
