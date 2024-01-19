from pydantic import BaseModel


class TwoFARequest(BaseModel):
    code: str
    csrf: str
