from fastapi import APIRouter, Depends

from panels_project.admin_dashboard.api.v1.auth.auth import get_panel_admin_hash

router = APIRouter()

fixed_response = {
    "status": "ok",
    "payloads": {
        "min_service_rate": 0.0001,
        "rates": [
            {
                "service_id": 1,
                "rate": 0.1,
                "is_percent": False
            },
            {
                "service_id": 1,
                "rate": 10,
                "is_percent": False
            },
            {
                "service_id": 1,
                "rate": 3,
                "is_percent": True
            }
        ],
        "services": [
            {
                "service_id": "1",
                "category_id": ["1", "2"],
                "name": "Likes",
                "rate": "0.01"
            },
            {
                "service_id": "2",
                "category_id": ["1", "2", "3"],
                "name": "Followers",
                "rate": "0.02"
            }
        ],
        "categories": [
            {
                "category_id": 1,
                "name": "Likes"
            },
            {
                "category_id": 1,
                "name": "Followers"
            }
        ]
    }
}


@router.get("/", dependencies=[Depends(get_panel_admin_hash)])
async def get_custom_rates(user_id: int):
    return fixed_response
