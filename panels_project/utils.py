from fastapi import FastAPI

from modules.config_manager.config_manager import get_configs


class CustomFastAPI(FastAPI):
    def __init__(self, *args, **kwargs):
        config = get_configs()
        docs_url = config["common"]["docs_url"]
        kwargs["docs_url"] = docs_url
        kwargs["redoc_url"] = docs_url
        kwargs["swagger_ui_oauth2_redirect_url"] = f"{docs_url}/oauth2-redirect"
        super().__init__(*args, **kwargs)
