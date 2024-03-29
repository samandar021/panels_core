from typing import List

from pydantic import BaseModel


class UpdateColumnsRequest(BaseModel):
    columns: List[str]
