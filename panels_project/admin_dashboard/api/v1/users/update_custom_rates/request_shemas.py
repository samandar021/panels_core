from typing import List

from pydantic import BaseModel


class CustomRatesItem(BaseModel):
    service_id: int
    rate: float
    is_percent: bool

    # @field_validator("rate")
    # def validate_rate(cls, v, values):
    #     if values.get("is_percent"):
    #         if not (0 <= v <= 10000):
    #             raise ValueError("Rate must be between 0 and 10000 for percentage values")
    #     else:
    #         # Perform validation based on your minimum price logic
    #         # You can adjust the validation rules according to your needs
    #         if v < MINIMUM_PRICE_FOR_NON_PERCENT:
    #             raise ValueError(f"Rate must be at least {MINIMUM_PRICE_FOR_NON_PERCENT}")
    #     return v


class UpdateCustomRatesRequest(BaseModel):
    user_id: int
    custom_rates: List[CustomRatesItem]
