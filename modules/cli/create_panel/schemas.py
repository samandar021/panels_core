import re

from pydantic import BaseModel, EmailStr, field_validator


class CreatePanel(BaseModel):
    panel_domain: str
    is_subdomain: bool
    email: EmailStr
    password: str
    currency: str

    @classmethod
    @field_validator("password")
    def validate_password(cls, v):
        if not re.match(r"^\S{8,60}$", v):
            raise ValueError("Invalid password format")
        return v
