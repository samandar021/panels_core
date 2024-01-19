"""update tables to login

Revision ID: f74a9c290eef
Revises: 6b3377701017
Create Date: 2023-08-23 11:16:27.195033

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f74a9c290eef'
down_revision: Union[str, None] = '6b3377701017'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=300), nullable=True),
        sa.Column('refferer_id', sa.Integer(), nullable=True),
        sa.Column('password', sa.String(length=300), nullable=True),
        sa.Column('password_salt', sa.String(length=300), nullable=True),
        sa.Column('password_method', sa.Integer(), nullable=True),
        sa.Column('balance', sa.DECIMAL(precision=21, scale=7), nullable=True),
        sa.Column('spent', sa.DECIMAL(precision=21, scale=7), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.Integer(), nullable=True),
        sa.Column('auth_at', sa.Integer(), nullable=True),
        sa.Column('auth_ip', sa.Integer(), nullable=True),
        sa.Column('apikey', sa.String(length=64), nullable=True),
        sa.Column('refferal_key', sa.String(length=8), nullable=True),
        sa.Column('discount', sa.Integer(), nullable=True),
        sa.Column('timezone', sa.Integer(), nullable=True),
        sa.Column('terms_confirm', sa.Integer(), nullable=True),
        sa.Column('lang_code', sa.String(length=2), nullable=True),
        sa.Column('email_status', sa.Integer(), nullable=True, comment='0 - not confirmed, 1 - confirmed'),
        sa.Column('status', sa.Integer(), nullable=True, comment='1 - active, 2 - suspended'),
        sa.Column('custom_variables', sa.JSON(), nullable=True),
        sa.Column('currency', sa.String(length=3), nullable=True),
        sa.Column('has_subscription', sa.Integer(), nullable=True),
        sa.Column('has_drip_feed', sa.Integer(), nullable=True),
        sa.Column('has_ticket', sa.Integer(), nullable=True),
        sa.Column('has_refill_task', sa.Integer(), nullable=True),
        sa.Column('custom_rates_quantity', sa.Integer(), nullable=True),
        sa.Column('confirmed', sa.Integer(), nullable=True),
        sa.Column('cpf_field', sa.String(length=200), nullable=True),
        sa.Column('two_fa_enabled', sa.Integer(), nullable=True),
        sa.Column('two_fa_generated_at', sa.Integer(), nullable=True),
        sa.Column('two_fa_generate_blocked', sa.Integer(), nullable=True),
        sa.Column('resend_email_at', sa.Integer(), nullable=True),
        sa.Column('change_email_at', sa.Integer(), nullable=True),
        sa.Column('orders_count', sa.Integer(), nullable=True),
        sa.Column('apikey_updated_at', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('refferal_key'),
        schema='panel_first_domain',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'user_custom_fields',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('default_field_id', sa.Integer(), nullable=True),
        sa.Column('position', sa.Integer(), nullable=True),
        sa.Column('rules', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='NO ACTION', ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_first_domain',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_panel_first_domain_user_custom_fields_user_id'), 'user_custom_fields',
                    ['user_id'], unique=False, schema='panel_first_domain')
    op.create_table(
        'user_details',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('field_name', sa.String(length=300), nullable=True),
        sa.Column('field_value', sa.String(length=300), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='NO ACTION', ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_first_domain',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_panel_first_domain_user_details_user_id'), 'user_details',
                    ['user_id'], unique=False, schema='panel_first_domain')
    op.create_table(
        'users_activity_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('user_agent_id', sa.Integer(), nullable=True),
        sa.Column('ip', sa.Integer(), nullable=True),
        sa.Column('event', sa.Integer(), nullable=True),
        sa.Column('location', sa.String(length=1000), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_agent_id'], ['panels.user_agent_list.id'], onupdate='NO ACTION',
                                ondelete='NO ACTION'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='NO ACTION', ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_first_domain',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_panel_first_domain_users_activity_log_user_agent_id'), 'users_activity_log',
                    ['user_agent_id'], unique=False, schema='panel_first_domain')
    op.create_index(op.f('ix_panel_first_domain_users_activity_log_user_id'), 'users_activity_log',
                    ['user_id'], unique=False, schema='panel_first_domain')
    op.create_table(
        'users_apikey_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('apikey', sa.String(length=128), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='NO ACTION', ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_first_domain',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_panel_first_domain_users_apikey_history_user_id'), 'users_apikey_history',
                    ['user_id'], unique=False, schema='panel_first_domain')
    op.create_table(
        'users_auth_codes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('event', sa.String(length=45), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='NO ACTION', ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_first_domain',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_panel_first_domain_users_auth_codes_user_id'), 'users_auth_codes',
                    ['user_id'], unique=False, schema='panel_first_domain')
    op.create_table(
        'users_custom_rates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('service_id', sa.Integer(), nullable=True),
        sa.Column('rate', sa.DECIMAL(precision=21, scale=4), nullable=True),
        sa.Column('is_percent', sa.Integer(), nullable=True,
                  comment='0 - fixed service rate, 1 - percent  of service rate'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='NO ACTION', ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_first_domain',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_panel_first_domain_users_custom_rates_service_id'), 'users_custom_rates',
                    ['service_id'], unique=False, schema='panel_first_domain')
    op.create_index(op.f('ix_panel_first_domain_users_custom_rates_user_id'), 'users_custom_rates',
                    ['user_id'], unique=False, schema='panel_first_domain')
    op.create_table(
        'users_password_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('password', sa.String(length=300), nullable=True),
        sa.Column('password_salt', sa.String(length=300), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='NO ACTION', ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_first_domain',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_panel_first_domain_users_password_history_user_id'), 'users_password_history',
                    ['user_id'], unique=False, schema='panel_first_domain')
    op.create_table(
        'admin_auth_codes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('panel_admin_id', sa.Integer(), nullable=True),
        sa.Column('panel_admin_hash_id', sa.Integer(), nullable=True),
        sa.Column('auth_code', sa.Integer(), nullable=True),
        sa.Column('attempts', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['panel_admin_hash_id'], ['panels.panel_admin_hash.id'],
                                onupdate='NO ACTION', ondelete='NO ACTION'),
        sa.ForeignKeyConstraint(['panel_admin_id'], ['panels.panel_admin.id'],
                                onupdate='NO ACTION', ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_admin_auth_codes_panel_admin_hash_id'), 'admin_auth_codes',
                    ['panel_admin_hash_id'], unique=False)
    op.create_index(op.f('ix_admin_auth_codes_panel_admin_id'), 'admin_auth_codes',
                    ['panel_admin_id'], unique=False)
    op.create_table(
        'activity_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('panel_admin_id', sa.Integer(), nullable=True),
        sa.Column('user_agent_id', sa.Integer(), nullable=True),
        sa.Column('super_admin', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.Column('ip', sa.Integer(), nullable=True),
        sa.Column('details_id', sa.Integer(), nullable=True),
        sa.Column('url', sa.String(length=1000), nullable=True),
        sa.Column('event_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['panel_admin_id'], ['panels.panel_admin.id'], onupdate='NO ACTION',
                                ondelete='NO ACTION'),
        sa.ForeignKeyConstraint(['user_agent_id'], ['panels.user_agent_list.id'], onupdate='NO ACTION',
                                ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_first_domain',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_panel_first_domain_activity_log_panel_admin_id'), 'activity_log',
                    ['panel_admin_id'], unique=False, schema='panel_first_domain')
    op.create_index(op.f('ix_panel_first_domain_activity_log_user_agent_id'), 'activity_log',
                    ['user_agent_id'], unique=False, schema='panel_first_domain')
    op.create_table(
        'admin_auth_codes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('panel_admin_id', sa.Integer(), nullable=True),
        sa.Column('panel_admin_hash_id', sa.Integer(), nullable=True),
        sa.Column('auth_code', sa.Integer(), nullable=True),
        sa.Column('attempts', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['panel_admin_hash_id'], ['panels.panel_admin_hash.id'], onupdate='NO ACTION',
                                ondelete='NO ACTION'),
        sa.ForeignKeyConstraint(['panel_admin_id'], ['panels.panel_admin.id'], onupdate='NO ACTION',
                                ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_first_domain',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_panel_first_domain_admin_auth_codes_panel_admin_hash_id'), 'admin_auth_codes',
                    ['panel_admin_hash_id'], unique=False, schema='panel_first_domain')
    op.create_index(op.f('ix_panel_first_domain_admin_auth_codes_panel_admin_id'), 'admin_auth_codes',
                    ['panel_admin_id'], unique=False, schema='panel_first_domain')
    op.create_table(
        'activity_log_details',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('request_data', sa.Text(), nullable=True),
        sa.Column('activity_log_details_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['activity_log_details_id'], ['activity_log.id'], onupdate='NO ACTION',
                                ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_first_domain',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'payment_methods_translations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('panel_payment_methods_id', sa.Integer(), nullable=True),
        sa.Column('lang_code', sa.String(length=2), nullable=True),
        sa.Column('name', sa.String(length=50), nullable=True),
        sa.Column('descriptions', sa.String(length=200), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['panel_payment_methods_id'], ['panels.panel_payment_methods.id'],
                                onupdate='NO ACTION', ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_first_domain',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'user_payment_methods',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('panel_payment_method_id', sa.Integer(), nullable=True),
        sa.Column('is_enabled', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['panel_payment_method_id'], ['panels.panel_payment_methods.id'],
                                onupdate='NO ACTION', ondelete='NO ACTION'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='NO ACTION', ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_first_domain',
        mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_payment_methods', schema='panel_first_domain')
    op.drop_table('payment_methods_translations', schema='panel_first_domain')
    op.drop_table('activity_log_details', schema='panel_first_domain')
    op.drop_index(op.f('ix_panel_first_domain_admin_auth_codes_panel_admin_id'), table_name='admin_auth_codes',
                  schema='panel_first_domain')
    op.drop_index(op.f('ix_panel_first_domain_admin_auth_codes_panel_admin_hash_id'), table_name='admin_auth_codes',
                  schema='panel_first_domain')
    op.drop_table('admin_auth_codes', schema='panel_first_domain')
    op.drop_index(op.f('ix_panel_first_domain_activity_log_user_agent_id'), table_name='activity_log',
                  schema='panel_first_domain')
    op.drop_index(op.f('ix_panel_first_domain_activity_log_panel_admin_id'), table_name='activity_log',
                  schema='panel_first_domain')
    op.drop_table('activity_log', schema='panel_first_domain')
    op.drop_index(op.f('ix_admin_auth_codes_panel_admin_id'), table_name='admin_auth_codes')
    op.drop_index(op.f('ix_admin_auth_codes_panel_admin_hash_id'), table_name='admin_auth_codes')
    op.drop_table('admin_auth_codes')
    op.drop_index(op.f('ix_panel_first_domain_users_password_history_user_id'), table_name='users_password_history',
                  schema='panel_first_domain')
    op.drop_table('users_password_history', schema='panel_first_domain')
    op.drop_index(op.f('ix_panel_first_domain_users_custom_rates_user_id'), table_name='users_custom_rates',
                  schema='panel_first_domain')
    op.drop_index(op.f('ix_panel_first_domain_users_custom_rates_service_id'), table_name='users_custom_rates',
                  schema='panel_first_domain')
    op.drop_table('users_custom_rates', schema='panel_first_domain')
    op.drop_index(op.f('ix_panel_first_domain_users_auth_codes_user_id'), table_name='users_auth_codes',
                  schema='panel_first_domain')
    op.drop_table('users_auth_codes', schema='panel_first_domain')
    op.drop_index(op.f('ix_panel_first_domain_users_apikey_history_user_id'), table_name='users_apikey_history',
                  schema='panel_first_domain')
    op.drop_table('users_apikey_history', schema='panel_first_domain')
    op.drop_index(op.f('ix_panel_first_domain_users_activity_log_user_id'), table_name='users_activity_log',
                  schema='panel_first_domain')
    op.drop_index(op.f('ix_panel_first_domain_users_activity_log_user_agent_id'), table_name='users_activity_log',
                  schema='panel_first_domain')
    op.drop_table('users_activity_log', schema='panel_first_domain')
    op.drop_index(op.f('ix_panel_first_domain_user_details_user_id'), table_name='user_details',
                  schema='panel_first_domain')
    op.drop_table('user_details', schema='panel_first_domain')
    op.drop_index(op.f('ix_panel_first_domain_user_custom_fields_user_id'), table_name='user_custom_fields',
                  schema='panel_first_domain')
    op.drop_table('user_custom_fields', schema='panel_first_domain')
    op.drop_table('users', schema='panel_first_domain')
    # ### end Alembic commands ###
