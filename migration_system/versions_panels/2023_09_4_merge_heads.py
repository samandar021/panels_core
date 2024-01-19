"""merge heads

Revision ID: 3814535d0f9e
Revises: 1a6dee8ead45, 20dc4e8ae15a
Create Date: 2023-09-04 19:20:20.014525

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3814535d0f9e'
down_revision: Union[str, None] = ('1a6dee8ead45', '20dc4e8ae15a')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
