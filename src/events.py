import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import Product
from src.database import database
from src.products import crud
from src.products import service


async def check_products_job(session: AsyncSession):
    products = await session.scalars(
        select(Product).where(
            Product.is_tracking == True,
        )
    )

    for product in products:
        schemas_product = await service.get_product_data(
            articul=product.articul,
        )
        await crud.update_product(
            product=product,
            session=session,
            **schemas_product.model_dump(),
        )


def check_products():
    scheduler = AsyncIOScheduler()
    session: AsyncSession = database.get_scoped_session()
    scheduler.add_job(
        lambda: asyncio.create_task(
            check_products_job(
                session=session,
            )
        ),
        "cron",
        minute=30,
    )
    scheduler.start()


if __name__ == "__main__":
    check_products()
