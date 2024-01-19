import hmac
from base64 import b64encode
from datetime import datetime
from hashlib import sha256
from ipaddress import ip_address
from os import urandom
from random import randrange
from typing import AsyncGenerator

from fastapi import Depends, Request
from sqlalchemy import and_, delete, join, or_, select
from sqlalchemy.orm import sessionmaker

from migration_system.models.panel_models import (PanelAdmin, PanelAdminAuthCodes, PanelAdminHash, PanelDomains, Panels,
                                                  UserAgentList)
from modules.connect_to_database.database import get_session_panels_db
from modules.helper.abstract_helper import AbstractHelper
from panels_project.admin_dashboard.api.v1.auth.response_shemas import PanelAdminRules

STATUS_ACTIVE = 1
STATUS_LOCKED = 2


class PanelsHelper(AbstractHelper):

    async def get_panels_domain(self, domain: str) -> PanelDomains | None:
        """Получить объект panels.panel_domains по домену."""
        panel_domains = await self.session.execute(
            select(PanelDomains).where(PanelDomains.domain == domain)
        )
        return panel_domains.scalars().first()

    async def get_panels(self, panels_id: int) -> Panels | None:
        """Получить объект panels.panels по id."""
        panels = await self.session.execute(
            select(Panels).where(Panels.id == panels_id)
        )
        return panels.scalars().first()

    async def get_panel_by_domain(self, domain: str) -> Panels | None:
        # Сначала ищем запись в Panels, которая соответствует заданному домену
        db_query_find_panel = select(Panels.id).where(
            and_(
                Panels.domain == domain,
                or_(Panels.status == STATUS_ACTIVE, Panels.status == STATUS_LOCKED),
                Panels.db_name.isnot(None)
            )
        )
        result_find_panel = await self.session.execute(db_query_find_panel)
        panel_id = result_find_panel.scalar_one_or_none()

        if panel_id is None:
            return None

        # Делаем JOIN между Panels и PanelDomains на основе найденного panel_id
        db_query = select(Panels, PanelDomains).select_from(
            join(Panels, PanelDomains, Panels.id == PanelDomains.panel_id)
        ).where(
            and_(
                Panels.id == panel_id,
                or_(Panels.status == STATUS_ACTIVE, Panels.status == STATUS_LOCKED),
                Panels.db_name.isnot(None),
                PanelDomains.domain.isnot(None)
            )
        )

        result = await self.session.execute(db_query)

        return result.scalars().first()

    async def get_panel_admin_by_id(self, panel_admin_id: int) -> PanelAdmin | None:
        """Получить объект panels.panel_admin по id."""
        panel_admin_obj = await self.session.execute(
            select(
                PanelAdmin
            ).where(
                PanelAdmin.id == panel_admin_id
            )
        )
        return panel_admin_obj.scalars().first()

    async def get_panel_admin_by_email(self, email: str) -> PanelAdmin | None:
        """Получить объект panels.panel_admin по email."""
        panel_admin_obj = await self.session.execute(
            select(
                PanelAdmin
            ).where(
                PanelAdmin.email == email
            )
        )
        return panel_admin_obj.scalars().first()

    async def update_panel_admin_obj__lastip(self, panel_admin_obj: PanelAdmin, request: Request) -> None:
        """Изменение panels.panel_admin lastip."""
        panel_admin_obj.lastip = str(ip_address(request.client.host))  # type: ignore
        await self.session.commit()

    async def get_panel_admin_hash_obj_by_id(self, panel_admin_id: int) -> PanelAdminHash | None:
        """Получить объект panels.panel_admin_hash по panel_admin_id."""
        panel_admin_hash_obj = await self.session.execute(
            select(
                PanelAdminHash
            ).where(
                PanelAdminHash.panel_admin_id == panel_admin_id
            )
        )
        return panel_admin_hash_obj.scalars().first()

    async def get_panel_admin_hash_obj_by_hash(self, hash: str) -> PanelAdminHash | None:
        """Получить объект panels.panel_admin_hash по hash."""
        panel_admin_hash_obj = await self.session.execute(
            select(
                PanelAdminHash
            ).where(
                PanelAdminHash.hash == hash
            )
        )
        return panel_admin_hash_obj.scalars().first()

    async def update_panel_admin_hash_obj(self, panel_admin_hash_obj: PanelAdminHash, is_2fa_step: bool) -> None:
        """Изменение panels.panel_admin_hash is_2fa_step."""
        panel_admin_hash_obj.is_2fa_step = is_2fa_step
        await self.session.commit()

    @staticmethod
    async def generate_hash(panel_admin_obj: PanelAdmin, rand_string: bytes) -> str:
        string_to_hash = str(panel_admin_obj.panel_id) + panel_admin_obj.email + panel_admin_obj.password
        hash_ = hmac.new(rand_string, string_to_hash.encode(), sha256).hexdigest()
        return hash_

    async def create_panel_admin_hash_obj(
            self,
            panel_admin_obj: PanelAdmin,
            request: Request,
            remember: bool,
            is_2fa_step: int,
            super_admin: bool = False,
            created_at: int = int(datetime.now().timestamp()),
            updated_at: int = int(datetime.now().timestamp())
    ) -> PanelAdminHash:
        """Создать объект panels.panel_admin_hash."""
        rand_string = urandom(16)
        hash_ = await self.generate_hash(panel_admin_obj, rand_string)
        rand_string_to_model = b64encode(rand_string).decode('utf-8')

        panel_admin_hash_obj = PanelAdminHash(
            panel_admin_id=panel_admin_obj.id,
            hash=hash_,
            rand_string=rand_string_to_model,
            ip=str(ip_address(request.client.host)),  # type: ignore
            remember=remember,
            is_2fa_step=bool(is_2fa_step),
            super_admin=super_admin,
            created_at=created_at,
            updated_at=updated_at
        )
        self.session.add(panel_admin_hash_obj)
        await self.session.commit()
        await self.session.refresh(panel_admin_hash_obj)
        return panel_admin_hash_obj

    async def delete_panel_admin_hash_obj(self, panel_admin_hash_id: int) -> None:
        """Удалить объект panels.panel_admin_hash по id."""
        await self.session.execute(
            delete(
                PanelAdminHash
            ).where(
                PanelAdminHash.id == panel_admin_hash_id
            )
        )
        await self.session.commit()

    async def get_permission(self, panel_admin_id: int, key: str) -> bool | None:
        """Получить разрешения к разделу для администратора по ключу"""
        panel_admin_obj = await self.get_panel_admin_by_id(panel_admin_id)
        if panel_admin_obj is None:
            return None

        permission_json = PanelAdminRules(**panel_admin_obj.rules)
        if key not in dir(permission_json):
            return False
        permission = getattr(permission_json, key)
        return permission

    async def get_all_permission(self, panel_admin_id: int) -> PanelAdminRules | None:
        """Получить разрешения для администратора"""
        panel_admin_obj = await self.get_panel_admin_by_id(panel_admin_id)
        if panel_admin_obj is None:
            return None

        permission_json = PanelAdminRules(**panel_admin_obj.rules)
        return permission_json

    async def get_or_create_user_agent_list(self, user_agent: str | None) -> UserAgentList:
        """Получить или создать panels.user_agent_list"""
        user_agent_list_select = await self.session.execute(
            select(
                UserAgentList
            ).where(
                UserAgentList.user_agent_name == user_agent
            )
        )
        user_agent_list_obj = user_agent_list_select.scalars().first()
        if user_agent_list_obj is not None:
            return user_agent_list_obj
        user_agent_list_obj = UserAgentList(user_agent_name=user_agent)
        self.session.add(user_agent_list_obj)
        await self.session.commit()
        await self.session.refresh(user_agent_list_obj)
        return user_agent_list_obj

    async def get_panel_admin_auth_code_by_panel_admin_hash_id(
            self,
            panel_admin_hash_id: int
    ) -> PanelAdminAuthCodes | None:
        """Получить объект panels.panel_admin_auth_codes по panel_admin_hash_id."""
        panel_admin_auth_code_obj = await self.session.execute(
            select(
                PanelAdminAuthCodes
            ).where(
                PanelAdminAuthCodes.panel_admin_hash_id == panel_admin_hash_id
            )
        )
        return panel_admin_auth_code_obj.one()[0]

    async def create_panel_admin_auth_code_obj(
            self,
            panel_admin_id: int,
            panel_admin_hash_id: int,
            auth_code: int = randrange(100_000, 999_999),
            attempts: int = 0,
            created_at: int = int(datetime.now().timestamp())
    ) -> None:
        """Создать объект panels.panel_admin_auth_codes."""
        panel_admin_auth_code_obj = PanelAdminAuthCodes(
            panel_admin_id=panel_admin_id,
            panel_admin_hash_id=panel_admin_hash_id,
            auth_code=auth_code,
            attempts=attempts,
            created_at=created_at
        )
        self.session.add(panel_admin_auth_code_obj)
        await self.session.commit()

    async def update_panel_admin_auth_code__attempts(
            self,
            panel_admin_auth_code_obj: PanelAdminAuthCodes,
            attempts: int
    ) -> None:
        """Изменение panels.panel_admin_auth_codes attempts."""
        panel_admin_auth_code_obj.attempts = attempts
        await self.session.commit()

    async def update_panel_admin_auth_code__created_at_and_code(
            self,
            panel_admin_auth_code_obj: PanelAdminAuthCodes,
            auth_code: int = randrange(100_000, 999_999),
            created_at: int = int(datetime.now().timestamp())
    ) -> None:
        """Изменение panels.panel_admin_auth_codes auth_code и created_at."""
        while True:
            if auth_code != panel_admin_auth_code_obj.auth_code:
                break
            auth_code = randrange(100_000, 999_999)
        panel_admin_auth_code_obj.auth_code = auth_code
        panel_admin_auth_code_obj.created_at = created_at
        await self.session.commit()

    async def delete_panel_admin_auth_code_obj(self, panel_admin_hash_id: int) -> None:
        """Удалить объект panels.panel_admin_auth_codes по panel_admin_hash_id."""
        await self.session.execute(
            delete(
                PanelAdminAuthCodes
            ).where(
                PanelAdminAuthCodes.panel_admin_hash_id == panel_admin_hash_id
            )
        )
        await self.session.commit()


async def get_panels_helper(async_session: sessionmaker = Depends(get_session_panels_db)) -> AsyncGenerator:
    async with async_session() as session:
        yield PanelsHelper(session)
