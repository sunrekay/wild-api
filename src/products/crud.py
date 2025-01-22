from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src import Product
from src.products import schemas
from src.products.exceptions import ProductAlreadyExists
from src.products.types import ArticulStr


async def get_product(
    artikul: ArticulStr,
    session: AsyncSession,
) -> Product:
    product = await session.scalar(
        select(Product).where(
            Product.articul == artikul,
        )
    )
    return product


async def update_product(
    product: Product,
    session: AsyncSession,
    **kwargs,
) -> Product:
    for k, v in kwargs.items():
        setattr(product, k, v)
    await session.commit()
    return product


async def create_product(
    schemas_product: schemas.Product,
    session: AsyncSession,
) -> Product:
    try:
        product: Product = Product(**schemas_product.model_dump())

        session.add(product)
        await session.commit()

        return product

    except IntegrityError:
        await session.rollback()
        raise ProductAlreadyExists()
