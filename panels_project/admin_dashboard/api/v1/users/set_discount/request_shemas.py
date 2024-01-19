from pydantic import BaseModel


class SetDiscountRequest(BaseModel):
    user_id: int
    discount: int
