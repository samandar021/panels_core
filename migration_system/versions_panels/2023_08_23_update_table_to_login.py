"""update table to login

Revision ID: cc5ea8669413
Revises: 56322c69e67d
Create Date: 2023-08-23 10:21:50.566851

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'cc5ea8669413'
down_revision: Union[str, None] = '56322c69e67d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('panel_admin', sa.Column('lastip', sa.String(length=15), nullable=True))
    op.add_column('panel_admin_hash', sa.Column('is_2fa_step', sa.Boolean(), nullable=True))
    op.drop_constraint('panel_admin_ibfk_1', 'panel_admin', type_='foreignkey')
    op.drop_column('panel_admin', 'panel_admin_hash_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('panel_admin_hash', 'is_2fa_step')
    op.create_foreign_key('panel_admin_ibfk_1', 'panel_admin', 'panel_admin_hash', ['panel_admin_hash_id'], ['id'])
    op.add_column('panel_admin', sa.Column('panel_admin_hash_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('panel_admin', 'lastip')
    # ### end Alembic commands ###
