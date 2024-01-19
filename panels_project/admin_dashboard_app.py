from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from fastapi_csrf_protect.exceptions import CsrfProtectError  # type: ignore

from modules.config_manager.config_manager import get_configs
from modules.connect_to_database.get_session_panel_db import found_panels_db_by_domain
from panels_project.admin_dashboard.api.v1.account.routers.switch_dark_mode_router import app_dark_mode
from panels_project.admin_dashboard.api.v1.auth.auth import generate_unsuccessful_login_response
from panels_project.admin_dashboard.api.v1.auth.auth import router as auth_router
from panels_project.admin_dashboard.api.v1.main_request.main_request import router as main_request_router
from panels_project.admin_dashboard.api.v1.settings.languages.languages_routes import app_langs_router
from panels_project.admin_dashboard.api.v1.settings.providers.providers_routes import app_providers
from panels_project.admin_dashboard.api.v1.two_fa.two_fa import router as two_fa_router
from panels_project.csrf_protect import CsrfProtectBody
from panels_project.exception import AuthorizationException, Is2FAException, NotFoundPanelByDomainException
from panels_project.i18n_middleware import I18nMiddleware
from panels_project.languages.translator import get_translate
from panels_project.utils import CustomFastAPI

""" User API Folders"""
from panels_project.admin_dashboard.api.v1.users.add_user.add_user import router as post_add_user
from panels_project.admin_dashboard.api.v1.users.change_status.change_status import router as post_change_status
from panels_project.admin_dashboard.api.v1.users.copy_custom_rates.copy_custom_rates import \
    router as post_copy_custom_rates
from panels_project.admin_dashboard.api.v1.users.copy_discount.copy_discount import router as post_copy_discount
from panels_project.admin_dashboard.api.v1.users.created_export.created_export import router as post_created_export
from panels_project.admin_dashboard.api.v1.users.delete_custom_rate.delete_custom_rate import \
    router as post_delete_custom_rate
from panels_project.admin_dashboard.api.v1.users.delete_discount.delete_discount import router as post_delete_discount
from panels_project.admin_dashboard.api.v1.users.edit_user.edit_user import router as post_edit_user
from panels_project.admin_dashboard.api.v1.users.export_download.export_download import router as get_created_export
from panels_project.admin_dashboard.api.v1.users.export_listing.export_listing import router as get_export_listing
from panels_project.admin_dashboard.api.v1.users.get_custom_rates.get_custom_rates import router as get_custom_rates
from panels_project.admin_dashboard.api.v1.users.get_user.get_user import router as get_user
from panels_project.admin_dashboard.api.v1.users.get_user_form.get_user_form import router as get_user_form
from panels_project.admin_dashboard.api.v1.users.listing.listing import router as get_user_listing
from panels_project.admin_dashboard.api.v1.users.set_discount.set_discount import router as post_set_discount
from panels_project.admin_dashboard.api.v1.users.set_password.set_password import router as post_set_password
from panels_project.admin_dashboard.api.v1.users.update_columns.update_columns import router as post_update_columns
from panels_project.admin_dashboard.api.v1.users.update_custom_rates.update_custom_rates import \
    router as post_update_custom_rates

app_admin_dashboard = CustomFastAPI(
    title='AdminDashboard',
    dependencies=[Depends(found_panels_db_by_domain)]
)

app_admin_dashboard.include_router(auth_router, prefix='/api/v1/auth', tags=['Auth login'])
app_admin_dashboard.include_router(two_fa_router, prefix='/api/v1/2fa', tags=['2fa login'])
app_admin_dashboard.include_router(app_dark_mode, prefix='/api/v1/account', tags=['Dark mode'])
app_admin_dashboard.include_router(main_request_router, prefix='/api/v1/main-request', tags=['Main Request'])

""" User API Methods"""

app_admin_dashboard.include_router(get_user_listing, prefix='/api/v1/users/listing', tags=['API User'])
app_admin_dashboard.include_router(post_update_columns, prefix='/api/v1/users/update_columns', tags=['API User'])
app_admin_dashboard.include_router(post_change_status, prefix='/api/v1/users/change_status', tags=['API User'])
app_admin_dashboard.include_router(post_delete_custom_rate, prefix='/api/v1/users/delete_custom_rate',
                                   tags=['API User'])
app_admin_dashboard.include_router(post_delete_discount, prefix='/api/v1/users/delete_discount',
                                   tags=['API User'])
app_admin_dashboard.include_router(post_set_discount, prefix='/api/v1/users/set_discount', tags=['API User'])
app_admin_dashboard.include_router(post_copy_discount, prefix='/api/v1/users/copy_discount', tags=['API User'])
app_admin_dashboard.include_router(post_copy_custom_rates, prefix='/api/v1/users/copy_custom_rates',
                                   tags=['API User'])
app_admin_dashboard.include_router(post_update_custom_rates, prefix='/api/v1/users/update_custom_rates',
                                   tags=['API User'])
app_admin_dashboard.include_router(get_custom_rates, prefix='/api/v1/users/get_custom_rates',
                                   tags=['API User'])
app_admin_dashboard.include_router(get_user, prefix='/api/v1/users/get_user',
                                   tags=['API User'])
app_admin_dashboard.include_router(post_set_password, prefix='/api/v1/users/set_password',
                                   tags=['API User'])
app_admin_dashboard.include_router(get_user_form, prefix='/api/v1/users/get_user_form',
                                   tags=['API User'])
app_admin_dashboard.include_router(post_add_user, prefix='/api/v1/users/add_user',
                                   tags=['API User'])
app_admin_dashboard.include_router(post_edit_user, prefix='/api/v1/users/edit_user',
                                   tags=['API User'])
app_admin_dashboard.include_router(get_export_listing, prefix='/api/v1/users/export_listing',
                                   tags=['API User'])
app_admin_dashboard.include_router(post_created_export, prefix='/api/v1/users/created_export',
                                   tags=['API User'])
app_admin_dashboard.include_router(get_created_export, prefix='/api/v1/users/export_id',
                                   tags=['API User'])

""" Language API Methods"""
app_admin_dashboard.include_router(app_langs_router, prefix='/api/v1/settings/languages', tags=['Languages'])

"""Providers API Methods"""
app_admin_dashboard.include_router(app_providers, prefix='/api/v1/settings/providers', tags=['Providers'])

app_admin_dashboard.add_middleware(I18nMiddleware)


@app_admin_dashboard.exception_handler(Is2FAException)
async def is_2fa_exception_handler(request: Request, exc: Is2FAException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'status': 'fail', 'payload': {'2fa': True}}
    )


@app_admin_dashboard.exception_handler(AuthorizationException)
async def authorization_exception_handler(request: Request, exc: AuthorizationException):
    translater = get_translate(request)
    return JSONResponse(
        status_code=exc.status_code,
        content={'status': 'fail', 'message': translater.authorization('Unauthorized')}
    )


@app_admin_dashboard.exception_handler(CsrfProtectError)
async def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    translater = get_translate(request)
    config = get_configs()
    csrf_protect = CsrfProtectBody()
    return await generate_unsuccessful_login_response(
        request,
        config,
        translater,
        csrf_protect,
        error='Invalid or missing CSRF token'
    )


@app_admin_dashboard.exception_handler(NotFoundPanelByDomainException)
async def not_found_panel_by_domain_exception_handler(request: Request, exc: NotFoundPanelByDomainException):
    translater = get_translate(request)
    return JSONResponse(
        status_code=exc.status_code,
        content={'status': 'fail', 'message': translater.exception('domain_not_found')}
    )


@app_admin_dashboard.get('/ping', tags=['Ping'], include_in_schema=False)
async def ping() -> str:
    return 'Admin dashboard'
