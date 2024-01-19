from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from modules.connect_to_database.get_session_panel_db import get_domain
from modules.helper.panels_helper import PanelAdminHash, PanelsHelper, get_panels_helper
from panels_project.admin_dashboard.api.v1.auth.auth import get_panel_admin_hash
from panels_project.languages.translator import Translator, get_translate

from .response_schemas import MainRequestPanelAdmin, OrdersKeys, PayloadsMainRequest, ReqponseMainRequest, SettingsKeys

router = APIRouter()


async def generate_data_in_section(
    sidebar: dict[str, dict],
    permission: MainRequestPanelAdmin,
    translater: Translator
) -> None:
    for key, value in permission.model_dump().items():
        if value is False:
            continue
        title = translater.main_request(key)
        alerts = 0
        alerts_color = ''
        url = '/admin/' + key.replace('_', '-')
        if isinstance(value, dict):
            sidebar_section = sidebar.get(
                key,
                {
                    'title': translater.main_request(key),
                    'alerts': 0,
                    'alerts_color': 'blue',
                    'url': f'/admin/{key}',
                    'section': {}
                }
            )
            for key_nested, value_nested in value.items():
                if value_nested is True:
                    sidebar_section['section'][key_nested] = {
                        'title': translater.main_request(key_nested),
                        'alerts': alerts,
                        'alerts_color': alerts_color,
                        'url': '/admin/' + key_nested.replace('_', '-'),
                    }
                    sidebar[key] = sidebar_section
        else:
            sidebar[key] = {
                'title': title,
                'alerts': alerts,
                'alerts_color': alerts_color,
                'url': url,
                'section': {}
            }


@router.get(
    '',
    response_model=ReqponseMainRequest,
    summary=(
        'This request provides all the information on the menu, the language code of the admin panel,'
        'whether the darkmod is enabled.'
    )
)
async def request_main_admin_panel(
    domain: Annotated[str, Depends(get_domain)],
    panels_helper: Annotated[PanelsHelper, Depends(get_panels_helper)],
    panel_admin_hash: Annotated[PanelAdminHash, Depends(get_panel_admin_hash)],
    translater: Annotated[Translator, Depends(get_translate)]
):
    """
    This request will need to be made every time you switch between sections.

    This request provides all the information on the menu, the language code of the admin panel,
    whether the darkmod is enabled.
    """
    panel_admin = await panels_helper.get_panel_admin_by_id(panel_admin_hash.panel_admin_id)
    if panel_admin is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    sidebar: dict[str, dict] = {}

    orders = OrdersKeys(**panel_admin.rules)
    settings = SettingsKeys(**panel_admin.rules)
    all_permission = MainRequestPanelAdmin(**panel_admin.rules, settings=settings, orders=orders)
    await generate_data_in_section(sidebar, all_permission, translater)

    help_ = {
        "title": translater.main_request.help(),
        "url": "/admin/help",
        "alert": 0,
        "alert_color": "red"
    }
    notifications = {
        "title": translater.main_request.notifications(),
        "url": "/admin/notification",
        "alert": 1,
        "alert_color": "red"
    }
    account = {
        "avatar": "http://example.com/images/1.jpg",
        "display_name": translater.main_request.test_testovich(),
        "account": {
            "title": translater.main_request.account(),
            "url": "/admin/account"
        },
        "darkmode": {
            "title": translater.main_request.dark_mode()
        },
        "logout": {
            "title": translater.main_request.logout(),
            "url": "/admin/logout"
        }
    }

    payloads = PayloadsMainRequest(
        title=domain,
        sidebar=sidebar,
        help=help_,
        notifications=notifications,
        account=account,
        dark_mode=bool(panel_admin.dark_mode),
        language=panel_admin.lang_code
    )
    return ReqponseMainRequest(status='ok', payloads=payloads)
