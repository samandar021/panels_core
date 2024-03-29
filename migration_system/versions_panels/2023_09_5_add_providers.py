"""add_providers

Revision ID: 30c83ac873fc
Revises: 3814535d0f9e
Create Date: 2023-09-05 14:09:05.305151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '30c83ac873fc'
down_revision: Union[str, None] = '3814535d0f9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('providers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=300), nullable=False),
    sa.Column('domain', sa.String(length=300), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.Column('settings_form', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('domain'),
    schema='panels',
    mysql_engine='InnoDB'
    )
    op.create_table('panel_provider_apikey_log',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('panel_id', sa.Integer(), nullable=False),
    sa.Column('provider_id', sa.Integer(), nullable=False),
    sa.Column('auth_field_1', sa.String(length=256), nullable=True),
    sa.Column('auth_field_2', sa.String(length=256), nullable=True),
    sa.Column('auth_field_3', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['panel_id'], ['panels.panels.id'], onupdate='NO ACTION', ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['provider_id'], ['panels.providers.id'], onupdate='NO ACTION', ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('id'),
    schema='panels',
    mysql_engine='InnoDB'
    )
    op.create_table('panel_provider_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('panel_id', sa.Integer(), nullable=False),
    sa.Column('string', sa.String(length=256), nullable=True),
    sa.Column('has_found', sa.Integer(), nullable=True, comment='0 - No, 1 - Yes'),
    sa.Column('created_at', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['panel_id'], ['panels.panels.id'], onupdate='NO ACTION', ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('id'),
    schema='panels',
    mysql_engine='InnoDB'
    )
    op.create_table('panel_providers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('panel_id', sa.Integer(), nullable=False),
    sa.Column('provider_id', sa.Integer(), nullable=False),
    sa.Column('auth_field_1', sa.String(length=256), nullable=True),
    sa.Column('auth_field_2', sa.String(length=256), nullable=True),
    sa.Column('auth_field_3', sa.String(length=256), nullable=True),
    sa.Column('created_at', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['panel_id'], ['panels.panels.id'], onupdate='NO ACTION', ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['provider_id'], ['panels.providers.id'], onupdate='NO ACTION', ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('id'),
    schema='panels',
    mysql_engine='InnoDB'
    )
    op.drop_constraint('panel_admin_ibfk_1', 'panel_admin', type_='foreignkey')
    op.create_foreign_key(None, 'panel_admin', 'panels', ['panel_id'], ['id'], source_schema='panels', referent_schema='panels', onupdate='NO ACTION', ondelete='NO ACTION')
    op.drop_constraint('panel_admin_auth_codes_ibfk_2', 'panel_admin_auth_codes', type_='foreignkey')
    op.drop_constraint('panel_admin_auth_codes_ibfk_1', 'panel_admin_auth_codes', type_='foreignkey')
    op.create_foreign_key(None, 'panel_admin_auth_codes', 'panel_admin', ['panel_admin_id'], ['id'], source_schema='panels', referent_schema='panels', onupdate='NO ACTION', ondelete='NO ACTION')
    op.create_foreign_key(None, 'panel_admin_auth_codes', 'panel_admin_hash', ['panel_admin_hash_id'], ['id'], source_schema='panels', referent_schema='panels', onupdate='NO ACTION', ondelete='NO ACTION')
    op.drop_constraint('panel_domains_ibfk_1', 'panel_domains', type_='foreignkey')
    op.create_foreign_key(None, 'panel_domains', 'panels', ['panel_id'], ['id'], source_schema='panels', referent_schema='panels', onupdate='NO ACTION', ondelete='NO ACTION')
    op.drop_constraint('panel_options_ibfk_1', 'panel_options', type_='foreignkey')
    op.create_foreign_key(None, 'panel_options', 'panels', ['panel_id'], ['id'], source_schema='panels', referent_schema='panels', onupdate='NO ACTION', ondelete='NO ACTION')
    op.drop_constraint('panel_payment_methods_ibfk_3', 'panel_payment_methods', type_='foreignkey')
    op.drop_constraint('panel_payment_methods_ibfk_1', 'panel_payment_methods', type_='foreignkey')
    op.drop_constraint('panel_payment_methods_ibfk_2', 'panel_payment_methods', type_='foreignkey')
    op.create_foreign_key(None, 'panel_payment_methods', 'payment_methods_currencies', ['currency_id'], ['id'], source_schema='panels', referent_schema='panels', onupdate='NO ACTION', ondelete='NO ACTION')
    op.create_foreign_key(None, 'panel_payment_methods', 'panels', ['panel_id'], ['id'], source_schema='panels', referent_schema='panels', onupdate='NO ACTION', ondelete='NO ACTION')
    op.create_foreign_key(None, 'panel_payment_methods', 'payment_methods', ['method_id'], ['id'], source_schema='panels', referent_schema='panels', onupdate='NO ACTION', ondelete='NO ACTION')
    op.drop_constraint('panel_payment_methods_bonuses_ibfk_1', 'panel_payment_methods_bonuses', type_='foreignkey')
    op.create_foreign_key(None, 'panel_payment_methods_bonuses', 'panel_payment_methods', ['panel_payment_methods_id'], ['id'], source_schema='panels', referent_schema='panels', onupdate='NO ACTION', ondelete='NO ACTION')
    op.drop_constraint('panel_payment_methods_options_ibfk_1', 'panel_payment_methods_options', type_='foreignkey')
    op.create_foreign_key(None, 'panel_payment_methods_options', 'panel_payment_methods', ['panel_payment_methods_id'], ['id'], source_schema='panels', referent_schema='panels', onupdate='NO ACTION', ondelete='NO ACTION')
    op.drop_constraint('payment_methods_currencies_ibfk_1', 'payment_methods_currencies', type_='foreignkey')
    op.create_foreign_key(None, 'payment_methods_currencies', 'payment_methods', ['method_id'], ['id'], source_schema='panels', referent_schema='panels', onupdate='NO ACTION', ondelete='NO ACTION')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'payment_methods_currencies', schema='panels', type_='foreignkey')
    op.create_foreign_key('payment_methods_currencies_ibfk_1', 'payment_methods_currencies', 'payment_methods', ['method_id'], ['id'])
    op.drop_constraint(None, 'panel_payment_methods_options', schema='panels', type_='foreignkey')
    op.create_foreign_key('panel_payment_methods_options_ibfk_1', 'panel_payment_methods_options', 'panel_payment_methods', ['panel_payment_methods_id'], ['id'])
    op.drop_constraint(None, 'panel_payment_methods_bonuses', schema='panels', type_='foreignkey')
    op.create_foreign_key('panel_payment_methods_bonuses_ibfk_1', 'panel_payment_methods_bonuses', 'panel_payment_methods', ['panel_payment_methods_id'], ['id'])
    op.drop_constraint(None, 'panel_payment_methods', schema='panels', type_='foreignkey')
    op.drop_constraint(None, 'panel_payment_methods', schema='panels', type_='foreignkey')
    op.drop_constraint(None, 'panel_payment_methods', schema='panels', type_='foreignkey')
    op.create_foreign_key('panel_payment_methods_ibfk_2', 'panel_payment_methods', 'payment_methods_currencies', ['currency_id'], ['id'])
    op.create_foreign_key('panel_payment_methods_ibfk_1', 'panel_payment_methods', 'payment_methods', ['method_id'], ['id'])
    op.create_foreign_key('panel_payment_methods_ibfk_3', 'panel_payment_methods', 'panels', ['panel_id'], ['id'])
    op.drop_constraint(None, 'panel_options', schema='panels', type_='foreignkey')
    op.create_foreign_key('panel_options_ibfk_1', 'panel_options', 'panels', ['panel_id'], ['id'])
    op.drop_constraint(None, 'panel_domains', schema='panels', type_='foreignkey')
    op.create_foreign_key('panel_domains_ibfk_1', 'panel_domains', 'panels', ['panel_id'], ['id'])
    op.drop_constraint(None, 'panel_admin_auth_codes', schema='panels', type_='foreignkey')
    op.drop_constraint(None, 'panel_admin_auth_codes', schema='panels', type_='foreignkey')
    op.create_foreign_key('panel_admin_auth_codes_ibfk_1', 'panel_admin_auth_codes', 'panel_admin', ['panel_admin_id'], ['id'])
    op.create_foreign_key('panel_admin_auth_codes_ibfk_2', 'panel_admin_auth_codes', 'panel_admin_hash', ['panel_admin_hash_id'], ['id'])
    op.drop_constraint(None, 'panel_admin', schema='panels', type_='foreignkey')
    op.create_foreign_key('panel_admin_ibfk_1', 'panel_admin', 'panels', ['panel_id'], ['id'])
    op.drop_table('panel_providers', schema='panels')
    op.drop_table('panel_provider_history', schema='panels')
    op.drop_table('panel_provider_apikey_log', schema='panels')
    op.drop_table('providers', schema='panels')
    # ### end Alembic commands ###
