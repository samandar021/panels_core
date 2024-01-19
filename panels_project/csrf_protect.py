from typing import Any

from fastapi_csrf_protect import CsrfProtect  # type: ignore
from pydantic import BaseModel, create_model

from modules.config_manager.config_manager import get_configs


class CsrfSettings(BaseModel):
    secret_key: str = get_configs()['common']['secret_key']
    token_key: str = 'csrf'
    token_location: str = 'body'


class CsrfProtectBody(CsrfProtect):
    def get_csrf_from_body(self, data: bytes) -> str:
        """
        Get token from the request body

        ---
        :param data: attached request body containing cookie data with configured `token_key`
        :type data: bytes
        """
        fields: dict[str, Any] = {self._token_key: (str, "csrf-token")}
        Body = create_model("Body", **fields)
        content: str = (
            data.decode("utf-8").replace("&", '","').replace("=", '":"')
        )
        body = Body.parse_raw(content)
        return body.dict()[self._token_key]


@CsrfProtectBody.load_config
def get_csrf_config():
    return CsrfSettings()
