from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from migration_system.models.panel_models import PanelAdminHash
from modules.helper.activity_log_helper import ActivityLogHelper, get_activity_log_helper
from modules.helper.panels_helper import PanelsHelper, get_panels_helper
from modules.helper.providers_helper import ProviderHelper, get_provider_helper
from panels_project.admin_dashboard.api.v1.auth.auth import get_panel_admin_hash
from panels_project.admin_dashboard.api.v1.settings.providers.providers_request_schemas import (CreateProviderSchema,
                                                                                                DomainProviderSchema,
                                                                                                ProviderSchema,
                                                                                                ProviderUpdateSchema)
from panels_project.admin_dashboard.api.v1.settings.providers.providers_response_schemas import ProviderResponseSchema
from panels_project.exception import AuthorizationException
from panels_project.languages.translator import Translator, get_translate

app_providers = APIRouter()


@app_providers.post("/create")
async def create_provider(
        request: Request,
        data: CreateProviderSchema,
        panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)],
        panel_admin_hash: Annotated[PanelAdminHash, Depends(get_panel_admin_hash)],
        activity_log_helper: Annotated[ActivityLogHelper, Depends(get_activity_log_helper)],
        translater: Annotated[Translator, Depends(get_translate)],
        provider_helper: ProviderHelper = Depends(get_provider_helper)
):
    panel_admin = await panels_helper.get_panel_admin_by_id(panel_admin_hash.panel_admin_id)
    if panel_admin is None:
        raise AuthorizationException(status_code=status.HTTP_401_UNAUTHORIZED)

    panel_id = panel_admin.panel_id

    result = await provider_helper.create_provider(data, panel_id)

    if result is None:
        return ProviderResponseSchema(status="ok", message=translater.settings_providers("Failed to create provider"))

    await activity_log_helper.create_activity_log_and_activity_log_details(
        request,
        panels_helper,
        panel_admin_hash.panel_admin_id,
        panel_admin_hash.super_admin
    )

    return result


@app_providers.post("/edit_provider")
async def edit_provider(
        request: Request,
        data: ProviderUpdateSchema,
        panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)],
        panel_admin_hash: Annotated[PanelAdminHash, Depends(get_panel_admin_hash)],
        activity_log_helper: Annotated[ActivityLogHelper, Depends(get_activity_log_helper)],
        translater: Annotated[Translator, Depends(get_translate)],
        provider_helper: ProviderHelper = Depends(get_provider_helper)
):
    panel_admin = await panels_helper.get_panel_admin_by_id(panel_admin_hash.panel_admin_id)
    if panel_admin is None:
        raise AuthorizationException(status_code=status.HTTP_401_UNAUTHORIZED)

    panel_id = panel_admin.panel_id

    result = await provider_helper.edit_provider(data, panel_id)

    if result is None:
        return ProviderResponseSchema(status="ok", message=translater.settings_providers("Failed to edit provider"))

    await activity_log_helper.create_activity_log_and_activity_log_details(
        request,
        panels_helper,
        panel_admin_hash.panel_admin_id,
        panel_admin_hash.super_admin
    )

    return result


@app_providers.post("/delete_provider")
async def delete_provider(
        request: Request,
        data: ProviderSchema,
        panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)],
        panel_admin_hash: Annotated[PanelAdminHash, Depends(get_panel_admin_hash)],
        activity_log_helper: Annotated[ActivityLogHelper, Depends(get_activity_log_helper)],
        translater: Annotated[Translator, Depends(get_translate)],
        provider_helper: ProviderHelper = Depends(get_provider_helper)
):
    panel_admin = await panels_helper.get_panel_admin_by_id(panel_admin_hash.panel_admin_id)
    if panel_admin is None:
        raise AuthorizationException(status_code=status.HTTP_401_UNAUTHORIZED)

    panel_id = panel_admin.panel_id

    result = await provider_helper.delete_provider(data, panel_id)

    if result is None:
        return ProviderResponseSchema(status="ok", message=translater.settings_providers("Failed to delete provider"))

    await activity_log_helper.create_activity_log_and_activity_log_details(
        request,
        panels_helper,
        panel_admin_hash.panel_admin_id,
        panel_admin_hash.super_admin
    )

    return result


@app_providers.post("/search")
async def search_provider(
        request: Request,
        data: DomainProviderSchema,
        panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)],
        panel_admin_hash: Annotated[PanelAdminHash, Depends(get_panel_admin_hash)],
        activity_log_helper: Annotated[ActivityLogHelper, Depends(get_activity_log_helper)],
        provider_helper: ProviderHelper = Depends(get_provider_helper)
):
    panel_admin = await panels_helper.get_panel_admin_by_id(panel_admin_hash.panel_admin_id)
    if panel_admin is None:
        raise AuthorizationException(status_code=status.HTTP_401_UNAUTHORIZED)

    panel_id = panel_admin.panel_id

    result = await provider_helper.search_provider(data, panel_id)

    if result is None:
        return ProviderResponseSchema(status="ok", message="Failed to search provider")

    await activity_log_helper.create_activity_log_and_activity_log_details(
        request,
        panels_helper,
        panel_admin_hash.panel_admin_id,
        panel_admin_hash.super_admin
    )

    return result


@app_providers.get("/get_balance")
async def get_provider_balance(
        panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)],
        panel_admin_hash: Annotated[PanelAdminHash, Depends(get_panel_admin_hash)],
):
    panel_admin = await panels_helper.get_panel_admin_by_id(panel_admin_hash.panel_admin_id)
    if panel_admin is None:
        raise AuthorizationException(status_code=status.HTTP_401_UNAUTHORIZED)

    fixed_response = {
        "status": "ok",
        "payloads": {
            "data": [
                {
                    "id": "1",
                    "provider_balance": 0,
                    "provider_converted": 0,
                    "balance_status": "done",
                    "provider_currency": "USD",
                    "form": {
                        "auth_field_2": {"name": "login"},
                        "auth_field_3": {"name": "password"},
                    }
                },
                {
                    "id": "2",
                    "provider_balance": 0,
                    "provider_converted": 0,
                    "balance_status": "queued",
                    "provider_currency": "TRY",
                    "form": {
                        "auth_field_1": {"name": "Login"},
                        "auth_field_2": {"name": "Password"},
                        "auth_field_3": {"name": "API key"},
                    }
                },
                {
                    "id": "2",
                    "provider_balance": 0,
                    "provider_converted": 0,
                    "balance_status": "error",
                    "provider_currency": "AED",
                    "balance_error": "API key incorect",
                    "form": {
                        "auth_field_1": {"name": "APIKey"}
                    }
                }
            ]
        }
    }

    return fixed_response


@app_providers.get("/providers")
async def get_providers(
        panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)],
        panel_admin_hash: Annotated[PanelAdminHash, Depends(get_panel_admin_hash)]
):
    panel_admin = await panels_helper.get_panel_admin_by_id(panel_admin_hash.panel_admin_id)
    if panel_admin is None:
        raise AuthorizationException(status_code=status.HTTP_401_UNAUTHORIZED)

    fixed_response = {
        "status": "ok",
        "payloads": {
            "data": [
                {
                    "id": "1",
                    "domain": "example.com",
                    "alias": "example",
                    "provider_balance": 0,
                    "provider_converted": 0,
                    "provider_currency": "USD",
                    "balance_status": "done"
                },
                {
                    "id": "2",
                    "domain": "example2.com",
                    "alias": "example2",
                    "provider_balance": 0,
                    "provider_converted": 0,
                    "provider_currency": "TRY",
                    "balance_status": "queued"
                },
                {
                    "id": "2",
                    "domain": "example2.com",
                    "alias": "example2",
                    "provider_balance": 0,
                    "provider_converted": 0,
                    "balance_status": "error",
                    "provider_currency": "AED",
                    "balance_error": "API key incorect"
                }
            ]
        }
    }
    return fixed_response
