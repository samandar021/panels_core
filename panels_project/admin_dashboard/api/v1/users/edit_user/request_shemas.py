from typing import List

from pydantic import BaseModel


class PaymentMethodsItem(BaseModel):
    method_id: int
    is_enabled: bool


class EditUserRequest(BaseModel):
    user_id: int
    email: str
    skype: str
    payment_methods: List[PaymentMethodsItem]
