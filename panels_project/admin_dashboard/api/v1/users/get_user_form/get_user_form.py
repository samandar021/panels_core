from fastapi import APIRouter, Depends

from panels_project.admin_dashboard.api.v1.auth.auth import get_panel_admin_hash

router = APIRouter()

fixed_response = {
    "status": "ok",
    "payloads": {
        "fields": {
            "email": "Email",
            "password": "Password",
            "cpf": "CPF field",
            "website": "Website",
            "telegram": "Telegram",
            "skype": "Skype",
            "whatsapp": "Whatsapp"
        },
        "payment_methods": [
            {
                "name": "Perfect money",
                "method_id": 4,
                "status": 1,
                "available_for_user": False,
            },
            {
                "name": "Perfect money",
                "method_id": 4,
                "status": 0,
                "available_for_user": True,
            }
        ]
    }
}


@router.get("/", dependencies=[Depends(get_panel_admin_hash)])
async def get_user_form():
    return fixed_response
