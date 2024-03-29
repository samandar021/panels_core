"""update panels.panel_domains

Revision ID: c501b8c24276
Revises: 29395c63c6c9
Create Date: 2023-08-29 15:58:32.594780

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'c501b8c24276'
down_revision: Union[str, None] = '29395c63c6c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('panel_domains', 'domain_type')
    op.drop_column('panel_domains', 'domain')
    op.add_column('panel_domains', sa.Column('domain', sa.String(length=300), nullable=True))
    op.add_column('panel_domains', sa.Column('domain_type', sa.Integer(), nullable=True, comment='Тип домена: 1 - основной, 2 - системный, 3 - дополнительный'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('panel_domains', 'domain_type')
    op.drop_column('panel_domains', 'domain')
    op.add_column('panel_domains', sa.Column('domain', mysql.VARCHAR(length=300), nullable=True))
    op.add_column('panel_domains', sa.Column('domain_type', mysql.INTEGER(), autoincrement=False, nullable=True, comment='Тип домена: 1 - основной, 2 - системный, 3 - дополнительный'))
    # ### end Alembic commands ###
