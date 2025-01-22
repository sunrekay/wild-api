from fastapi import HTTPException, status


class ProductAlreadyExists(HTTPException):

    detail = "product already exist"
    status_code = status.HTTP_403_FORBIDDEN

    def __init__(self):
        super().__init__(
            detail=self.detail,
            status_code=self.status_code,
        )


class ProductNotFound(HTTPException):

    detail = "product not found"
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self):
        super().__init__(
            detail=self.detail,
            status_code=self.status_code,
        )
