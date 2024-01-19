from fastapi import APIRouter, Depends

from panels_project.admin_dashboard.api.v1.auth.auth import get_panel_admin_hash

router = APIRouter()

fixed_response = {
    "status": "ok",
    "payloads": {
        "user": {
            "id": 2,
            "first_name": "Tito",
            "last_name": "Trke",
            "phone": "11.com",
            "website": "111.com",
            "telegram": "11.com",
            "skype": "11.com",
            "whatsapp": "11.com",
            "balance": "23.999",
            "spent": "2.322",
            "status": 1,
            "created": "2023-03-20",
            "last_auth": "2023-08-20",
            "discount": 20,
            "custom_rates": 0
        },
        "stats": {

        },
        "status_list": {
            "0": "Active",
            "1": "Suspended",
            "2": "Unconfirmed"
        },
        "acces_rules": {
            "add_user": True,
            "edit_user": True,
            "change_status": True,
            "edit_discount": True,
            "export_users": True,
            "activity_log": True
        }
    }
}


@router.get("/", dependencies=[Depends(get_panel_admin_hash)])
async def get_user(user_id: int):
    return fixed_response
