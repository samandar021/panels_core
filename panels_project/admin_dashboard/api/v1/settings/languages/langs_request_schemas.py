from typing import Dict, Optional

from pydantic import BaseModel, Field, field_validator


class LanguageCodeSchema(BaseModel):
    lang_code: str = Field(..., pattern="^[a-zA-Z]{1,2}$")

    @classmethod
    @field_validator("lang_code", mode='before')
    def set_lang_code_to_lower(cls, value):
        return value.lower()


class LanguageEdit(LanguageCodeSchema):
    lang_name: Optional[str] = None
    variables: Optional[Dict[str, str]] = None


class LangChangeStatus(LanguageCodeSchema):
    status: int


class SortLanguageSchema(LanguageCodeSchema):
    old_position: int
    new_position: int
