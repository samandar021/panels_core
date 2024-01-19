import json
from datetime import datetime
from ipaddress import ip_address
from typing import AsyncGenerator

from fastapi import Depends, Request
from sqlalchemy.orm import sessionmaker

from migration_system.models.panel_template_models import ActivityLog, ActivityLogDetails
from modules.connect_to_database.get_session_panel_db import get_session_panel_db
from modules.helper.abstract_helper import AbstractHelper
from modules.helper.panels_helper import PanelsHelper


class ActivityLogHelper(AbstractHelper):

    async def create_activity_log_and_activity_log_details(
        self,
        request: Request,
        panels_helper: PanelsHelper,
        panel_admin_obj_id: int,
        panel_admin_hash_obj_super_admin: int,
        mass_actions: bool = False
    ) -> None:
        """
        Создать объект panel_template.activity_log и panel_template.activity_log_details
        Для массовых действий нужен аргумент mass_actions = True
        """
        activity_log_obj = await self.create_activity_log(
            request,
            panels_helper,
            panel_admin_obj_id,
            panel_admin_hash_obj_super_admin
        )
        if mass_actions is False:
            await self.create_activity_log_details(request, activity_log_obj.id)

    async def create_activity_log(
        self,
        request: Request,
        panels_helper: PanelsHelper,
        panel_admin_id: int,
        super_admin: int,
        event_id: int = 0,
        details_id: int = 0,
        created_at: int = int(datetime.now().timestamp())
    ) -> ActivityLog:
        """Создать объект panel_template.activity_log"""
        user_agent = request.headers.get('user-agent')
        user_agent_list_obj = await panels_helper.get_or_create_user_agent_list(user_agent)
        activity_log_obj = ActivityLog(
            panel_admin_id=panel_admin_id,
            user_agent_id=user_agent_list_obj.id,
            ip=str(ip_address(request.client.host)),  # type: ignore
            url=str(request.url),
            event_id=event_id,
            super_admin=super_admin,
            details_id=details_id,
            created_at=created_at,
        )
        self.session.add(activity_log_obj)
        await self.session.commit()
        await self.session.refresh(activity_log_obj)
        return activity_log_obj

    async def create_activity_log_details(self, request: Request, activity_log_id: int) -> None:
        """Создать объект panel_template.activity_log_details"""
        request_data = {
            'query_params': {k: v for k, v in request.query_params.items()},
            'body': json.loads(await request.body()),
            'headers': {k: v for k, v in request.headers.items()},
            'cookies': {k: v for k, v in request.cookies.items()},
            'url': str(request.url)
        }
        request_data_json = json.dumps(request_data)
        activity_log_details = ActivityLogDetails(
            activity_log_details_id=activity_log_id,
            request_data=request_data_json,
        )
        self.session.add(activity_log_details)
        await self.session.commit()


async def get_activity_log_helper(
    async_session: sessionmaker = Depends(get_session_panel_db)
) -> AsyncGenerator:
    async with async_session() as session:
        yield ActivityLogHelper(session)
