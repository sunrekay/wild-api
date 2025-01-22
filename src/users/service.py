from typing import Optional

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.users import exceptions as users_exceptions
from src.users.models import User
from src.users.schemas import UserRegistrationIn


async def create_user(
    user_in: UserRegistrationIn,
    session: AsyncSession,
) -> User:
    try:
        user: User = User(**user_in.model_dump())
        session.add(user)
        await session.commit()
        return user
    except IntegrityError:
        await session.rollback()
        raise users_exceptions.user_already_exist


async def get_user_by_email(
    user_email: EmailStr | str,
    session: AsyncSession,
) -> Optional[User]:
    user = await session.scalar(
        select(User).where(
            User.email == user_email,
        )
    )
    return user
