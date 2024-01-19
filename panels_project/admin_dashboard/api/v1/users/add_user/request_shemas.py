from typing import List

from pydantic import BaseModel


class PaymentMethodsItem(BaseModel):
    method_id: int
    is_enabled: bool


class AddUserRequest(BaseModel):
    email: str
    password: str
    skype: str
    payment_methods: List[PaymentMethodsItem]
