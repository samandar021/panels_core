from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class LanguageResponseSchema(BaseModel):
    status: str
    message: str


class LanguageDataSchema(BaseModel):
    code: str
    is_visible: bool
    updated: Optional[str]
    position: int
    name: str


class AvailableLanguagesSchema(BaseModel):
    lang_code: str
    name: str


class SortSchema(BaseModel):
    is_active: Optional[None] = Field(None, alias='is_active')


class ColumnSchema(BaseModel):
    sort: Optional[SortSchema]
    name: str


class PayloadsSchema(BaseModel):
    access_rules: Dict = {}
    data: List[LanguageDataSchema]
    columns: Dict[str, ColumnSchema]
    list: List[str]
    available_languages: List[AvailableLanguagesSchema]


class ListingResponseSchema(BaseModel):
    status: str
    payloads: PayloadsSchema
