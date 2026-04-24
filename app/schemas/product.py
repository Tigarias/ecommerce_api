from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0, description="O preço deve ser maior que zero")
    stock: int = Field(ge=0, description="O estoque não pode ser negativo")
    is_active: Optional[bool] = True
    category_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Smartphone XYZ",
                "description": "Um smartphone de última geração",
                "price": 2500.00,
                "stock": 50,
                "is_active": True,
                "category_id": 1,
                "created_at": "2024-03-24T12:00:00"
            }
        }
