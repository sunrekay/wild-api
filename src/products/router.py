from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import dependencies as auth_dependencies
from src.database import database
from src.products import crud
from src.products import schemas
from src.products import service
from src.products.types import ArticulStr

router = APIRouter(dependencies=[Depends(auth_dependencies.validate_refresh_token)])


@router.get(
    path="/products",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ProductOut,
)
async def get_product(
    artikul: ArticulStr,
    session: AsyncSession = Depends(database.session_dependency),
):
    return await crud.get_product(
        artikul=artikul,
        session=session,
    )


@router.post(
    path="/products",
    response_model=schemas.ProductOut,
    status_code=status.HTTP_200_OK,
)
async def products(
    product_in: schemas.ProductIn,
    session: AsyncSession = Depends(database.session_dependency),
):
    return await service.products(
        articul=product_in.artikul,
        session=session,
    )


@router.get(
    path="/subscribe",
    response_model=schemas.ProductOut,
    status_code=status.HTTP_202_ACCEPTED,
)
async def subscribe(
    articul: ArticulStr,
    session: AsyncSession = Depends(database.session_dependency),
):
    return await service.subscribe(
        articul=articul,
        session=session,
    )
