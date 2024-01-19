from pydantic import BaseModel


class SetPasswordRequest(BaseModel):
    user_id: int
    password: str
