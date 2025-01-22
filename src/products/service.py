import httpx
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from src import Product
from src.products import crud
from src.products import schemas
from src.products.constants import WB_CARD_URL
from src.products.exceptions import ProductNotFound
from src.products.types import ArticulStr


async def get_product_data(articul: ArticulStr) -> schemas.Product:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            WB_CARD_URL.format(articul=articul),
        )
        if response.status_code != status.HTTP_200_OK:
            raise ProductNotFound()
        item = response.json()["data"]["products"][0]

    return schemas.Product(
        articul=articul,
        name=item["name"],
        price=item["salePriceU"],
        rating=item["supplierRating"],
        quantity=item["totalQuantity"],
    )


async def products(
    articul: ArticulStr,
    session: AsyncSession,
) -> Product:
    schemas_product = await get_product_data(articul=articul)
    return await crud.create_product(
        schemas_product=schemas_product,
        session=session,
    )


async def subscribe(
    articul: ArticulStr,
    session: AsyncSession,
) -> Product:
    product: Product = await crud.get_product(
        artikul=articul,
        session=session,
    )

    if product:
        product = await crud.update_product(
            product=product,
            session=session,
            **{"is_tracking": True},
        )

    else:
        schemas_product = await get_product_data(articul=articul)
        product = await crud.create_product(
            schemas_product=schemas_product,
            session=session,
        )

    return product
