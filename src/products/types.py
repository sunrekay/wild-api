from typing import Annotated

from annotated_types import MinLen, MaxLen

from src.products.constants import MIN_PRODUCT_ARTICUL, MAX_PRODUCT_ARTICUL

ArticulStr = Annotated[
    str,
    MinLen(MIN_PRODUCT_ARTICUL),
    MaxLen(MAX_PRODUCT_ARTICUL),
]
