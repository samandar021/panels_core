"""panels_db: init

Revision ID: bd6373d8fe77
Revises:
Create Date: 2023-08-14 14:25:59.175941

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'bd6373d8fe77'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'panel_admin_hash',
        sa.Column('panel_admin_id', sa.Integer(), nullable=False),
        sa.Column('hash', sa.String(length=128), nullable=True),
        sa.Column('rand_string', sa.String(length=128), nullable=True),
        sa.Column('ip', sa.Integer(), nullable=True),
        sa.Column('remember', sa.Integer(), nullable=True),
        sa.Column('super_user', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.Integer(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='panels',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_panels_panel_admin_hash_hash'), 'panel_admin_hash',
                    ['hash'], unique=False, schema='panels')
    op.create_index(op.f('ix_panels_panel_admin_hash_panel_admin_id'), 'panel_admin_hash',
                    ['panel_admin_id'], unique=False, schema='panels')
    op.create_table(
        'panels',
        sa.Column('domain', sa.String(length=1000), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.Column('expired_at', sa.Integer(), nullable=True),
        sa.Column('currency', sa.String(length=3), nullable=False),
        sa.Column('plan_id', sa.Integer(), nullable=False),
        sa.Column('db_name', sa.String(length=45), nullable=False),
        sa.Column('status', sa.String(length=45), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='panels',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_panels_panels_currency'), 'panels', ['currency'], unique=False, schema='panels')
    op.create_index(op.f('ix_panels_panels_plan_id'), 'panels', ['plan_id'], unique=False, schema='panels')
    op.create_index(op.f('ix_panels_panels_status'), 'panels', ['status'], unique=False, schema='panels')
    op.create_table('panel_admin',
                    sa.Column('panel_id', sa.Integer(), nullable=True),
                    sa.Column('panel_admin_hash_id', sa.Integer(), nullable=True),
                    sa.Column('username', sa.String(length=300), nullable=True),
                    sa.Column('email', sa.String(length=300), nullable=True),
                    sa.Column('password', sa.String(length=300), nullable=True),
                    sa.Column('password_salt', sa.String(length=300), nullable=True),
                    sa.Column('authorization_at', sa.Integer(), nullable=True),
                    sa.Column('status', sa.Integer(), nullable=True, comment='1 - Active, 2 - Suspended'),
                    sa.Column('created_at', sa.Integer(), nullable=True),
                    sa.Column('updated_at', sa.Integer(), nullable=True),
                    sa.Column('dark_mode', sa.Integer(), nullable=True, comment='0 - disabled, 1 - enabled'),
                    sa.Column('rules', sa.Text(collation='utf8mb4_general_ci'), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['panel_admin_hash_id'], ['panels.panel_admin_hash.id'],
                                            onupdate='NO ACTION', ondelete='NO ACTION'),
                    sa.ForeignKeyConstraint(['panel_id'], ['panels.panels.id'], onupdate='NO ACTION',
                                            ondelete='NO ACTION'),
                    sa.PrimaryKeyConstraint('id'),
                    schema='panels',
                    mysql_engine='InnoDB'
                    )
    op.create_index(op.f('ix_panels_panel_admin_panel_id'), 'panel_admin', ['panel_id'], unique=False, schema='panels')
    op.create_table('panel_domains',
                    sa.Column('panel_id', sa.Integer(), nullable=True),
                    sa.Column('domain', sa.String(length=300), nullable=True),
                    sa.Column('domain_type', sa.Integer(), nullable=True,
                              comment='Тип домена: 1 - основной, 2 - системный, 3 - дополнительный'),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['panel_id'], ['panels.panels.id'], onupdate='NO ACTION',
                                            ondelete='NO ACTION'),
                    sa.PrimaryKeyConstraint('id'),
                    schema='panels',
                    mysql_engine='InnoDB'
                    )
    op.create_index(op.f('ix_panels_panel_domains_domain'), 'panel_domains', ['domain'], unique=False, schema='panels')
    op.create_index(op.f('ix_panels_panel_domains_domain_type'), 'panel_domains', ['domain_type'], unique=True,
                    schema='panels')
    op.create_index(op.f('ix_panels_panel_domains_panel_id'), 'panel_domains', ['panel_id'], unique=False,
                    schema='panels')
    op.create_table('panel_options',
                    sa.Column('panel_id', sa.Integer(), nullable=True),
                    sa.Column('signup_page', sa.Integer(), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['panel_id'], ['panels.panels.id'], onupdate='NO ACTION',
                                            ondelete='NO ACTION'),
                    sa.PrimaryKeyConstraint('id'),
                    schema='panels',
                    mysql_engine='InnoDB'
                    )
    op.create_index(op.f('ix_panels_panel_options_panel_id'), 'panel_options', ['panel_id'], unique=False,
                    schema='panels')
    op.create_table('plan_list',
                    sa.Column('panel_id', sa.Integer(), nullable=True),
                    sa.Column('name', sa.String(length=45), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['panel_id'], ['panels.panels.id'], onupdate='NO ACTION',
                                            ondelete='NO ACTION'),
                    sa.PrimaryKeyConstraint('id'),
                    schema='panels',
                    mysql_engine='InnoDB'
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('plan_list', schema='panels')
    op.drop_table('panel_options', schema='panels')
    op.drop_table('panel_domains', schema='panels')
    op.drop_table('panel_admin', schema='panels')
    op.drop_table('panels', schema='panels')
    op.drop_table('panel_admin_hash', schema='panels')
    # ### end Alembic commands ###
