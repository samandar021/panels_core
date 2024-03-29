"""panel_template_db: init

Revision ID: 06b255c9cef8
Revises:
Create Date: 2023-08-14 14:26:25.749977

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '06b255c9cef8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'user_agent_list',
        sa.Column('user_agent_name', sa.String(length=300), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_template',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'users',
        sa.Column('username', sa.String(length=300), nullable=True),
        sa.Column('email', sa.String(length=300), nullable=True),
        sa.Column('refferer_id', sa.Integer(), nullable=True),
        sa.Column('password', sa.String(length=300), nullable=True),
        sa.Column('password_salt', sa.String(length=300), nullable=True),
        sa.Column('password_method', sa.Integer(), nullable=True),
        sa.Column('balance', sa.Float(), nullable=True),
        sa.Column('spent', sa.Float(), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.Integer(), nullable=True),
        sa.Column('auth_at', sa.Integer(), nullable=True),
        sa.Column('auth_ip', sa.Integer(), nullable=True),
        sa.Column('apikey', sa.String(length=64), nullable=True),
        sa.Column('refferal_key', sa.String(length=8), nullable=True),
        sa.Column('discount', sa.Integer(), nullable=True),
        sa.Column('timezone', sa.Integer(), nullable=True),
        sa.Column('terms_confirm', sa.Integer(), nullable=True),
        sa.Column('lang_code', sa.String(length=3), nullable=True),
        sa.Column('email_status', sa.Integer(), nullable=True, comment='0 - not confirmed, 1 - confirmed'),
        sa.Column('status', sa.Integer(), nullable=True, comment='1 - active, 2 - suspended'),
        sa.Column('options', sa.Text(), nullable=True),
        sa.Column('currency', sa.String(length=4), nullable=True),
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
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('refferal_key'),
        schema='panel_template',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_panel_template_users_username'), 'users', ['username'], unique=False,
                    schema='panel_template')
    op.create_table(
        'users_activity_log',
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('user_agent_id', sa.Integer(), nullable=True),
        sa.Column('ip', sa.Integer(), nullable=True),
        sa.Column('event', sa.Integer(), nullable=True),
        sa.Column('location', sa.String(length=1000), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_agent_id'], ['panel_template.user_agent_list.id'], onupdate='NO ACTION',
                                ondelete='NO ACTION'),
        sa.ForeignKeyConstraint(['user_id'], ['panel_template.users.id'], onupdate='NO ACTION', ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_template',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_panel_template_users_activity_log_user_agent_id'), 'users_activity_log',
                    ['user_agent_id'], unique=False, schema='panel_template')
    op.create_index(op.f('ix_panel_template_users_activity_log_user_id'), 'users_activity_log',
                    ['user_id'], unique=False, schema='panel_template')
    op.create_table(
        'users_apikey_history',
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('apikey', sa.String(length=128), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['panel_template.users.id'], onupdate='NO ACTION', ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_template',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_panel_template_users_apikey_history_user_id'), 'users_apikey_history',
                    ['user_id'], unique=False, schema='panel_template')
    op.create_table(
        'users_auth_codes',
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('event', sa.String(length=45), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['panel_template.users.id'], onupdate='NO ACTION', ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_template',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_panel_template_users_auth_codes_user_id'), 'users_auth_codes',
                    ['user_id'], unique=False, schema='panel_template')
    op.create_table(
        'users_custom_fields',
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('field_name', sa.String(length=300), nullable=True),
        sa.Column('field_value', sa.String(length=300), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['panel_template.users.id'], onupdate='NO ACTION', ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_template',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_panel_template_users_custom_fields_user_id'), 'users_custom_fields',
                    ['user_id'], unique=False, schema='panel_template')
    op.create_table(
        'users_custom_rates',
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('service_id', sa.Integer(), nullable=True),
        sa.Column('rate', sa.DECIMAL(precision=21.4), nullable=True),
        sa.Column('is_percent', sa.Integer(), nullable=True, comment='0 - fixed service rate, 1 - percent  of service rate'),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['panel_template.users.id'], onupdate='NO ACTION', ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_template',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_panel_template_users_custom_rates_service_id'), 'users_custom_rates',
                    ['service_id'], unique=False, schema='panel_template')
    op.create_index(op.f('ix_panel_template_users_custom_rates_user_id'), 'users_custom_rates',
                    ['user_id'], unique=False, schema='panel_template')
    op.create_table(
        'users_password_history',
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('password', sa.String(length=300), nullable=True),
        sa.Column('password_salt', sa.String(length=300), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['panel_template.users.id'], onupdate='NO ACTION', ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_template',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_panel_template_users_password_history_user_id'), 'users_password_history',
                    ['user_id'], unique=False, schema='panel_template')
    op.create_table(
        'activity_log',
        sa.Column('panel_admin_id', sa.Integer(), nullable=True),
        sa.Column('user_agent_id', sa.Integer(), nullable=True),
        sa.Column('super_admin', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.Column('ip', sa.Integer(), nullable=True),
        sa.Column('details_id', sa.Integer(), nullable=True),
        sa.Column('url', sa.String(length=1000), nullable=True),
        sa.Column('event_id', sa.Integer(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['panel_admin_id'], ['panels.panel_admin.id'], onupdate='NO ACTION',
                                ondelete='NO ACTION'),
        sa.ForeignKeyConstraint(['user_agent_id'], ['panel_template.user_agent_list.id'], onupdate='NO ACTION',
                                ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_template',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_panel_template_activity_log_panel_admin_id'), 'activity_log',
                    ['panel_admin_id'], unique=False, schema='panel_template')
    op.create_index(op.f('ix_panel_template_activity_log_user_agent_id'), 'activity_log',
                    ['user_agent_id'], unique=False, schema='panel_template')
    op.create_table(
        'activity_log_details',
        sa.Column('request_data', sa.Text(), nullable=True),
        sa.Column('activity_log_details_id', sa.Integer(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['activity_log_details_id'], ['panel_template.activity_log.id'], onupdate='NO ACTION',
                                ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panel_template',
        mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('activity_log_details', schema='panel_template')
    op.drop_table('activity_log', schema='panel_template')
    op.drop_table('users_password_history', schema='panel_template')
    op.drop_table('users_custom_rates', schema='panel_template')
    op.drop_table('users_custom_fields', schema='panel_template')
    op.drop_table('users_auth_codes', schema='panel_template')
    op.drop_table('users_apikey_history', schema='panel_template')
    op.drop_table('users_activity_log', schema='panel_template')
    op.drop_table('users', schema='panel_template')
    op.drop_table('user_agent_list', schema='panel_template')
    # ### end Alembic commands ###
