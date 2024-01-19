from typing import Any, Dict

from fastapi import APIRouter, Depends, Query

from panels_project.admin_dashboard.api.v1.auth.auth import get_panel_admin_hash

router = APIRouter()

fixed_data = {
    "status": "ok",
    "payloads": {
        "acces_rules": {
            "add_user": True,
            "edit_user": True,
            "change_status": True,
            "edit_discount": True,
            "export_users": True
        },
        "data": [
            {
                "id": 1,
                "first_name": "Vasiliy",
                "last_name": "Vasilek",
                "phone": "test.com",
                "website": "test.com",
                "telegram": "test.com",
                "skype": "test.com",
                "whatsapp": "test.com",
                "balance": "33.999",
                "spent": "22.322",
                "status": 1,
                "created": "2023-01-20",
                "last_auth": "2023-05-20",
                "discount": 20,
                "custom_rates": 0
            },
            {
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
            }
        ],
        "pages": {
            "current_page": "текущая страница",
            "row_per_page": "количество запись на страницу",
            "page_quantity": "количество страниц",
            "row_quantity": "количество записей"
        },
        "filter": {
            "search": "123",
            "status": 1
        },
        "columns": {
            "available": {
                "id": {
                    "sort": {
                        "is_active": "id_desc",
                        "asc": "id",
                        "desc": "id_desc"
                    },
                    "name": "ID"
                },
                "email": {
                    "sort": None,
                    "name": "Email"
                },
                "created": {
                    "sort": {
                        "is_active": False,
                        "asc": "created",
                        "desc": "created_desc"
                    },
                    "name": "Created"
                },
                "fields_block": {
                    "sort": False,
                    "name": "",
                    "fields": {
                        "first_name": False,
                        "last_name": False,
                        "phone": False,
                        "website": False,
                        "telegram": False,
                        "skype": False,
                        "whatsapp": False
                    }
                },
            },
            "list": [
                "id",
                "first_name",
                "last_name",
                "created",
                "last_auth"
            ]
        },
        "currency": {
            "code": "USD",
            "sign": "$"
        },
        "status_list": {
            "0": "Active",
            "1": "Suspended",
            "2": "Unconfirmed"
        }
    }
}


@router.get("/", dependencies=[Depends(get_panel_admin_hash)])
async def get_user_listing(search: str = Query(None, description="Строка поиска"),
                           status: int = Query(None, description="Фильтрация с учетом статуса пользователя"),
                           page: int = Query(1, description="Номер страницы для отображения"),
                           page_quantity: int = Query(100, description="Количество записей на страницу"),
                           sort: str = Query(None, description="Ключ направления сортировки"),
                           ) -> Dict[str, Any]:
    return fixed_data
