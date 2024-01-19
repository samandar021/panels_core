from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool
    captcha_field: str
    csrf: str
