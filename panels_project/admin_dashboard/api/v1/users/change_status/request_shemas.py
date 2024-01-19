from pydantic import BaseModel


class UpdateChangeStatusRequest(BaseModel):
    user_id: int
    status: int
