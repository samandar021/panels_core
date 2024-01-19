from pydantic import BaseModel


class DeleteDiscountRequest(BaseModel):
    user_id: int
