from base64 import b64decode
from ipaddress import ip_address
from typing import Annotated, Union

import argon2
from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse

from migration_system.models.panel_models import PanelAdminHash
from modules.config_manager.config_manager import get_configs
from modules.helper.activity_log_helper import ActivityLogHelper, get_activity_log_helper
# from modules.helper.geoip_helper import find_county_by_ip
from modules.helper.panels_helper import PanelsHelper, get_panels_helper
from modules.redis.auth_redis import delete_ip_in_redis, get_ip_in_redis, set_ip_in_redis
from panels_project.csrf_protect import CsrfProtectBody
from panels_project.exception import AuthorizationException, Is2FAException
from panels_project.languages.translator import Translator, get_translate

from .request_shemas import LoginRequest
from .response_shemas import (PanelAdminRules, PayloadsCapthaResponse, PayloadsTwoFAResponse, StandartResponse,
                              SuccessfulResponse, UnsuccessfulLoginResponse, UnsuccessfulResponse)

router = APIRouter()


async def get_panel_admin_hash(
    request: Request,
    panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)],
    authorization_token: Annotated[str | None, Cookie(alias='authorization-token', include_in_schema=False)] = None
) -> PanelAdminHash:
    """Проверка авторизован ли пользователь"""
    if authorization_token is None:
        raise AuthorizationException(status_code=status.HTTP_401_UNAUTHORIZED)

    panel_admin_hash_obj = await panels_helper.get_panel_admin_hash_obj_by_hash(authorization_token)
    if panel_admin_hash_obj is None:
        raise AuthorizationException(status_code=status.HTTP_401_UNAUTHORIZED)
    if panel_admin_hash_obj.is_2fa_step is True:
        if '/admin/api/v1/2fa/fetch_conf' != request.url.path and '/admin/api/v1/2fa/verify' != request.url.path:
            raise Is2FAException(status_code=status.HTTP_401_UNAUTHORIZED)

    panel_admin_obj = await panels_helper.get_panel_admin_by_id(panel_admin_hash_obj.panel_admin_id)
    if panel_admin_obj is None:
        raise AuthorizationException(status_code=status.HTTP_401_UNAUTHORIZED)

    rand_string = b64decode(panel_admin_hash_obj.rand_string)
    hash_ = await panels_helper.generate_hash(panel_admin_obj, rand_string)
    if panel_admin_hash_obj.hash != hash_:
        raise AuthorizationException(status_code=status.HTTP_401_UNAUTHORIZED)

    return panel_admin_hash_obj


@router.get(
    '/check-auth',
    summary='This method checks whether the user is authorized or not',
    response_model=StandartResponse
)
async def check_auth(
    request: Request,
    panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)],
    authorization_token: Annotated[str | None, Cookie(alias='authorization-token', include_in_schema=False)] = None
):
    """
    This method checks whether the user is authorized or not, if the user is not authorized,
    then it must be sent to the authorization page with the get parameter of the page where he was previously.
    """
    try:
        await get_panel_admin_hash(request, panels_helper, authorization_token)
    except HTTPException:
        return StandartResponse(status='fail')
    return StandartResponse(status='ok')


async def generate_unsuccessful_login_response(request, config, translater, csrf_protect, error):
    payloads_captha, signed_token = await generate_data_fetch_conf(request, config, csrf_protect)
    response_data = UnsuccessfulLoginResponse(
        status='fail',
        message=translater.authorization(error),
        payloads=payloads_captha
    ).model_dump()
    response = JSONResponse(content=response_data, status_code=status.HTTP_401_UNAUTHORIZED)
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response


@router.post(
    '/login',
    response_model=Union[SuccessfulResponse, UnsuccessfulResponse],
    summary='Authorization.'
)
async def auth_login(
    request: Request,
    login_data: LoginRequest,
    config: Annotated[dict, Depends(get_configs)],
    panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)],
    activity_log_helper: Annotated[ActivityLogHelper, Depends(get_activity_log_helper)],
    translater: Annotated[Translator, Depends(get_translate)],
    csrf_protect: CsrfProtectBody = Depends()
):
    """
    This request checks the administrator's email and password,
    if two-factor authorization is enabled on the account, then the client needs to display the two_face page.

    After successful authorization, redirect the administrator to where he wanted, or to /
    """
    await csrf_protect.validate_csrf(request)
    if request.client is None:
        return await generate_unsuccessful_login_response(
            request,
            config,
            translater,
            csrf_protect,
            error='client ip not found'
        )

    panel_admin_obj = await panels_helper.get_panel_admin_by_email(login_data.email)
    if panel_admin_obj is None:
        await set_ip_in_redis(request.client.host)
        return await generate_unsuccessful_login_response(
            request,
            config,
            translater,
            csrf_protect,
            error='Incorrect email or password'
        )
    if panel_admin_obj.status == 2:
        return await generate_unsuccessful_login_response(
            request,
            config,
            translater,
            csrf_protect,
            error='Incorrect email or password'
        )

    try:
        ph = argon2.PasswordHasher()
        ph.verify(panel_admin_obj.password, f'{login_data.password}.{panel_admin_obj.password_salt}')
    except argon2.exceptions.VerifyMismatchError:
        await set_ip_in_redis(request.client.host)
        return await generate_unsuccessful_login_response(
            request,
            config,
            translater,
            csrf_protect,
            error='Incorrect email or password'
        )
    await delete_ip_in_redis(request.client.host)

    panel_admin_hash_obj = await panels_helper.get_panel_admin_hash_obj_by_id(panel_admin_obj.id)
    if panel_admin_hash_obj is not None:
        await panels_helper.delete_panel_admin_auth_code_obj(panel_admin_hash_obj.id)
        await panels_helper.delete_panel_admin_hash_obj(panel_admin_hash_obj.id)

    if panel_admin_obj.lastip != str(ip_address(request.client.host)):
        is_2fa_step = True
        two_fa = True
    else:
        is_2fa_step = False
        two_fa = False

    panel_admin_hash_obj = await panels_helper.create_panel_admin_hash_obj(
        panel_admin_obj,
        request,
        login_data.remember_me,
        is_2fa_step,
    )
    await panels_helper.update_panel_admin_obj__lastip(panel_admin_obj, request)

    await panels_helper.create_panel_admin_auth_code_obj(panel_admin_obj.id, panel_admin_hash_obj.id)

    await activity_log_helper.create_activity_log_and_activity_log_details(
        request,
        panels_helper,
        panel_admin_obj.id,
        panel_admin_hash_obj.super_admin
    )

    payloads_two_fa = PayloadsTwoFAResponse(two_fa=two_fa)
    response_data = SuccessfulResponse(status='ok', payloads=payloads_two_fa).model_dump(by_alias=True)
    response = JSONResponse(content=response_data)

    if login_data.remember_me:
        cookie_max_age = config['common']['cookies_for_authorization_max']
    else:
        cookie_max_age = config['common']['cookies_for_authorization_min']
    response.set_cookie(key='authorization-token', value=panel_admin_hash_obj.hash, max_age=cookie_max_age)

    return response


async def generate_data_fetch_conf(request, config, csrf_protect):
    captcha = False
    captcha_key = ''
    captcha_provider = ''
    csrf, signed_token = csrf_protect.generate_csrf_tokens()

    if config['common']['admin_captcha_enabled'] == 0:
        payloads_captha = PayloadsCapthaResponse(
            captcha=captcha,
            captcha_key=captcha_key,
            captcha_provider=captcha_provider,
            csrf=csrf,
        )
        return payloads_captha, signed_token

    client_ip = request.client.host
    count_request_ip = await get_ip_in_redis(client_ip)
    if count_request_ip > 0:
        captcha = True
        # country = await find_county_by_ip(client_ip)
        # if country == 'China':
        #     payloads_captha['captcha_key'] = config['common']['captcha']['hcaptcha']['site_keys']
        #     payloads_captha['captcha_provider'] = 'hcaptcha'
        # else:
        captcha_key = config['common']['captcha']['recaptcha']['site_keys']
        captcha_provider = 'recaptcha'
    payloads_captha = PayloadsCapthaResponse(
        captcha=captcha,
        captcha_key=captcha_key,
        captcha_provider=captcha_provider,
        csrf=csrf,
    )
    return payloads_captha, signed_token


@router.get(
    '/fetch_conf',
    response_model=SuccessfulResponse,
    summary='Data for rendering the authorization page.'
)
async def auth_fetch_conf(
    request: Request,
    config: Annotated[dict, Depends(get_configs)],
    translater: Annotated[Translator, Depends(get_translate)],
    csrf_protect: CsrfProtectBody = Depends()
):
    """
    This method returns the necessary data for rendering the authorization page,
    shows whether to display a captcha or not, and which one.

    It also gives an up-to-date csrf token, in case the client made a request and received an error,
    you need to re-request the data and display the captcha if necessary.
    """
    if request.client is None:
        return UnsuccessfulResponse(
            status='fail',
            message=translater.authorization('client ip not found')
        )

    payloads_captha, signed_token = await generate_data_fetch_conf(request, config, csrf_protect)

    response_data = SuccessfulResponse(status='ok', payloads=payloads_captha).model_dump()
    response = JSONResponse(content=response_data, status_code=status.HTTP_200_OK)
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response


@router.get(
    '/permission',
    summary='Get permission to the section.'
)
async def get_permission(
    permission: str,
    panel_admin_hash_obj: Annotated[PanelAdminHash, Depends(get_panel_admin_hash)],
    panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)]
) -> bool | None:
    """Get permission to the section."""
    return await panels_helper.get_permission(panel_admin_hash_obj.panel_admin_id, permission)


@router.get(
    '/all-permission',
    response_model=Union[PanelAdminRules, None],
    summary='Get all permissions for the client.'
)
async def get_all_permission(
    panel_admin_hash_obj: Annotated[PanelAdminHash, Depends(get_panel_admin_hash)],
    panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)]
):
    """Get all permissions for the client."""
    return await panels_helper.get_all_permission(panel_admin_hash_obj.panel_admin_id)
