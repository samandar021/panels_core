import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from migration_system.models.panel_models import PanelAdmin
from modules.cli.create_panel_admin.schemas import AdminCreate
from modules.security.hash_password import generate_salt, hash_password


async def create_admin(db: AsyncSession, admin_data: AdminCreate):
    salt = generate_salt()  # Генерация соли
    hashed_password = hash_password(admin_data.password, salt)

    now = datetime.datetime.now()
    timestamp = int(now.timestamp())

    new_admin = PanelAdmin(
        panel_id=admin_data.panel_id,
        email=admin_data.email,
        password=hashed_password,
        password_salt=salt,
        authorization_at=timestamp,  # Текущая дата и время
        status=1,  # 1 - Active
        created_at=timestamp,  # Текущая дата и время
        updated_at=timestamp,  # Текущая дата и время
        dark_mode=0,  # 0 - disabled
    )

    db.add(new_admin)
    await db.commit()
