from datetime import datetime
from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse

from migration_system.models.panel_models import PanelAdminHash
from modules.helper.panels_helper import PanelsHelper, get_panels_helper
from panels_project.csrf_protect import CsrfProtectBody

from ..auth.auth import get_panel_admin_hash
from .request_shemas import TwoFARequest
from .response_shemas import (PayloadsFetchConfResponse, PayloadsVerifyResponse, SuccessfulFetchConfResponse,
                              SuccessfulVerifyResponse, UnsuccessfulVerifyResponse)

router = APIRouter()


async def generate_data_fetch_conf(admin_auth_code, csrf_protect):
    csrf, signed_token = csrf_protect.generate_csrf_tokens()
    payloads = PayloadsFetchConfResponse(
        code=str(admin_auth_code.auth_code),
        code_location='email',
        csrf=csrf
    )
    return payloads, signed_token


@router.get(
    '/fetch_conf',
    response_model=SuccessfulFetchConfResponse,
    summary='Data for rendering the 2fa authorization page.'
)
async def two_fa_fetch_conf(
        panel_admin_hash: Annotated[PanelAdminHash, Depends(get_panel_admin_hash)],
        panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)],
        csrf_protect: CsrfProtectBody = Depends()
):
    """
    This method returns the necessary data for rendering the 2fa authorization page,
    shows where the code was sent, and displays the code for the environment dev.

    It also gives an up-to-date csrf token, in case the client made a request and received an error,
    you need to re-request the data.
    """
    admin_auth_code = await panels_helper.get_panel_admin_auth_code_by_panel_admin_hash_id(panel_admin_hash.id)
    if admin_auth_code is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    payloads, signed_token = await generate_data_fetch_conf(admin_auth_code, csrf_protect)

    response_data = SuccessfulFetchConfResponse(status='ok', payloads=payloads).model_dump()
    response = JSONResponse(content=response_data, status_code=status.HTTP_200_OK)
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response


@router.post(
    '/verify',
    response_model=Union[SuccessfulVerifyResponse, UnsuccessfulVerifyResponse],
    summary='This method checks the CSRF token and the authentication code.'
)
async def two_fa_verify(
        request: Request,
        response: Response,
        verify_data: TwoFARequest,
        panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)],
        panel_admin_hash_obj: Annotated[PanelAdminHash, Depends(get_panel_admin_hash)],
        csrf_protect: CsrfProtectBody = Depends()
):
    """
    This method checks the CSRF token and the authentication code.

    In case of 3 unsuccessful attempts, we send the user to the authorization page.

    If the redirect_to_auth parameter is true, then we send the user to the authorization page.
    """
    await csrf_protect.validate_csrf(request)
    if panel_admin_hash_obj.is_2fa_step == 0:
        return SuccessfulVerifyResponse(status='ok', payloads={"2fa": False})

    admin_auth_code = await panels_helper.get_panel_admin_auth_code_by_panel_admin_hash_id(panel_admin_hash_obj.id)
    if admin_auth_code is None:
        raise HTTPException(status_code=403)

    if int(datetime.now().timestamp()) - admin_auth_code.created_at >= 10 * 60:
        await panels_helper.update_panel_admin_auth_code__created_at_and_code(admin_auth_code)
        payloads, signed_token = await generate_data_fetch_conf(admin_auth_code, csrf_protect)

        payloads = PayloadsVerifyResponse(
            redirect_to_auth=False,
            code=payloads.code,
            code_location=payloads.code_location,
            csrf=payloads.csrf
        ).model_dump()
        response_data = UnsuccessfulVerifyResponse(status='fail', payloads=payloads).model_dump()
        response = JSONResponse(content=response_data, status_code=status.HTTP_401_UNAUTHORIZED)
        csrf_protect.set_csrf_cookie(signed_token, response)
        return response

    if verify_data.code != str(admin_auth_code.auth_code):
        if admin_auth_code.attempts == 3:
            payloads = PayloadsVerifyResponse(redirect_to_auth=True)
            await panels_helper.delete_panel_admin_auth_code_obj(panel_admin_hash_obj.id)
            await panels_helper.delete_panel_admin_hash_obj(panel_admin_hash_obj.id)
            response_data = UnsuccessfulVerifyResponse(status='fail', payloads=payloads).model_dump()
            response = JSONResponse(content=response_data, status_code=status.HTTP_401_UNAUTHORIZED)
            response.delete_cookie('authorization-token')
        else:
            attempts = admin_auth_code.attempts + 1
            await panels_helper.update_panel_admin_auth_code__attempts(admin_auth_code, attempts)
            payloads, signed_token = await generate_data_fetch_conf(admin_auth_code, csrf_protect)

            payloads = PayloadsVerifyResponse(
                redirect_to_auth=False,
                code=payloads.code,
                code_location=payloads.code_location,
                csrf=payloads.csrf
            ).model_dump()
            response_data = UnsuccessfulVerifyResponse(status='fail', payloads=payloads).model_dump()
            response = JSONResponse(content=response_data, status_code=status.HTTP_401_UNAUTHORIZED)
            csrf_protect.set_csrf_cookie(signed_token, response)

        return response

    await panels_helper.update_panel_admin_hash_obj(panel_admin_hash_obj, False)
    return SuccessfulVerifyResponse(status='ok', payloads={})
