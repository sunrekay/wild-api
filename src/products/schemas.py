from pydantic import BaseModel

from src.products.types import ArticulStr


class Product(BaseModel):
    articul: ArticulStr
    name: str
    price: float
    rating: float
    quantity: int
    is_tracking: bool = False


class ProductIn(BaseModel):
    artikul: ArticulStr


class ProductOut(Product):
    pass
