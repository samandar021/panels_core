from fastapi import APIRouter, Depends

from panels_project.admin_dashboard.api.v1.auth.auth import get_panel_admin_hash

router = APIRouter()

fixed_data = {
    "status": "ok",
    "payloads": {
        "acces_rules": {
            "export_users": True
        },

        "data": [
            {
                "from": "2022-02-02 20:20:22",
                "to": "2023-02-02 20:20:22",
                "status": 1,
                "format": "CSV",
                "created": "2023-02-02 20:20:22",
                "link": "https://example.com/wxpoer/12.csv"
            },
            {
                "from": "2022-02-02 20:20:22",
                "to": "2023-02-02 20:20:22",
                "status": 1,
                "format": "CSV",
                "created": "2023-02-02 20:20:22",
                "link": "https://example.com/wxpoer/12.csv"
            }
        ],
        "pages": {
            "current_page": "текущая страница",
            "row_per_page": "количество запись на страницу",
            "page_quantity": "количество страниц",
            "row_quantity": "количество записей"
        },
        "columns": {
            "available": {
                "from": {
                    "sort": None,
                    "name": "From"
                },
                "to": {
                    "sort": None,
                    "name": "To"
                },
                "status": {
                    "sort": None,
                    "name": "Status"
                },
                "format": {
                    "sort": None,
                    "name": "Format"
                },
                "created": {
                    "sort": None,
                    "name": "Created"
                },
            },
            "list": [
                "from",
                "to",
                "status",
                "format",
                "created"
            ]
        },
        "users_columns": {
            "list": [
                "id",
                "first_name",
                "last_name",
                "phone",
                "website",
                "telegram",
                "skype",
                "whatsapp",
                "balance",
                "spent",
                "status",
                "created",
                "last_auth",
                "discount",
                "custom_rates"
            ]
        },
        "export_format": [
            "csv"
        ],
        "currency": {
            "code": "USD",
            "sign": "$"
        },
        "status_list": {
            "0": "Pending",
            "1": "Processing",
            "2": "Finished",
            "3": "Deleted"
        },
        "users_status_list": {
            "0": "Pending",
            "1": "Processing",
            "2": "Finished",
            "3": "Deleted"
        }
    }
}


@router.get("/", dependencies=[Depends(get_panel_admin_hash)])
async def get_export_listing():
    return fixed_data
