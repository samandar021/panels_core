from pydantic import BaseModel


class ProviderSchema(BaseModel):
    provider_id: int


class DomainProviderSchema(BaseModel):
    domain: str


class AuthFieldProviderSchema(BaseModel):
    auth_field_1: str
    auth_field_2: str
    auth_field_3: str


class CreateProviderSchema(AuthFieldProviderSchema, DomainProviderSchema):
    pass


class ProviderUpdateSchema(AuthFieldProviderSchema, ProviderSchema):
    pass
