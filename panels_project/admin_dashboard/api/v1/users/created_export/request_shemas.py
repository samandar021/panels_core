from datetime import date
from typing import List

from pydantic import BaseModel


class CreatedExportRequest(BaseModel):
    from_date: date
    to_date: date
    statuses: List[int]
    format: str
    columns: List[str]
