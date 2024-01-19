import re

from pydantic import BaseModel, EmailStr, field_validator


class AdminCreate(BaseModel):
    panel_id: int
    password: str
    email: EmailStr

    @field_validator("password")
    def validate_password(cls, v):
        if not re.match(r"^[^\s]{8,60}$", v):
            raise ValueError("Invalid password format")
        return v
