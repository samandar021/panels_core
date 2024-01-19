from pydantic import BaseModel


class StandartResponse(BaseModel):
    status: str


class PayloadsVerifyResponse(BaseModel):
    redirect_to_auth: bool
    code: str | None = None
    code_location: str | None = None
    csrf: str | None = None


class UnsuccessfulVerifyResponse(StandartResponse):
    payloads: PayloadsVerifyResponse


class PayloadsFetchConfResponse(BaseModel):
    code: str | None = None
    code_location: str
    csrf: str


class SuccessfulFetchConfResponse(StandartResponse):
    payloads: PayloadsFetchConfResponse


class SuccessfulVerifyResponse(StandartResponse):
    payloads: dict
