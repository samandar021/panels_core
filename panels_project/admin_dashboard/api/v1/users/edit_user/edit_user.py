from fastapi import APIRouter, Depends

from panels_project.admin_dashboard.api.v1.auth.auth import get_panel_admin_hash

from .request_shemas import EditUserRequest

router = APIRouter()

fixed_response = {
    "status": "ok",
    "payloads": {
        "table": {},
        "pages": {
            "current_page": "",  # текущая страница
            "row_per_page": "",  # количество запись на страницу
            "page_quantity": "",  # количество страниц
            "row_quantity": ""  # количество записей
        },
        "sort": {

        },
        "columps": {

        },
        "statuses": {

        }
    }
}


@router.post("/", dependencies=[Depends(get_panel_admin_hash)])
async def edit_user(request_data: EditUserRequest):
    return fixed_response
