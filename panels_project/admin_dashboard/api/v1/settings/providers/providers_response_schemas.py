from pydantic import BaseModel


class ProviderResponseSchema(BaseModel):
    status: str
    message: str


class PayloadProviderResponse(BaseModel):
    id: int
    form: dict


class SearchProviderSuccessResponse(BaseModel):
    status: str
    payload: PayloadProviderResponse
