from typing import List

from fastapi import APIRouter

from .request_shemas import DeleteDiscountRequest

router = APIRouter()


@router.post("/")
async def delete_discount(request_data: List[DeleteDiscountRequest]):
    fixed_response = {
        "status": "ok",
        "message": "Password setted"
    }
    return fixed_response
