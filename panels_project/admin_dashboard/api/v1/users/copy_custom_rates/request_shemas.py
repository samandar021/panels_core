from typing import List

from pydantic import BaseModel


class CopyCustomRatesRequest(BaseModel):
    from_user_id: int
    to_users_id: List[int]
