"""panels_db: update panels_db(add tables)

Revision ID: c1d5529674ef
Revises: bd6373d8fe77
Create Date: 2023-08-16 12:21:43.957824

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c1d5529674ef'
down_revision: Union[str, None] = 'bd6373d8fe77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'panel_user_custom_fields',
        sa.Column('variable_name', sa.String(length=100), nullable=True),
        sa.Column('translation_code', sa.String(length=50), nullable=True),
        sa.Column('rules', sa.JSON(), nullable=True),
        sa.Column('position', sa.Integer(), nullable=True),
        sa.Column('default', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='panels',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'payment_methods',
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('addfunds_form', sa.JSON(), nullable=True),
        sa.Column('settings_form', sa.JSON(), nullable=True),
        sa.Column('settings_form_description', sa.String(length=300), nullable=True),
        sa.Column('has_take_fee', sa.Integer(), nullable=True),
        sa.Column('has_extra_fee', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.Integer(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='panels',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'payment_methods_currencies',
        sa.Column('method_id', sa.Integer(), nullable=True),
        sa.Column('currency', sa.String(length=50), nullable=True),
        sa.Column('position', sa.Integer(), nullable=True),
        sa.Column('settings_form', sa.JSON(), nullable=True),
        sa.Column('settings_form_description', sa.String(length=300), nullable=True),
        sa.Column('is_available', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.Integer(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['method_id'], ['panels.payment_methods.id'], onupdate='NO ACTION',
                                ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panels',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_panels_payment_methods_currencies_currency'), 'payment_methods_currencies',
                    ['currency'], unique=True, schema='panels')
    op.create_index(op.f('ix_panels_payment_methods_currencies_method_id'), 'payment_methods_currencies',
                    ['method_id'], unique=True, schema='panels')
    op.create_table(
        'panel_payment_methods',
        sa.Column('panel_id', sa.Integer(), nullable=True),
        sa.Column('method_id', sa.Integer(), nullable=True),
        sa.Column('currency_id', sa.Integer(), nullable=True),
        sa.Column('is_visible', sa.Boolean(), nullable=True),
        sa.Column('webhook_url', sa.String(length=500), nullable=True),
        sa.Column('is_test_mode', sa.Boolean(), nullable=True),
        sa.Column('min_amount', sa.Integer(), nullable=True),
        sa.Column('max_amount', sa.Integer(), nullable=True),
        sa.Column('is_deleted', sa.Integer(), nullable=True),
        sa.Column('amount_currency', sa.Integer(), nullable=True),
        sa.Column('has_available_for_new_user', sa.Integer(), nullable=True),
        sa.Column('position', sa.Integer(), nullable=True),
        sa.Column('has_extra_fee', sa.Integer(), nullable=True),
        sa.Column('has_take_from_user', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.Integer(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['currency_id'], ['panels.payment_methods_currencies.id'], onupdate='NO ACTION',
                                ondelete='NO ACTION'),
        sa.ForeignKeyConstraint(['method_id'], ['panels.payment_methods.id'], onupdate='NO ACTION',
                                ondelete='NO ACTION'),
        sa.ForeignKeyConstraint(['panel_id'], ['panels.panels.id'], onupdate='NO ACTION', ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panels',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'panel_payment_methods_bonuses',
        sa.Column('panel_payment_methods_id', sa.Integer(), nullable=True),
        sa.Column('amount_percent', sa.Integer(), nullable=True),
        sa.Column('deposit_from', sa.Integer(), nullable=True),
        sa.Column('is_available', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.Integer(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['panel_payment_methods_id'], ['panels.panel_payment_methods.id'], onupdate='NO ACTION',
                                ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panels',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'panel_payment_methods_options',
        sa.Column('panel_payment_methods_id', sa.Integer(), nullable=True),
        sa.Column('options', sa.Text(length=5000), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['panel_payment_methods_id'], ['panels.panel_payment_methods.id'], onupdate='NO ACTION',
                                ondelete='NO ACTION'),
        sa.PrimaryKeyConstraint('id'),
        schema='panels',
        mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('panel_payment_methods_options', schema='panels')
    op.drop_table('panel_payment_methods_bonuses', schema='panels')
    op.drop_table('panel_payment_methods', schema='panels')
    op.drop_table('payment_methods_currencies', schema='panels')
    op.drop_table('payment_methods', schema='panels')
    op.drop_table('panel_user_custom_fields', schema='panels')
    # ### end Alembic commands ###
