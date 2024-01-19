from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from migration_system.models.panel_models import PanelAdminHash
from modules.helper.activity_log_helper import ActivityLogHelper, get_activity_log_helper
from modules.helper.languages_helper import LanguagesHelper, get_languages_helper
from modules.helper.panels_helper import PanelsHelper, get_panels_helper
from panels_project.admin_dashboard.api.v1.auth.auth import get_panel_admin_hash
from panels_project.admin_dashboard.api.v1.settings.languages.langs_request_schemas import (LangChangeStatus,
                                                                                            LanguageCodeSchema,
                                                                                            LanguageEdit,
                                                                                            SortLanguageSchema)
from panels_project.admin_dashboard.api.v1.settings.languages.langs_response_schemas import LanguageResponseSchema
from panels_project.exception import AuthorizationException
from panels_project.languages.translator import Translator, get_translate

app_langs_router = APIRouter()


@app_langs_router.post("/create")
async def create_language(
        request: Request,
        language: LanguageCodeSchema,
        panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)],
        panel_admin_hash: Annotated[PanelAdminHash, Depends(get_panel_admin_hash)],
        activity_log_helper: Annotated[ActivityLogHelper, Depends(get_activity_log_helper)],
        translater: Annotated[Translator, Depends(get_translate)],
        language_helper: LanguagesHelper = Depends(get_languages_helper),

):
    result = await language_helper.create_language_helper(language, translater)

    if result is None:
        return LanguageResponseSchema(
            status="error",
            message=translater.chapter_languages('unsuccessfully.Failed to create language'))

    panel_admin = await panels_helper.get_panel_admin_by_id(panel_admin_hash.panel_admin_id)
    await activity_log_helper.create_activity_log_and_activity_log_details(
        request,
        panels_helper,
        panel_admin_hash.panel_admin_id,
        panel_admin_hash.super_admin
    )
    if panel_admin is None:
        raise AuthorizationException(status_code=status.HTTP_401_UNAUTHORIZED)

    return result


@app_langs_router.post("/edit")
async def edit_language(
        request: Request,
        language: LanguageEdit,
        panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)],
        panel_admin_hash: Annotated[PanelAdminHash, Depends(get_panel_admin_hash)],
        activity_log_helper: Annotated[ActivityLogHelper, Depends(get_activity_log_helper)],
        translater: Annotated[Translator, Depends(get_translate)],
        language_helper: LanguagesHelper = Depends(get_languages_helper),
):
    result = await language_helper.edit_language(language, translater)

    if result is None:
        return LanguageResponseSchema(status="error", message=translater.chapter_languages('Failed to edit language'))

    panel_admin = await panels_helper.get_panel_admin_by_id(panel_admin_hash.panel_admin_id)
    await activity_log_helper.create_activity_log_and_activity_log_details(
        request,
        panels_helper,
        panel_admin_hash.panel_admin_id,
        panel_admin_hash.super_admin
    )
    if panel_admin is None:
        raise AuthorizationException(status_code=status.HTTP_401_UNAUTHORIZED)

    return result


@app_langs_router.post("/change_status")
async def change_status_language(
        request: Request,
        language: LangChangeStatus,
        panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)],
        panel_admin_hash: Annotated[PanelAdminHash, Depends(get_panel_admin_hash)],
        activity_log_helper: Annotated[ActivityLogHelper, Depends(get_activity_log_helper)],
        translater: Annotated[Translator, Depends(get_translate)],
        language_helper: LanguagesHelper = Depends(get_languages_helper),
):
    result = await language_helper.change_status_helper(language, translater)

    if result is None:
        return LanguageResponseSchema(status="error",
                                      message=translater.chapter_languages('Failed to change status of language'))

    panel_admin = await panels_helper.get_panel_admin_by_id(panel_admin_hash.panel_admin_id)
    await activity_log_helper.create_activity_log_and_activity_log_details(
        request,
        panels_helper,
        panel_admin_hash.panel_admin_id,
        panel_admin_hash.super_admin
    )
    if panel_admin is None:
        raise AuthorizationException(status_code=status.HTTP_401_UNAUTHORIZED)

    return result


@app_langs_router.post("/default")
async def make_default_language(
        request: Request,
        language: LanguageCodeSchema,
        panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)],
        panel_admin_hash: Annotated[PanelAdminHash, Depends(get_panel_admin_hash)],
        activity_log_helper: Annotated[ActivityLogHelper, Depends(get_activity_log_helper)],
        translater: Annotated[Translator, Depends(get_translate)],
        language_helper: LanguagesHelper = Depends(get_languages_helper),
):
    result = await language_helper.change_default_language(language, translater)

    if result is None:
        return LanguageResponseSchema(status="error",
                                      message=translater.chapter_languages('Failed to make default language'))

    panel_admin = await panels_helper.get_panel_admin_by_id(panel_admin_hash.panel_admin_id)
    await activity_log_helper.create_activity_log_and_activity_log_details(
        request,
        panels_helper,
        panel_admin_hash.panel_admin_id,
        panel_admin_hash.super_admin
    )
    if panel_admin is None:
        raise AuthorizationException(status_code=status.HTTP_401_UNAUTHORIZED)

    return result


@app_langs_router.post("/sort")
async def sort_language(
        request: Request,
        sort_data: SortLanguageSchema,
        panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)],
        panel_admin_hash: Annotated[PanelAdminHash, Depends(get_panel_admin_hash)],
        activity_log_helper: Annotated[ActivityLogHelper, Depends(get_activity_log_helper)],
        translater: Annotated[Translator, Depends(get_translate)],
        language_helper: LanguagesHelper = Depends(get_languages_helper),
):
    result = await language_helper.sort_languages_helper(sort_data, translater)

    if result is None:
        return LanguageResponseSchema(status="error",
                                      message=translater.chapter_languages('Failed to change position of language'))

    panel_admin = await panels_helper.get_panel_admin_by_id(panel_admin_hash.panel_admin_id)
    await activity_log_helper.create_activity_log_and_activity_log_details(
        request,
        panels_helper,
        panel_admin_hash.panel_admin_id,
        panel_admin_hash.super_admin
    )
    if panel_admin is None:
        raise AuthorizationException(status_code=status.HTTP_401_UNAUTHORIZED)

    return result


@app_langs_router.get("/reset")
async def reset_language_changes(
        request: Request,
        language: LanguageCodeSchema,
        panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)],
        panel_admin_hash: Annotated[PanelAdminHash, Depends(get_panel_admin_hash)],
        activity_log_helper: Annotated[ActivityLogHelper, Depends(get_activity_log_helper)],
        translater: Annotated[Translator, Depends(get_translate)],
        language_helper: LanguagesHelper = Depends(get_languages_helper),
):
    result = await language_helper.reset_language_changes(language, translater)

    if result is None:
        return LanguageResponseSchema(status="error",
                                      message=translater.chapter_languages('Failed to reset language changes'))

    panel_admin = await panels_helper.get_panel_admin_by_id(panel_admin_hash.panel_admin_id)
    await activity_log_helper.create_activity_log_and_activity_log_details(
        request,
        panels_helper,
        panel_admin_hash.panel_admin_id,
        panel_admin_hash.super_admin
    )
    if panel_admin is None:
        raise AuthorizationException(status_code=status.HTTP_401_UNAUTHORIZED)

    return result


@app_langs_router.get("/listing")
async def get_languages(
        panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)],
        panel_admin_hash: Annotated[PanelAdminHash, Depends(get_panel_admin_hash)],
        translater: Annotated[Translator, Depends(get_translate)],
        language_helper: LanguagesHelper = Depends(get_languages_helper),
):
    panel_admin = await panels_helper.get_panel_admin_by_id(panel_admin_hash.panel_admin_id)
    if panel_admin is None:
        raise AuthorizationException(status_code=status.HTTP_401_UNAUTHORIZED)

    result = await language_helper.get_languages()

    if result is None:
        return LanguageResponseSchema(status="error",
                                      message=translater.chapter_languages('Failed to get listing of languages'))

    return result
