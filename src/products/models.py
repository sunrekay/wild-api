from sqlalchemy import String, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped

from src.models import Base
from src.products.constants import (
    MAX_PRODUCT_NAME,
    MAX_PRODUCT_RATING,
    MIN_PRODUCT_RATING,
    MIN_PRODUCT_PRICE,
    MIN_PRODUCT_QUANTITY,
)


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    articul: Mapped[str] = mapped_column(nullable=False, unique=True)

    name: Mapped[str] = mapped_column(
        String(MAX_PRODUCT_NAME), nullable=False, unique=True
    )
    price: Mapped[int] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)

    is_tracking: Mapped[bool] = mapped_column(nullable=False, default=False)

    __table_args__ = (
        CheckConstraint(f"price > {MIN_PRODUCT_PRICE}", name="check_price_min"),
        CheckConstraint(f"rating >= {MIN_PRODUCT_RATING}", name="check_rating_min"),
        CheckConstraint(f"rating <= {MAX_PRODUCT_RATING}", name="check_rating_max"),
        CheckConstraint(
            f"quantity >= {MIN_PRODUCT_QUANTITY}", name="check_quantity_min"
        ),
    )
