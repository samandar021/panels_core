from pydantic import BaseModel


class DeleteCustomRateRequest(BaseModel):
    user_id: int
